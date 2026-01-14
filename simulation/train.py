import enum

from positionalAgent import *
from block import *

class State(Enum):
    GO = 0
    CAUTION = 1
    STOP = 2
    STATION = 3
    PASS_STATION = 4

    def __str__(self):
        return f'{self.name}'


class Train(PositionalAgent):
    def __init__(self, model, position, speed, acceleration, braking):
        super().__init__(model, position)
        # self.mass = mass
        self._wait = None
        self.braking = braking
        self.acceleration = acceleration
        self.max_speed = speed
        self.speed = speed
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_train(self)
        self.position = position
        self.state = State.GO
        self.dt = model.dt
        self.wait = None

    def step(self):
        # Look at the signal, update the state and do stuff accordingly
        signal, distance = self.signalling_control.next_signal(self)

        if signal == Color.GREEN:
            self.state = State.GO
        elif signal == Color.ORANGE:
            self.state = State.CAUTION
        elif signal == Color.RED:
            self.state = State.STOP
        elif signal == Color.STATION and self.state != State.PASS_STATION:
            self.state = State.STATION


        if self.state == State.GO:
            self.go_to_speed(self.max_speed)
        elif self.state == State.CAUTION:
            if signal == Color.UNKNOWN and self.brake_distance(0) > distance - 20:
                self.go_to_speed(0)
            else:
                self.go_to_speed(self.max_speed)
        elif self.state == State.STOP or self.state == State.STATION:
            if self.brake_distance(0) > distance - 20:
                self.go_to_speed(0)
            if self.brake_distance(0, 1) > distance:
                raise Exception(f"Unable to brake in time. {self}")
        elif self.state == State.PASS_STATION:
            self.go_to_speed(10)

        if self.state == State.STATION and self.speed == 0:
            self.wait = self.wait - self.dt if self.wait is not None else self.model.wait_time
            if self.wait <= 0:
                self.state = State.PASS_STATION
                self.wait = None

        self.position += self.speed * self.dt


    def go_to_speed(self, speed):
        assert(0 <= speed <= self.max_speed)

        if self.speed > speed:
            self.speed = max(speed, self.speed - self.braking * self.dt)
        elif self.speed < speed:
            self.speed = min(speed, self.speed + self.acceleration * self.dt)


    def brake_distance(self, speed, safety_factor = 0.9):
        if self.speed > speed:
            return (self.speed - speed)**2 / (2 * self.braking * safety_factor)
        else:
            return 0


    def __str__(self):
        signal, distance = self.signalling_control.next_signal(self)
        return f"{self.position}, speed: {self.speed:.1f}, state: {self.state}, next signal: {signal} in {distance:.0f}"


    def get_resistance(self):
        return 0

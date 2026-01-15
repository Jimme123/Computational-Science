import enum
import math
from simulation.positionalAgent import *
from simulation.block import *

class State(Enum):
    GO = 0
    CAUTION = 1
    STOP = 2
    STATION = 3
    PASS_STATION = 4

    def __str__(self):
        return f'{self.name}'


class Train(PositionalAgent):
    def __init__(self, model, position, speed, max_acceleration, braking, max_power=None, weight=None):
        super().__init__(model, position)
        self._wait = None
        self.max_braking = braking
        self.max_acceleration = max_acceleration
        self.max_speed = speed
        self.speed = 0
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_train(self)
        self.position = position
        self.dt = model.dt
        self.power = max_power
        self.weight = weight

        self.state = State.GO
        self.wait = None

    def step(self):
        # Look at the signal, update the state and do stuff accordingly
        signal, distance = self.signalling_control.next_signal(self)
        braking, acceleration = self.acceleration_bounds()

        if signal == Color.GREEN:
            self.state = State.GO
        elif signal == Color.ORANGE:
            self.state = State.CAUTION
        elif signal == Color.RED:
            self.state = State.STOP
        elif signal == Color.STATION and self.state != State.PASS_STATION:
            self.state = State.STATION

        if self.state == State.GO:
            self.go_to_speed(self.max_speed, braking, acceleration)
        elif self.state == State.CAUTION:
            if signal == Color.UNKNOWN and self.brake_distance(0) > distance - 20:
                self.go_to_speed(0, braking, acceleration)
            else:
                self.go_to_speed(self.max_speed, braking, acceleration)
        elif self.state == State.STOP or self.state == State.STATION:
            if self.brake_distance(0, 1) > distance:
                raise Exception(f"Unable to brake in time. {self}")

            if self.brake_distance(0) > distance - self.speed * self.dt - 20:
                self.go_to_speed(0, braking, acceleration)
            else:
                self.go_to_speed(self.max_speed, braking, acceleration)
        elif self.state == State.PASS_STATION:
            self.go_to_speed(3, braking, acceleration)

        if self.state == State.STATION and self.speed == 0:
            self.wait = self.wait - self.dt if self.wait is not None else self.model.wait_time
            if self.wait <= 0:
                self.state = State.PASS_STATION
                self.wait = None

        self.position += self.speed * self.dt


    def go_to_speed(self, speed, braking, acceleration):
        assert(0 <= speed <= self.max_speed)

        if self.speed > speed:
            self.speed = max(speed, self.speed - braking * self.dt)
        elif self.speed < speed:
            self.speed = min(speed, self.speed + acceleration * self.dt)


    def brake_distance(self, speed, safety_factor = 0.9):
        if self.speed > speed:
            return (self.speed - speed)**2 / (2 * self.max_braking * safety_factor)
        else:
            return 0


    def acceleration_bounds(self):
        if self.power is not None and self.weight is not None:
            power_limit = float(self.power) / float(self.speed * self.weight) if self.speed != 0 else math.inf
        return self.max_braking, min(power_limit, self.max_acceleration)


    def __str__(self):
        signal, distance = self.signalling_control.next_signal(self)
        return f"{self.position}, speed: {self.speed:.1f}, state: {self.state}, next signal: {signal} in {distance:.0f}"


    def get_resistance(self):
        return 0

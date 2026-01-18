import enum
import math
from typing import TypedDict, NotRequired
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


class TrainSpecifications(TypedDict):
    max_braking: float
    max_acceleration: float
    max_speed: float
    max_power: NotRequired[float]
    weight: NotRequired[float]
    length: NotRequired[float]



class Train(PositionalAgent):
    def __init__(self, model, position, train_specification: TrainSpecifications):
        super().__init__(model, position)
        self.max_braking = train_specification['max_braking']
        self.max_acceleration = train_specification['max_acceleration']
        self.max_speed = train_specification['max_speed']
        self.power = train_specification['max_power'] if 'power' in train_specification else None
        self.weight = train_specification['weight'] if 'weight' in train_specification else None
        self.position = position

        self.dt = model.dt
        self.clearance = model.clearance
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_train(self)

        self.speed = 0
        self.state = State.CAUTION
        self.wait = None

    def step(self):
        # Look at the signal, update the state and do stuff accordingly
        signal, distance = self.signalling_control.next_signal(self.position)
        braking, acceleration = self.acceleration_bounds()

        # Handle the signals
        if signal == Color.GREEN:
            self.state = State.GO
        elif signal == Color.ORANGE:
            self.state = State.CAUTION
        elif signal == Color.RED:
            self.state = State.STOP
        elif signal == Color.STATION and self.state != State.PASS_STATION:
            self.state = State.STATION
        elif signal == Color.STATION and self.state == State.PASS_STATION:
            if distance > 30:
                self.state = State.STATION


        if self.state == State.GO:
            self.go_to_speed(self.max_speed, braking, acceleration)

        elif self.state == State.CAUTION:
            if signal == Color.UNKNOWN:
                self.stop_at(distance, braking, acceleration)
            else:
                self.go_to_speed(self.max_speed, braking, acceleration)

        elif self.state == State.STOP or self.state == State.STATION:
            self.stop_at(distance, braking, acceleration)

        elif self.state == State.PASS_STATION:
            signal, distance = self.signalling_control.next_next_signal(self.position)
            if signal == Color.RED or signal == Color.STATION:
                self.stop_at(distance, braking, acceleration)
            else:
                self.go_to_speed(self.max_speed, braking, acceleration)

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


    def braking_distance_to_zero(self, safety_factor=0.9):
        return (self.speed ** 2) / (2 * self.max_braking * safety_factor)


    def stop_at(self, distance, braking, acceleration):
        if self.brake_distance(0, 1) > distance:
            raise Exception(f"Unable to brake in time. {self}")

        if self.brake_distance(0) > distance - self.speed * self.dt - self.clearance:
            self.go_to_speed(0, braking, acceleration)
        else:
            self.go_to_speed(self.max_speed, braking, acceleration)


    def acceleration_bounds(self):
        if self.power is not None and self.weight is not None:
            power_limit = float(self.power) / float(self.speed * self.weight) if self.speed != 0 else math.inf
            return self.max_braking, min(power_limit, self.max_acceleration)
        else:
            return self.max_braking, self.max_acceleration


    def __str__(self):
        signal, distance = self.signalling_control.next_signal(self.position)
        if self.state == State.PASS_STATION:
            signal2, distance2 = self.signalling_control.next_next_signal(self.position)
            return f"""{self.position}, speed: {self.speed:.1f}, state: {self.state}, next signal: {signal} in {distance:.0f}, next next signal: {signal2} in {distance2:.0f}"""
        else:
            return f"{self.position}, speed: {self.speed:.1f}, state: {self.state}, next signal: {signal} in {distance:.0f}"


    def get_resistance(self):
        return 0

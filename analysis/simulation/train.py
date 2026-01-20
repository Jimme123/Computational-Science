import enum
import math
from typing import TypedDict, NotRequired
from simulation.positionalAgent import *
from simulation.block import *


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
        self.length = train_specification.get("length", 0)
        self.position = position

        self.speed = 0
        self.speed_limit = 10
        self.next_speed_limit = 0
        self.station_wait = None

        self.dt = model.dt
        self.clearance = model.clearance
        self.wait_time = model.wait_time
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_train(self)


    def step(self):
        # Look at the signal, update the state and do stuff accordingly
        signal, distance = self.signalling_control.next_signal(self.position)
        braking, acceleration = self.acceleration_bounds()

        if signal == "unknown":
            self.go_at(distance, self.next_speed_limit, braking, acceleration)
        else:
            if signal.is_station:
                if self.speed == 0:
                    if self.station_wait is None:
                        self.station_wait = self.wait_time
                    else:
                        self.station_wait = self.station_wait - self.dt

            if self.station_wait is not None and self.station_wait <= 0:
                self.go_at(distance + signal.distance_to_next_signal, signal.max_speed_next, braking, acceleration)
            else:
                self.go_at(distance, signal.max_speed, braking, acceleration)

        dx = self.speed * self.dt
        self.position += dx

        if dx >= distance:
            self.next_speed_limit = signal.max_speed_next
            if not signal.is_station:
                self.speed_limit = signal.max_speed
            else:
                self.speed_limit = math.inf
                self.station_wait = None


    def go_to_speed(self, speed, braking, acceleration):
        assert(0 <= speed <= self.max_speed)

        if self.speed > speed:
            self.speed = max(speed, self.speed - braking * self.dt)
        elif self.speed < speed:
            self.speed = min(speed, self.speed + acceleration * self.dt)


    def brake_distance(self, speed, safety_factor = 0.9):
        if self.speed > speed:
            return (self.speed - speed)*(self.speed + speed) / (2 * self.max_braking * safety_factor)
        else:
            return 0


    def speed_bound(self, distance, speed, braking):
        if distance < 0:
            return speed
        else:
            return max(math.sqrt(2*distance*braking + speed**2) - braking * self.dt, speed)


    def go_at(self, distance, speed, braking, acceleration):
        """
            Make the train go as fast as possible while being able to go a certain speed some distance from now.
        """
        current_max_speed = min(self.speed_limit, self.max_speed)
        if self.speed > current_max_speed:
            raise Exception(f"speeding {self}")

        target_speed = min(speed, current_max_speed)
        upper_envelope = self.speed_bound(distance - self.clearance, target_speed, braking)

        if upper_envelope < self.speed - braking * self.dt:
            raise Exception(f"Unable to brake in time. {self}")
        elif speed == 0 and self.speed < braking * self.dt and distance < 2 * self.clearance:
            self.speed = 0
        else:
            self.speed = min(upper_envelope, self.speed + acceleration * self.dt, current_max_speed)


    def acceleration_bounds(self):
        if self.power is not None and self.weight is not None:
            power_limit = float(self.power) / float(self.speed * self.weight) if self.speed != 0 else math.inf
            return self.max_braking, min(power_limit, self.max_acceleration)
        else:
            return self.max_braking, self.max_acceleration


    def __str__(self):
        signal, distance = self.signalling_control.next_signal(self.position)

        signal_text = f"uncertain {self.next_speed_limit}" if signal == "unknown" else f"{signal.max_speed:.0f}"
        station_text = ""
        if self.station_wait is not None and self.station_wait > 0:
            station_text = f" at station for {self.station_wait:.0f}"
        elif self.station_wait is not None:
            station_text = f" leaving station"
        elif signal != "unknown" and signal.is_station:
            station_text = " approaching station"

        return f"pos: {self.position}, speed: {self.speed:.1f}, speed limit: {self.speed_limit:.0f}, next limit: {signal_text} in {distance:.0f}" + station_text


    def get_resistance(self):
        return 0

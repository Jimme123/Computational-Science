from positionalAgent import *
from block import *

dt = 1
rho = 1.05  # rotating mass-factor (for now)

class Train(PositionalAgent):
    def __init__(self, model, position, speed, acceleration, braking):
        super().__init__(model, position)
        # self.mass = mass
        self.braking = braking
        self.acceleration = acceleration
        self.max_speed = speed
        self.speed = speed
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_train(self)
        self.position = position

    def step(self):
        signal, distance = self.signalling_control.next_signal(self)

        if signal != Color.STATION:
            self._wait = None
        else:
            if self.speed == 0:
                self._wait = self._wait - dt if self._wait is not None else 10
            
            if self._wait is not None and self._wait <= 0:
                signal = Color.ORANGE
            else:
                signal = Color.RED

        if signal == Color.RED:
            # Go half speed and stop 20m before the signal
            if self.brake_distance(0) > distance - 20:
                self.speed = max(0, self.speed - self.braking * dt)
            elif self.speed > self.max_speed / 2:
                self.speed = max(self.max_speed / 2, self.speed - self.braking * dt)
            elif self.speed < self.max_speed / 2:
                self.speed = min(self.max_speed / 2, self.speed + self.acceleration * dt)

        if signal == Color.ORANGE:
            # Go maximal speed as long as possible, but pass the signal at half speed
            if self.brake_distance(self.max_speed / 2) > distance:
                self.speed = max(self.max_speed / 2, self.speed - self.braking * dt)
            elif self.speed > self.max_speed:
                self.speed = max(self.max_speed, self.speed - self.braking * dt)
            elif self.speed < self.max_speed:
                self.speed = min(self.max_speed, self.speed + self.acceleration * dt)
        
        if signal == Color.GREEN:
            # Full steam ahead
            self.speed = min(self.max_speed, self.speed + self.acceleration * dt)


        self.position += self.speed * dt

        # if self.position.start >= self.signalling_control.length:
        #     self.signalling_control.remove_train(self)
        #     super().remove()

    def brake_distance(self, speed):
        return (self.speed - speed)**2 / 2*self.braking if self.speed > speed else 0

    def __str__(self):
        signal, distance = self.signalling_control.next_signal(self)
        return f"{self.position}, speed: {self.speed:.1f}, next signal: {signal} in {distance:.0f}"

#    def get_acceleration(self, tractive_force):
#        if self.speed == self.max_speed:
#            return 0
#
#        resistance = self.get_resistance()
#        acceleration = (tractive_force - resistance) / (self.mass * rho)
#
#        if self.speed <= 0 & acceleration <= 0:
#            return 0
#        
#        return acceleration
    
    def get_resistance(self):
        return 0

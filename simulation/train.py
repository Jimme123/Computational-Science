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

        if signal == Color.RED:
            acceleration = self.braking if (self.brake_distance(0) > distance - 20) else 0
        elif signal == Color.ORANGE:
            acceleration = self.braking if self.brake_distance(self.max_speed / 2) > distance - 20 else (self.acceleration if self.speed < self.max_speed else 0)
        else:
            acceleration = self.acceleration if self.speed < self.max_speed else 0

        self.speed += acceleration * dt
        if self.speed < 0:
            self.speed = 0
        self.position += self.speed * dt

        if self.position.start >= self.signalling_control.length:
            self.signalling_control.remove_train(self)
            super().remove()

    def brake_distance(self, speed):
        return (self.speed - speed)**2 / 2*-self.braking

    def __str__(self):
        return f"{self.position}, speed: {self.speed:.1f}"

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

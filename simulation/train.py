from positionalAgent import *
from block import *

dt = 1
rho = 1.05  # rotating mass-factor (for now)

class Train(PositionalAgent):
    def __init__(self, model, mass, position, rails, speed, fmax, fmin):
        super().__init__(model, position)
        self.mass = mass
        self.fmax = fmax
        self.fmin = fmin
        self.max_speed = speed
        self.speed = speed
        self.rails = rails
        self.rails.add_train(self)
        self.position = position

    def move(self, direction):
        acceleration = self.get_acceleration()
        self.speed += acceleration * dt

        signal = self.model.rails.next_signal(self)
        # signal = self.model.rails.next_signal(next_position)

        if signal == Color.RED:
            acceleration = self.get_acceleration(self.fmin)
        elif signal == Color.ORANGE:
            acceleration = self.get_acceleration(self.fmin)
        else:
            acceleration = self.get_acceleration(self.fmax)

        self.speed += acceleration * dt
        self.position += self.postion + self.speed * dt

        if self.position.start >= self.rails.length:
            self.rails.remove_train(self)
            super().remove()

    def step(self):
        self.move(direction = 1)

    def get_acceleration(self, tractive_force):
        if self.speed == self.max_speed:
            return 0

        resistance = self.get_resistance()
        acceleration =  (tractive_force - resistance) / (self.mass * rho)

        if self.speed <= 0 & acceleration <= 0:
            return 0
        
        return acceleration
    
    def get_resistance(self):
        pass
    

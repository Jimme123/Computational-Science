from positionalAgent import *
from block import *

class Train(PositionalAgent):
    def __init__(self, model, position, rails, speed):
        super().__init__(model, position)
        self.max_speed = speed
        self.speed = speed
        self.rails = rails
        self.rails.add_train(self)
        self.position = position

    def move(self, direction):
        next_position = self.position + self.speed * direction

        signal = self.model.rails.next_signal(self)
        # signal = self.model.rails.next_signal(next_position)

        if signal == Color.RED:
            self.speed = 0
        elif signal == Color.ORANGE:
            self.speed = max(self.max_speed / 2, 1)
            self.position += self.speed * direction
        else:
            self.position = next_position

        if self.position.start >= self.rails.length:
            self.rails.remove_train(self)
            super().remove()

    def step(self):
        self.move(direction = 1)

from positionalAgent import *
from block import *

class Train(PositionalAgent):
    def __init__(self, model, position, rails, speed):
        super().__init__(model, position)
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
            self.speed = max(self.speed / 2, 1)
            self.position += self.speed * direction
        else:
            self.position = next_position

    def step(self):
        self.move(direction = 1)

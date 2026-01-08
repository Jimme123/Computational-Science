from positionalAgent import *

class Train(PositionalAgent):
    def __init__(self, model, position, rails, speed):
        super().__init__(model, position)
        self.speed = speed
        self.rails.add_train(self)

    def move(self, direction):
        next_position = self.position + self.speed * direction

        signal = self.model.rails.next_signal(next_position)

        if signal == "RED":
            self.speed = 0
        elif signal == "ORANGE":
            self.speed = max(self.speed / 2, 1)
            self.position += self.speed * direction
        else:
            self.position = next_position

    def step(self):
        self.move(direction = 1)

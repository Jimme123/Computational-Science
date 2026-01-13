import mesa

from block import *
from rails import *
from train import *

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length):
        super().__init__()
        self.rails = Rails(self, 10000)
        self.trains = [
            Train(model=self, position=Position(0,100), rails=self.rails, max_speed=50),
            Train(model=self, position=Position(3000,3100), rails=self.rails, max_speed=30)
        ]
        n = 20
        self.blocks = []
        for i in range(n):
            pos = Position(i * length / n, (i + 1) * length / n)
            block = Block(self, pos, self.rails)
            self.blocks.append(block)

    def step(self):
        """Advance the model by one step."""
        print("step")
        for train in self.trains:
            train.step()


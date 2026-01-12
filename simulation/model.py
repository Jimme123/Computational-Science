import mesa

from block import *
from signallingControl import *
from train import *

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length, type):
        super().__init__()
        self.signalling_control = SignallingControl(self, 10000)
        self.trains = Train.create_agents(self, 2, [Position(0, 100), Position(3000, 3100)], self.signalling_control, [55, 25], 1.1, -1.3)
        n = 20
        self.blocks = Block.create_agents(self, n, [Position(i * length / n, (i + 1) * length / n) for i in range(n)], self.signalling_control)
        

    def step(self):
        """Advance the model by one step."""
        print("step")
        self.trains.shuffle_do("step")
        for train in self.trains:
            print(train)
 

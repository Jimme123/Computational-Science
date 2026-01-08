import mesa

from signal import *
from rails import *
from train import *

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length):
        super().__init__()
        self.rails = Rails(10000)
        Trains = Train.create_agents(self, 2, rails, [Position(0, 100), Position(3000, 3100)], [200, 100])
        n = 20
        Blocks = Block.create_agents(self, n, rails, [Position(x * length / n, x + length / n) for i in range(n)])
        

    def step(self):
        """Advance the model by one step."""
        self.Trains.shuffle_do("step")
 

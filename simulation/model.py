import mesa

from block import *
from train import *

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length, signalling_control_class):
        super().__init__()
        self.signalling_control = signalling_control_class(self, 10000)
        self._step = 0
        

    def step(self):
        """Advance the model by one step."""
        self._step += 1
        print(f"step {self._step}")
        self.trains.shuffle_do("step")
        for train in self.trains:
            print(train)
    
    def add_train(*args):
        Train.create_agents(self, 1, self.signalling_control, *args)

    def add_block(*args):
        Block.create_agents(self, 1, self.signalling_control, *args)
 

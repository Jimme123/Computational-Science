import mesa

from block import *
from train import *

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length, signalling_control_class):
        super().__init__()
        self.signalling_control = signalling_control_class(self, 10000)
        

    def step(self):
        """Advance the model by one step."""
        print("step")
        self.trains.shuffle_do("step")
        for train in self.trains:
            print(train)
    
    def add_train(*args):
        Train.create_agents(self, 1, *args)

    def add_block(*args):
        Block.create_agents(self, 1, *args)
 

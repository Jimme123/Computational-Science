import mesa

from block import *
from train import *

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length, signalling_control_class, sight, dt, wait_time):
        super().__init__()
        self.signalling_control = signalling_control_class(self, length)
        self._step = 0
        self.trains = Train.create_agents(self, 0)
        self.sight = sight
        self.dt = dt
        self.wait_time = wait_time
        

    def step(self):
        """Advance the model by one step."""
        self._step += 1
        print(f"step {self._step}")
        self.trains.shuffle_do("step")
        for train in self.trains:
            print(train)
    
    def add_train(self, *args):
        self.trains.add(Train(self, *args))

    def add_block(self, *args):
        Block(self, *args)

    def add_station(self, *args):
        Station(self, *args)
 

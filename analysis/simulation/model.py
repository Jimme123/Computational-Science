import mesa
import math

from simulation.block import *
from simulation.train import *
from simulation.position import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *

class Railroad(mesa.Model):
    """The model containing the trains signal, stations, etc."""

    def __init__(self, length, signalling_control_class, dt, wait_time, sight=math.inf, clearance=20, verbose=False):
        super().__init__()
        self.signalling_control = signalling_control_class(self, length)
        self._step = 0
        self.trains = Train.create_agents(self, 0)
        self.sight = sight
        self.clearance = clearance
        self.dt = dt
        self.wait_time = wait_time
        self.verbose = verbose
        self.type = "static" if signalling_control_class == StaticBlockSignalling else "moving"


    def step(self):
        """Advance the model by one step. Print the details if verbose is on."""
        self._step += 1
        self.trains.shuffle_do("step")

        if self.verbose:
            print(f"step {self._step}")
            for train in self.trains:
                print(train)

    def add_train(self, *args):
        self.trains.add(Train(self, *args))

    def add_block(self, *args):
        Block(self, *args)

    def add_station(self, *args):
        Station(self, *args)

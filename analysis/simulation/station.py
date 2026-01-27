import mesa

from simulation.block import *

class Station(Block):
    def __init__(self, model, position):
        super().__init__(model, position)

    @property
    def signal(self):
        return SignalState.STATION

    def is_stop(self):
        return True

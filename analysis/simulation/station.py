import mesa

from block import *

class Station(Block):
    def __init__(self, model, position):
        super().__init__(model, position)

    @property
    def signal(self):
        return Color.STATION

    def is_stop(self):
        return True

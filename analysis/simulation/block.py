import mesa
from enum import Enum

from simulation.positionalAgent import *

class Color(Enum):
    UNKNOWN = 0
    GREEN = 1
    ORANGE = 2
    RED = 3
    STATION = 4

    def __str__(self):
        return f'{self.name}'

class Block(PositionalAgent):
    def __init__(self, model, position):
        super().__init__(model, position)
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_block(self)

    @property
    def signal(self):
        """
        Returns signal colour based on train positions:
        - RED if train is in this block
        - ORANGE if next block is occupied
        - GREEN otherwise
        """
        next_block = self.signalling_control.get_next_block(self)
        if next_block is None:
            return Color.GREEN
        elif self.is_stop():
            return Color.RED
        elif next_block.is_stop():
            return Color.ORANGE
        else:
            return Color.GREEN

    def is_stop(self):
        return self.signalling_control.block_contains_train(self)

class Station(Block):
    def __init__(self, model, position):
        super().__init__(model, position)

    @property
    def signal(self):
        return Color.STATION

    def is_stop(self):
        return True

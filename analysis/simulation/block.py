"""
    A block is a piece of track in which only one train can be at a time.
    The block starts with a signal. This signal can be
     - red      if the block a train
     - orange   if the train has to stop at the next signal
     - green    if the train can continue at full speed
     - station  this is how we implement a station. This signals that the train should stop before this block,
                wait for a bit and then ignore the signal.
"""

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
            Returns signal color.
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
        """
            Returns if this signal has a stop.
            Block call this is to prevent a recursion loop where each block ask the next block for it's signal.
        """
        return self.signalling_control.block_contains_train(self)

class Station(Block):
    """
        This just sends a station signal.
        This signals that the train should stop before this block, wait for a bit and then ignore the signal.
        Notice that if a train is wholly contained in this station,
        it might cause a collision because the departing train ignores the signal.
    """

    def __init__(self, model, position):
        assert(position.length <= 10)
        super().__init__(model, position)

    @property
    def signal(self):
        return Color.STATION

    def is_stop(self):
        return True

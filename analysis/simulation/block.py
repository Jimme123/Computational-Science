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
import math
from enum import Enum

from simulation.positionalAgent import *

class SignalState:
    def __init__(self, max_speed=math.inf, max_speed_next=math.inf,
                 distance_to_next_signal=0, is_station=False):
        self.max_speed = max_speed  # speed at which train can pass this signal
        self.max_speed_next = max_speed_next  # speed at which train can pass next signal
        self.is_station = is_station
        self.distance_to_next_signal = distance_to_next_signal
        if is_station:
            assert (max_speed == 0)

    def make_station(self):
        self.is_station = True
        self.max_speed = 0

    def __str__(self):
        if self.is_station:
            return f"Station, next_signal: {self.max_speed_next} in \
            {self.distance_to_next_signal}"
        else:
            return f"signal: {self.max_speed}, next_signal: {self.max_speed_next}"


class Block(PositionalAgent):
    def __init__(self, model, position, max_speed=math.inf):
        super().__init__(model, position)
        self.signalling_control = self.model.signalling_control
        self.signalling_control.add_block(self)
        self.max_speed = max_speed  # speed at which train can pass this block

    @property
    def signal(self):
        """
            Returns a signal state
        """
        next_block, _ = self.signalling_control.get_next_block(self.position)

        if next_block is None:  
            return SignalState(self.speed())
        else:
            if next_block == self:
                distance = self.position.rail_length
            else:
                distance = get_distance(self.position, next_block.position) + self.position.length
            # return max speed in current block, next block and distance
            # between blocks
            return SignalState(self.speed(), next_block.speed(), distance)

    def speed(self):
        """
            Returns the speed with which this signal can be passed.
        """
        if self.signalling_control.block_contains_train(self):
            return 0
        else:
            return self.max_speed

    def __str__(self):
        return f'{self.position}'


class Station(Block):
    """
        This just sends a station signal.
        This signals that the train should stop before this block, wait for a bit and then ignore the signal.
    """

    def __init__(self, model, position):
        assert(position.length <= 20)
        super().__init__(model, position)

    @property
    def signal(self):
        signal_information = super().signal
        signal_information.make_station()
        return signal_information

    def speed(self):
        return 0

    def __str__(self):
        return f'station {self.position}'

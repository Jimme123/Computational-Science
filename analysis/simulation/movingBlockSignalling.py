"""
Moving block signalling class that bases the signalling on the distances
between trains and stations
"""
from simulation.staticBlockSignalling import *
from simulation.block import *


class MovingBlockSignalling(StaticBlockSignalling):

    def __init__(self, model, length):
        super().__init__(model, length)

    def next_signal(self, position):
        signal, signal_distance = super().next_signal(position)
        train, train_distance = self.get_next_object(self.trains, position)

        if train_distance <= signal_distance:  # train is closest
            return (SignalState(0), train_distance)  # add red signal at end of next train
        else:  # next signal is closest
            if signal.distance_to_next_signal > train_distance:  # train is closer than next signal
                # alter the signal
                signal.distance_to_next_signal = train_distance
                signal.max_speed_next = 0
            return (signal, signal_distance)

from simulation.staticBlockSignalling import *
from simulation.block import *


class MovingBlockSignalling(StaticBlockSignalling):

    def __init__(self, model, length):
        super().__init__(model, length)

    def next_signal(self, position):
        signal, signal_distance = super().next_signal(position)
        train, train_distance = self.get_next_object(self.trains, position)

        if train_distance <= signal_distance:
            return (SignalState(0), train_distance)
        else:
            if signal.distance_to_next_signal > train_distance:
                signal.distance_to_next_signal = train_distance
                signal.max_speed_next = 0
            return (signal, signal_distance)

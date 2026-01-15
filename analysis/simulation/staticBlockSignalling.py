import mesa
import math

from simulation.positionalAgent import *
from simulation.position import *
from simulation.block import *
from simulation.signallingControl import *

class StaticBlockSignalling(SignallingControl):
    def __init__(self, model, length):
        super().__init__(model, length)
        self.blocks = []

    def add_train(self, train):
        occupied_blocks = self.blocks_occupied_train(train)
        for block in occupied_blocks:
            if self.block_contains_train(block):
                raise Exception("Block already contains train")

        super().add_train(train)


    def add_block(self, block):
        self.blocks.append(block)

    def get_next_block(self, train):
        """
            Gets the next block from the train. Returns the distance and block.
        """
        min_distance = math.inf
        min_block = None
        for block in self.blocks:
            if get_distance(train, block) < min_distance:
                min_block = block
                min_distance = get_distance(train, block)
        return min_distance, min_block

    def next_signal(self, train):
        """
        input: train
        output: next signal for the train with the distance. If the signal is to far to see, it is unknown.
                (The driver still gets the distance, because they have to memorize the signal positions.)
        """
        distance, block = self.get_next_block(train)

        if next_block is None:
            return (Color.GREEN, math.inf)
        else:
            signal = next_block.signal

        if distance > self.model.sight:
            return (Color.UNKNOWN, distance)
        else:
            return (signal, distance)

    def block_contains_train(self, block):
        """
        input: block
        output: true if a train is in the block, false otherwise
        """
        for train in self.trains:
            if overlap(train.position, block.position):
                return True
        return False
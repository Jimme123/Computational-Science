import mesa
import math
import copy

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


    def blocks_occupied_train(self, train):
        """
        input: train
        output: list of blocks where the train is
        """
        blocks_occupied = []
        for block in self.blocks:
            if overlap(train.position, block.position):
                blocks_occupied.append(block)
        return blocks_occupied


    def get_next_object(self, objects, position, strict = False):
        """
            From a list of (positional) objects, selects the object which is in front of the position.
            So objects overlapping with the position are excluded.
            If strict is true, objects which are a distance of zero from the agent are also excluded.
        """
        min_distance = math.inf
        min_obj = None
        for obj in objects:
            distance = get_distance(position, obj.position, False)
            if distance < min_distance and (not strict or 0 < distance):
                min_obj = obj
                min_distance = distance
        return min_obj, min_distance



    def get_next_block(self, position, strict = False):
        """
            See get_next_position
        """
        return self.get_next_object(self.blocks, position, strict)


    def next_signal(self, position):
        """
        input: position
        output: next signal from the position with the distance. If the signal is to far to see, it is unknown.
                (The driver still gets the distance, because they have to memorize the signal positions.)
        """
        block, distance = self.get_next_block(position, True)

        if block is None:
            return (Color.GREEN, math.inf)

        signal = block.signal

        if distance > self.model.sight:
            return (Color.UNKNOWN, distance)
        else:
            return (signal, distance)


    def next_next_signal(self, position):
        """
        input: train
        output: The signal past the next signal for the train with the distance. If the signal is to far to see, it is unknown.
                (The driver still gets the distance, because they have to memorize the signal positions.)

        This function is useful when looking past station signals.
        """
        _, distance = self.next_signal(position)
        position = copy.deepcopy(position)
        position += distance
        return self.next_signal(position)


    def block_contains_train(self, block):
        """
        input: block
        output: true if a train is in the block, false otherwise
        """
        for train in self.trains:
            if overlap(train.position, block.position):
                return True
        return False

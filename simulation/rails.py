import mesa

from positionalAgent import *
from position import *

class Rails:
    def __init__(self, model, length):
        self.model = model
        self.length = length
        self.trains = []
        self.blocks = []
    
    def add_train(self, train):
        self.trains.append(train)

    def add_block(self, block):
        self.blocks.append(block)

    def get_next_block(self, block):
        return self.blocks[self.blocks.index(block) + 1]

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

    def next_signal(self, train):
        """
        input: train
        output: next signal for the train
        """
        blocks_occupied = self.blocks_occupied_train(train)
        last_block = blocks_occupied[-1]
        next_block = self.get_next_block(last_block)
        signal = next_block.signal
        return signal

    def block_contains_train(self, block):
        """
        input: block
        output: true if a train is in the block, false otherwise
        """
        for train in self.trains:
            if overlap(train.position, block.position):
                return True
        return False
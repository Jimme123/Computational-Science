import mesa

from positionalAgent import *


def overlap(position_a , position_b):
    start_a, end_a = position_a.get_positions
    start_b, end_b = position_b.get_positions
    if start_a <= start_b <= end_a or\
                start_a <= end_b <= end_a or \
                (start_b <= start_a and end_a <= end_b):
        return True
    return False

class Rails:
    def __init__(self, model, length, blocks):
        self.model = model
        self.length = length
        self.trains = []
        self.blocks = []
    
    def add_train(self, train):
        self.train.append(train)

    def add_block(self, block):
        self.train.append(block)

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
        next_block = self.blocks[self.blocks.index(last_block) + 1]
        signal = next_block.get_signal
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
import mesa

from positionalAgent import *
from position import *
from block import *
from signallingControl import *

class StaticBlockSignalling(SignallingControl):
    def __init__(self, model, length):
        super().__init__(model, length)
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def get_next_block(self, block):
        index = (self.blocks.index(block) + 1) % len(self.blocks)
        return self.blocks[index]

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
    
    def block_head_train(self, train):
        start, end = train.position.bounds
        head = Position(end, end, self.length)

        for block in self.blocks:
            if overlap(block.position, head):
                return block
        return None

    def next_signal(self, train):
        """
        input: train
        output: next signal for the train
        """
        blocks_occupied = self.blocks_occupied_train(train)
        if self.blocks[0] in blocks_occupied and self.blocks[1]:
            last_block = self.blocks[0]
        else:
            last_block = blocks_occupied[-1]

        next_block = self.get_next_block(last_block)
        if next_block is None:
            return (Color.GREEN, 1000000)
        else:
            signal = next_block.signal
        distance = get_distance(train.position, next_block.position, self.length)
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
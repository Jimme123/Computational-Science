import mesa

import positionalAgent.py

class Rails:
    def __init__(self, model, length, blocks):
        self.model = model
        self.length = length
        self.trains = []
        self.blocks = blocks
    
    def add_train(self, train):
        self.train.append(train)

    def blocks_occupied_train(self, train):
        """
        input: train
        output: list of blocks where the train is
        """
        start_train, end_train = train.get_position
        blocks_occupied = []
        for block in self.blocks:
            start_block, end_block = block.get_position
            if start_train <= start_block <= end_train or start_train <= end_block <= end_train:
                blocks_occupied.append(block)
            elif start_block <= start_train and end_train <= end_block:
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
        start_block, end_block = block.get_position
        for train in self.trains:
            start_train, end_train = train.get_position
            if start_block <= start_train <= end_block or start_block <= end_train <= end_block:
                return True
            elif start_train <= start_block and end_block <= end_train:
                return True
        return False
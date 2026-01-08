import mesa
from enum import Enum

class Colour(Enum):
    GREEN = 1
    ORANGE = 2
    RED = 3

class Block(PositionalAgent):
    def __init__(self, model, position, rails):
        super().__init__(model, position)
        self.rails = rails

    def signal(self):
        """
        Returns signal colour based on train positions:
        - RED if train is in this block
        - ORANGE if next block is occupied
        - GREEN otherwise
        """
        if self.rails.block_contains_train(self):
            return Colour.RED
        elif self.rails.next_block_occupied(self):
            return Colour.ORANGE
        else:
            return Colour.GREEN

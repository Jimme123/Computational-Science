import mesa

from position import *

class PositionalAgent(mesa.Agent):
    def __init__(self, model, position):
        super().__init__(model)
        self.position = position


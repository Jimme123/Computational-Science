"""
A positional mesa agent
"""

import mesa

from simulation.position import *

class PositionalAgent(mesa.Agent):
    def __init__(self, model, position):
        super().__init__(model)
        self.position = position


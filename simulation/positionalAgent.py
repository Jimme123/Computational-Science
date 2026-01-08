import mesa

import position

class PositionalAgent(mesa.agents):
    def __init__(self, model, start, end):
        super().__init__(model)
        self.position = Position(start, end)

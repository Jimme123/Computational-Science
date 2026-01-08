import mesa

import position

class PositionalAgent(mesa.agents):
    def __init__(self, model, position):
        super().__init__(model)
        self.position = position

    def get_position(self):
        return (self.position.start, self.position.end)

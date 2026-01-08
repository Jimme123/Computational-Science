import mesa

import position

class PositionalAgent(mesa.Agent):
    def __init__(self, model, start, end):
        super().__init__(model)
        self.position = Position(start, end)
    
    def get_position(self):
        return (self.position.start, self.position.end)

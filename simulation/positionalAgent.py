import mesa

from position import *

class PositionalAgent(mesa.Agent):
    _id_counter = 0

    def __init__(self, model, position):
        self.unique_id = PositionalAgent._id_counter
        PositionalAgent._id_counter += 1

        super().__init__(self.unique_id, model)
        self.position = position

    def get_position(self):
        return (self.position.start, self.position.end)

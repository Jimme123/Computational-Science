import mesa

class Train(mesa.Agent):
    def __init__(self, model, rails):
        super().__init__(model)
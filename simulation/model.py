import mesa

import signal
import rails
import train

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length):
        super().__init__()
        self.rails = Rails(length)
        Trains = Train.create_agents(self, 2, rails)
        Signals = Signal.create_agents(self, 20, rails)
        

    def step(self):
        """Advance the model by one step."""
        self.Trains.shuffle_do("move")

import mesa

import signal
import rails
import train

class Railroad(mesa.Model):
    """The model containing the trains and signals."""

    def __init__(self, length):
        super().__init__()
        self.rails = Rails(10000)
        Trains = Train.create_agents(self, 2, rails, [0, 3000], [100, 3100], [200, 100])
        Signals = Signal.create_agents(self, 20, rails)
        

    def step(self):
        """Advance the model by one step."""
        self.Trains.shuffle_do("step")

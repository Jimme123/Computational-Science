import mesa

import signal
import rails
import train

class Railroad(mesa.Model):
    """A model with some number of agents."""

    def __init__(self):
        super().__init__()
        self.num_agents = n
        print("hi")

    def step(self):
        """Advance the model by one step."""
        self.agents.shuffle_do("move")
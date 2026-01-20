import numpy as np

from simulation.staticBlockSignalling import *
from simulation.model import *
from simulation.position import *

rail_length = 10000
model = Railroad(rail_length, StaticBlockSignalling, sight=100, dt=1, wait_time=10, verbose=True)

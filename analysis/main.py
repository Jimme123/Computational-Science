import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *

rail_length = 4000
model = generate_metro(verbose=False, signalling_type="static", sight=40)

test_capacity(model, train_specification=metro_specifications, verbose=True, min_trains=1, max_trains=20)

add_trains(model, 15, metro_specifications)
visualize(model, 1500)

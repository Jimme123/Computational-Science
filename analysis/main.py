import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *

model = generate_metro(signalling_type="moving", verbose=False, block_size=250)


print(test_capacity(model, metro_specifications, min_trains=1, max_trains=30, verbose=True))
add_trains(model, 10, metro_specifications)

for i in range(3000):
    model.step()

visualize(model, 1000)

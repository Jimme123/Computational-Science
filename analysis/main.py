import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *
from generateModel import *

model = generate_model(distances_variation=1)
# print(test_capacity(model, metro_specifications, max_trains=30, verbose=True))

for i in range(3000):
    model.step()

#visualize(model, 1000)

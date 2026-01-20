import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *
from generateModel import *

model = generate_model(signalling_type="moving", 
                       distances_variation=1, 
                       acc_dist=[0.25, 0.5, 0.25], 
                       braking_dist=[0.25, 0.5, 0.25])
# print(test_capacity(model, metro_specifications, max_trains=30, verbose=True))

for i in range(3000):
    model.step()

visualize(model, 1000)

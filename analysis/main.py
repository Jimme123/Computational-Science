import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *

rail_length = 1000
train_length = 100
train_args = [25, 1.3, 1.1]
model = Railroad(rail_length, MovingBlockSignalling, 300, 1, 10, False)

# n, cap = test_capacity(model, train_length, train_args, max_trains=8)
# print(n, cap)

add_trains(model, rail_length, 8, train_length, train_args)
visualize(model, 300)

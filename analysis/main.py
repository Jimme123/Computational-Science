import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *

rail_length = 2000
train_length = 100
train_args = [20, 1.5, 1.5]
model = Railroad(rail_length, StaticBlockSignalling, 300, 1, 10, True)

n = 8
positions = np.linspace(0, rail_length, n + 1)
stations = [2, 4]
for i in range(n):
    if i in stations:
        model.add_station(Position(positions[i], positions[i]+10, rail_length))
        model.add_block(Position(positions[i]+10, positions[i+1], rail_length))
    else:
        model.add_block(Position(positions[i], positions[i+1], rail_length))

result = test_capacity(model, train_length, train_args, max_trains=4)
print(result)


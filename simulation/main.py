import numpy as np

from model import *
from staticBlockSignalling import *
from movingBlockSignalling import *
from position import *

rail_length = 12000
model = Railroad(rail_length, StaticBlockSignalling)
model.add_train(Position(0, 100), 55, 1.3, 1.1)
model.add_train(Position(3000, 3100), 25, 1.3, 1.1)
n = 8
positions = np.linspace(0, rail_length, n + 1)
stations = [2, 4]
for i in range(n):
    if i in stations:
        model.add_station(Position(positions[i], positions[i]+10))
        model.add_block(Position(positions[i]+10, positions[i+1]))
    else:
        model.add_block(Position(positions[i], positions[i+1]))

for i in range(400):
    model.step()
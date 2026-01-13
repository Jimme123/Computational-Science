import numpy as np

from model import *
from staticBlockSignalling import *
from position import *

length = 10500
railroad = Railroad(length, StaticBlockSignalling)
railroad.add_train(Position(0, 100), 55, 1.3, 1.1)
railroad.add_train(Position(3000, 3100), 25, 1.3, 1.1)
n = 7
positions = np.linspace(0, length, n + 1)
stations = [2, 6]
for i in range(n):
    if i in stations:
        railroad.add_station(Position(positions[i], positions[i]+1))
        railroad.add_block(Position(positions[i]+1, positions[i+1]))
    else:
        railroad.add_block(Position(positions[i], positions[i+1]))

for i in range(400):
    railroad.step()
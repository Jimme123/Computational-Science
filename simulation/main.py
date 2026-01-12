from model import *
from staticBlockSignalling import *
from position import *

length = 10000
railroad = Railroad(length, StaticBlockSignalling)
railroad.add_train(Position(0, 100), 55, 1.3, -1.1)
railroad.add_train(Position(3000, 3100), 25, 1.3, -1.1)
n = 5
for i in range(n):
    railroad.add_block(Position(i * length / n, (i + 1) * length / n))

for i in range(500):
    railroad.step()
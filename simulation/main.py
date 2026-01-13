from model import *
from staticBlockSignalling import *
from position import *

length = 10500
railroad = Railroad(length, StaticBlockSignalling)
railroad.add_train(Position(3000, 3100, length), 25, 1.3, -1.1)
railroad.add_train(Position(0, 100, length), 55, 1.3, -1.1)
n = 7
for i in range(n):
    railroad.add_block(Position(i * length / n, (i + 1) * length / n, length))

for i in range(300):
    railroad.step()
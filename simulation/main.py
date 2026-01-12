from model import *
from blockSignalling import *

railroad = Railroad(10000, BlockSignalling)
for i in range(500):
    railroad.step()
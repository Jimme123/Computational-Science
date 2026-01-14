from simulation.model import Railroad
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

rail_length = 3000
signalling_class = StaticBlockSignalling
sight = 300
dt = 1
wait_time = 10
model = Railroad(rail_length, signalling_class, sight, dt, wait_time)
metro_length = 108.68
metro_specifications = (19.4444444, 1.27, 1.35)
block_size = 200  # 156

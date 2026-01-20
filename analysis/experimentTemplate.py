from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from generateModel import *

sight = math.inf
dt=1
wait_time=40
verbose=False
block_size=1500
rail_length=15000
num_stations=5
station_size=15
min_station_distance=1515
distances_variation=0
num_trains=5
train_specifications=[sng_specifications]
train_distribution=[1]


static_model = generate_model("static", sight, dt, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, num_trains,
                                train_specifications, train_distribution, True)

moving_model = generate_model("moving", sight, dt, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, num_trains,
                                train_specifications, train_distribution, True)

print(test_capacity(static_model, max_trains=30, verbose=True))
print(test_capacity(moving_model, max_trains=30, verbose=True))

visualize(static_model, 500, "Static Block Circular Railway Simulation")
visualize(moving_model, 500, "Moving Block Circular Railway Simulation")

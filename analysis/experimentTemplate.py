from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from generateModel import *

sight = math.inf
wait_time=40
verbose=False
block_size=900
rail_length=10000
num_stations=5
station_size=0
min_station_distance=block_size+station_size
distances_variation=1
train_specifications=[sng_specifications]
train_distribution=[1]
repetitions = 10


static_model = generate_model("static", sight, 1, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, 0,
                                train_specifications, train_distribution, False,
                                False)

moving_model = generate_model("moving", sight, 1, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, 0,
                                train_specifications, train_distribution, False,
                                False)

test_capacity_distances_and_trains([static_model, moving_model], num_stations, station_size, block_size, rail_length, min_station_distance, distances_variation, repetitions,
                                   trains=train_specifications, train_distribution=train_distribution, max_trains=7, min_trains=5))


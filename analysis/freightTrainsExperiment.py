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
block_size=1150
rail_length=6000
num_stations=0
station_size=0
min_station_distance=block_size+station_size
distances_variation=0
train_specifications=[freight_train_specifications]
train_distribution=[1]
repetitions = 1
min_trains = 1
max_trains = 6


static_model = generate_model("static", sight, 1, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, 0,
                                train_specifications, train_distribution, False,
                                True)

moving_model = generate_model("moving", sight, 1, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, 0,
                                train_specifications, train_distribution, False,
                                True)

result = test_capacity_trains([static_model, moving_model], train_specifications,
                              train_distribution, min_trains=min_trains,
                              max_trains=max_trains, repetitions=repetitions)


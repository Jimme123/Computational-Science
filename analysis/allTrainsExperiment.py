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
rail_length=20000
num_stations=0
station_size=0
min_station_distance=block_size+station_size
distances_variation=0
train_specifications=[sng_specifications,virm_specifications, freight_train_specifications]
train_distribution=[0.4, 0.4, 0.2]
repetitions = 10
min_trains = 1
max_trains = 35


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

result_wide = test_capacity_trains([static_model, moving_model], train_specifications,
                              train_distribution, min_trains=min_trains,
                              max_trains=max_trains, repetitions=1)

max_trains_static = max(result_wide, key=lambda x: x[1][0][0])[0]
max_trains_moving = max(result_wide, key=lambda x: x[1][0][1])[0]

result_static = test_capacity_trains([static_model], train_specifications,
                              train_distribution, min_trains=max_trains_static-1,
                              max_trains=max_trains_static+1, repetitions=repetitions)

result_moving = test_capacity_trains([moving_model], train_specifications,
                              train_distribution, min_trains=max_trains_moving-1,
                              max_trains=max_trains_moving+1, repetitions=repetitions)

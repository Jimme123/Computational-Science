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
block_size=1500
rail_length=15000
num_stations=5
station_size=300
min_station_distance=1815
distances_variation=0
train_specifications=[sng_specifications]
train_distribution=[1]


static_model = generate_model("static", sight, 1, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, 0,
                                train_specifications, train_distribution, True)

moving_model = generate_model("moving", sight, 1, wait_time, verbose, block_size,
                                rail_length, num_stations, station_size,
                                min_station_distance, distances_variation, 0,
                                train_specifications, train_distribution, True)

test_capacity([static_model, moving_model], trains=train_specifications, train_distribution=train_distribution,
                     max_trains=30,verbose=True)


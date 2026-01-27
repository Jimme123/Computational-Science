from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from simulation.tools import *
from simulation.visualize import *
from simulation.generateModel import *

from trainSpecifications import *

sight = math.inf
dt = 1
wait_time=180
verbose=True
block_size=1000
rail_length=3500
num_stations=1
station_size_static=0
station_size_moving=250
station_size = 0
min_station_distance=1815
distances_variation=0
num_trains=2
train_specifications=[sng_specifications]
train_distribution=[1]

trains=False
blocks=True

for signalling_type in ["static", "moving"]:
    if signalling_type == "static":
        station_size = station_size_static
    else:
        station_size = station_size_moving

    model = generate_model(signalling_type, sight, dt, wait_time, verbose, block_size,
                                    rail_length, num_stations, station_size,
                                    min_station_distance, distances_variation, num_trains,
                                    train_specifications, train_distribution, trains,
                                    blocks)
    add_trains(model, [sng_specifications]*2)

    for i in range(2000):
        model.step()

    visualize(model, 500, f"{signalling_type} demonstration")

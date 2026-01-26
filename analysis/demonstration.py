from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from generateModel import *

sight = math.inf
wait_time=180
verbose=True
block_size=1000
rail_length=3500
num_stations=1
station_size=0
min_station_distance=1815
distances_variation=0

for signalling_type in ["static", "moving"]:
    model = generate_model(signalling_type, sight, 1, wait_time, verbose, block_size,
                                    rail_length, num_stations, station_size,
                                    min_station_distance, distances_variation, trains=False)
    add_trains(model, [sng_specifications]*2)

    for i in range(2000):
        model.step()

    visualize(model, 500, f"{signalling_type} demonstration")

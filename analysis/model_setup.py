import numpy as np

from simulation.model import Railroad
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *


def blocks_from_distances(model, rail_length, distances, station_size, block_size, signalling_type = "static"):
    """
    Takes the distances between stations and other variables to get stations and blocks in model
    """
    # translate distances between stations into positions on line
    positions = [0]
    for distance in distances:
        last_value = positions[-1]
        positions.append(last_value + distance)

    # loop over all positions
    for i in range(len(positions) - 1):
        model.add_station(Position(positions[i], positions[i] + station_size, rail_length))
        if signalling_type == "static":
            # calculate distance between this station and next station
            distance = distances[i] - station_size
            quotient = distance // block_size
            current_distance = positions[i] + station_size
            # get spacing for the blocks with minimum block_size
            block_spacing = np.linspace(current_distance, current_distance + distance, quotient + 1)
            #add the blocks
            for j in range(quotient):
                if block_spacing[j + 1] == rail_length:  # alter last block 
                    model.add_block(Position(block_spacing[j], 0, rail_length))
                else:
                    model.add_block(Position(block_spacing[j], block_spacing[j + 1], rail_length))
                



signalling_class = StaticBlockSignalling
signalling_type = "static"

#signalling_class = MovingBlockSignalling
#signalling_type = "moving"

rail_length = 9600
sight = 50
dt = 1
wait_time = 40
model = Railroad(rail_length, signalling_class, sight=sight, dt=dt, wait_time=wait_time, verbose=False)
metro_length = 108.68
metro_specifications = (19.4444444, 1.27, 1.35)
block_size = 500  # 156
station_size = 15
distances_east = [2000, 700, 500, 500, 1100]
distances_west = distances_east[::-1]

distances = distances_east + distances_west

blocks_from_distances(model, rail_length, distances, station_size, block_size, signalling_type)
for block in model.signalling_control.blocks:
    print(block)



# add_trains(model, rail_length, 20, metro_length, metro_specifications)

print(test_capacity(model, metro_length, metro_specifications, max_trains=30, verbose=True))


import numpy as np
import math

from simulation.model import Railroad
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *
from simulation.train import *

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
        model.add_block(Position(positions[i], positions[i] + 150, rail_length), 40/3.6)
        model.add_station(Position(positions[i] + 150, positions[i] + 150 + station_size, rail_length))
        if signalling_type == "static":
            # calculate distance between this station and next station
            distance = distances[i] - station_size - 150
            quotient = distance // block_size
            current_distance = positions[i] + station_size + 150
            if quotient == 0:
                model.add_block(Position(current_distance, current_distance + distance, rail_length))
            # get spacing for the blocks with minimum block_size
            block_spacing = np.linspace(current_distance, current_distance + distance, quotient + 1)
            #add the blocks
            for j in range(quotient):
                if block_spacing[j + 1] == rail_length:  # alter last block
                    model.add_block(Position(block_spacing[j], 0, rail_length))
                else:
                    model.add_block(Position(block_spacing[j], block_spacing[j + 1], rail_length))



def generate_metro(signalling_type="static",
                    sight=math.inf,
                    dt=1,
                    wait_time=30,
                    verbose=False,
                    block_size=500,
                    station_size=15):

    if signalling_type == "static":
        signalling_class = StaticBlockSignalling
    elif signalling_type == "moving":
        signalling_class = MovingBlockSignalling
    else:
        raise ValueError(f"unknown signalling type {signalling_type}")

    rail_length = 9600

    model = Railroad(rail_length, signalling_class, sight=sight, dt=dt, wait_time=wait_time, verbose=verbose)

    block_size = 500  # 156
    station_size = 15
    distances_east = [2000, 700, 500, 500, 1100]
    distances_west = distances_east[::-1]

    distances = distances_east + distances_west

    blocks_from_distances(model, rail_length, distances, station_size, block_size, signalling_type)

    return model

metro_specifications = TrainSpecifications(
    max_speed=19.4,
    max_acceleration=1.27,
    max_braking=1.35,
    max_power=1.68*2*10**6,
    weight=141.5*1000*2,
    length=108.68
    )

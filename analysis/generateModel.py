import math

from simulation.model import Railroad
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from tools import *


def generate_model(signalling_type="static",
                    sight=math.inf,
                    dt=1,
                    wait_time=40,
                    verbose=False,
                    block_size=500,
                    rail_length=10000,
                    num_stations=10,
                    station_size=15,
                    min_station_distance=515,
                    distances_variation=0):
                    
    if signalling_type == "static":
        signalling_class = StaticBlockSignalling
    elif signalling_type == "moving":
        signalling_class = MovingBlockSignalling
    else:
        raise ValueError(f"unknown signalling type {signalling_type}")
    
    model = Railroad(rail_length, signalling_class, sight=sight, dt=dt, wait_time=wait_time, verbose=False)
    distances = get_distances(num_stations, station_size, block_size, rail_length, min_station_distance, distances_variation)
    blocks_from_distances(model, rail_length, distances, station_size, block_size, signalling_type)
    #add trains

    return model

import numpy as np
import math

from simulation.model import Railroad
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *
from simulation.train import *

from simulation.tools import *
from simulation.visualize import *


def generate_metro(signalling_type="static",
                    sight=math.inf,
                    dt=1,
                    wait_time=30,
                    verbose=False,
                    block_size=500,
                    station_size=150):

    if signalling_type == "static":
        signalling_class = StaticBlockSignalling
    elif signalling_type == "moving":
        signalling_class = MovingBlockSignalling
    else:
        raise ValueError(f"unknown signalling type {signalling_type}")

    rail_length = 9600

    model = Railroad(rail_length, signalling_class, sight=sight, dt=dt, wait_time=wait_time, verbose=verbose)

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

import math

from simulation.model import Railroad
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from tools import *
from trainSpecifications import *


def generate_model(signalling_type="static",
                    sight=math.inf,
                    dt=1,
                    wait_time=40,
                    verbose=False,
                    block_size=1500,
                    rail_length=15000,
                    num_stations=5,
                    station_size=15,
                    min_station_distance=1515,
                    distances_variation=0,
                    num_trains=5,
                    train_specifications=[sng_specifications],
                    train_distribution=[1]
                    ):
    # make sure the distance between stations is greater then the braking distance at max speed 

    if braking_dist[0] > 0:
        assert(min_station_distance > (train_specifications['max_speed']**2) / (2 * 0.9 * (train_specifications['max_braking'] - dif_braking)))
    if braking_dist[1] > 0:
        assert(min_station_distance > (train_specifications['max_speed']**2) / (2 * 0.9 * (train_specifications['max_braking'])))
    if braking_dist[2] > 0:
        assert(min_station_distance > (train_specifications['max_speed']**2) / (2 * 0.9 * (train_specifications['max_braking'] + dif_braking)))

    if signalling_type == "static":
        signalling_class = StaticBlockSignalling
    elif signalling_type == "moving":
        signalling_class = MovingBlockSignalling
    else:
        raise ValueError(f"unknown signalling type {signalling_type}")
    
    model = Railroad(rail_length, signalling_class, sight=sight, dt=dt, wait_time=wait_time, verbose=False)
    distances = get_distances(num_stations, station_size, block_size, rail_length, min_station_distance, distances_variation)
    blocks_from_distances(model, rail_length, distances, station_size, block_size, signalling_type)
    
    
    trains = get_trains(num_trains, train_specifications, train_distribution)
    add_trains(model, trains)

    return model

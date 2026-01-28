from simulation.generateModel import *
from simulation.tools import *
from trainSpecifications import sng_specifications
from simulation.visualize import *

def run_experiment(
    sight = math.inf,
    dt=1,
    wait_time=40,
    verbose=False,
    block_size=1150,
    rail_length=20000,
    num_stations=5,
    station_size_static=0,
    station_size_moving=250,
    min_station_distance=None,
    distances_variation=0,
    train_specifications=[sng_specifications],
    train_distribution=[1],
    repetitions = 10,
    min_trains = 1,
    max_trains = 35,
    run_repetitions=True,
    run_moving=True,
    run_static=True,
):
    if min_station_distance is None:
        min_station_distance = block_size + max(station_size_static, station_size_moving)

    models = []
    if run_static:
        models.append(generate_model("static", sight, dt, wait_time, verbose, block_size,
                                    rail_length, num_stations, station_size_static,
                                    min_station_distance, distances_variation, 0,
                                    train_specifications, train_distribution, False,
                                    True))
    if run_moving:
        models.append(generate_model("moving", sight, dt, wait_time, verbose, block_size,
                                        rail_length, num_stations, station_size_moving,
                                        min_station_distance, distances_variation, 0,
                                        train_specifications, train_distribution, False,
                                        True))

    result_wide = test_capacity_trains(models, train_specifications,
                                train_distribution, min_trains=min_trains,
                                max_trains=max_trains, repetitions=1)

    if run_repetitions:
        assert(run_moving and run_static)
        max_trains_static = max(result_wide, key=lambda x: x[1][0][0])[0]
        max_trains_moving = max(result_wide, key=lambda x: x[1][0][1])[0]

        result_static = test_capacity_trains(models[0:1], train_specifications,
                                    train_distribution, min_trains=max_trains_static-1,
                                    max_trains=max_trains_static+1, repetitions=repetitions)

        result_moving = test_capacity_trains(models[1:2], train_specifications,
                                    train_distribution, min_trains=max_trains_moving-1,
                                    max_trains=max_trains_moving+1, repetitions=repetitions)

        return result_wide, result_static, result_moving
    else:
        return result_wide

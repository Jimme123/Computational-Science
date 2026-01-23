import copy
import numpy as np
from scipy.stats import dirichlet

from simulation.position import *
from simulation.model import *
from simulation.block import *
from trainSpecifications import *

def add_trains(model, train_specifications):
    length = model.signalling_control.length
    n = len(train_specifications)

    if model.type == "moving":
        max_train_length = max(train_specifications, key=lambda x:x['length'])['length']
        if length / n <= max_train_length:
            return False

        starts = np.linspace(0, length, n, False)
        for i in range(n):
            model.add_train(Position(starts[i], starts[i] + train_specifications[i]['length'], length), train_specifications[i])

    else:
        blocks = model.signalling_control.blocks
        i = n
        for block in blocks:
            if block.signal.is_station:
                continue
            # If the block is to small for the train continue
            if train_specifications[i - 1]["length"] > block.position.length > 0:
                continue

            start = block.position.bounds[0] + 1
            model.add_train(Position(start, start + train_specifications[i - 1]['length'], length), train_specifications[i - 1])
            i -= 1
            if i == 0:
                break
        if i > 0:
            return False

    return True


def get_trains(number_trains, train_specifications, train_distribution):
    """
    train_specifications: list of different trainSpecifications
    train_distribution: the distribution with which the trains should be chosen

    returns a list with train_specifications
    """
    assert(sum(train_distribution) == 1)
    assert(len(train_specifications) == len(train_distribution))

    trains = []
    for i in range(number_trains):
        cur_train_specs = train_specifications[np.random.choice(range(len(train_specifications)), p=train_distribution)].copy()
        trains.append(cur_train_specs)

    return trains


def get_distances(number_stations, station_size, block_size, rail_length, min_distance, variation):
    """
    Determines distances between stations that sum to the rail_length. takes min_distance into consideration

    variation: float between 0 and 1 where 0 is no randomness and 1 is total randomness
    """
    assert(min_distance >= block_size + station_size)
    assert(number_stations < (rail_length - number_stations * station_size) / block_size)
    assert(0 <= variation <= 1)

    if number_stations == 0:
        return []

    # determine equally split distances
    distance = rail_length / number_stations
    equal_distances = [distance for i in range(number_stations)]

    # random distances with minimum distances
    min_distances = [min_distance for i in range(number_stations)]
    remaining_length = rail_length - number_stations * min_distance
    rand_distances = dirichlet.rvs(np.ones(number_stations), size=1) * remaining_length

    # total random distances
    total_rand_distances = min_distances + rand_distances[0]

    # distances is weighted average between equal distances and random distances
    distances = [(1 - variation) * a + variation * b for a, b in zip(equal_distances, total_rand_distances)]


    assert(rail_length - 1 <= sum(distances) <= rail_length + 1)

    return distances


def blocks_from_distances(model, rail_length, distances, station_size, block_size, signalling_type = "static"):
    """
    Takes the distances between stations and other variables to get stations and blocks in model
    """

    if len(distances) == 0:
        if signalling_type == "static":
            quotient = int(rail_length // block_size)
            block_spacing = np.linspace(0, rail_length, quotient + 1)
            for j in range(quotient):
                if block_spacing[j + 1] == rail_length:  # alter last block
                    model.add_block(Position(block_spacing[j], 0, rail_length))
                else:
                    model.add_block(Position(block_spacing[j], block_spacing[j + 1], rail_length))
        return

    # translate distances between stations into positions on line
    positions = [0]
    for distance in distances:
        last_value = positions[-1]
        positions.append(last_value + distance)

    # loop over all positions
    for i in range(len(positions) - 1):
        if station_size > 0:
            model.add_block(Position(positions[i], positions[i] + station_size, rail_length), 40/3.6)
        model.add_station(Position(positions[i] + station_size, positions[i] + station_size + 1, rail_length))
        if signalling_type == "static":
            # calculate distance between this station and next station
            distance = distances[i] - station_size - 1
            quotient = int(distance // block_size)
            current_distance = positions[i] + station_size + 1
            if quotient == 0:
                model.add_block(Position(current_distance, current_distance + distance, rail_length))
            # get spacing for the blocks with minimum block_size
            block_spacing = np.linspace(current_distance, current_distance + distance, quotient + 1)
            #add the blocks
            for j in range(quotient):
                if block_spacing[j + 1] >= rail_length:  # alter last block
                    model.add_block(Position(block_spacing[j], 0, rail_length))
                else:
                    model.add_block(Position(block_spacing[j], block_spacing[j + 1], rail_length))


def test_capacity_distances_and_trains(empty_models: [Railroad], num_stations, station_size, block_size, rail_length,
                                       min_station_distance, distances_variation, repetitions, trains, train_distribution, max_trains, min_trains):
    """
    Tests the capacity of a trainless and blockless model by varying over the distances
    """
    result = []
    for i in range(repetitions):
        distances = get_distances(num_stations, station_size, block_size, rail_length,
                                       min_station_distance, distances_variation)
        models = []
        for empty_model in empty_models:
            model: Railroad = copy.deepcopy(empty_model)
            blocks_from_distances(model, rail_length, distances, station_size, block_size, model.type)
            models.append(model)
        capacities = test_capacity_trains(models, trains, train_distribution, max_trains=max_trains, min_trains=min_trains, verbose=True, repetitions=1)
        result.append([i, capacities])
    return result


def test_capacity_trains(trainless_models: [Railroad], trains=[sng_specifications], train_distribution=[1], wind_up=600, test_length=3600, min_trains=1, max_trains=5, repetitions=10, verbose=False):
    """
    Tests the capacity of a trainless model when given a set of trains and their distribution

    Returns a list of lists, the lists in the list are of the form [n, capacities] where n
    is the number of trains and capacities is a list of tuples with the capacity of the different
    trainless_models
    """
    n = 1
    result = []

    for n in range(min_trains, max_trains + 1):
        capacities = []
        for _ in range(repetitions):
            trains_specifications = get_trains(n, trains, train_distribution)
            capacity_both = []
            for trainless_model in trainless_models:
                model: Railroad = copy.deepcopy(trainless_model)
                # Add n trains to the model
                if add_trains(model, trains_specifications) == False:
                    capacity_both.append(0)
                    continue

                for i in range(wind_up // model.dt):
                    model.step()

                passes = 0
                check = Position(0, 1, model.signalling_control.length)
                was_occupied = model.signalling_control.position_contains_train(check)
                for i in range(test_length // model.dt):
                    model.step()
                    occupied = model.signalling_control.position_contains_train(check)
                    if occupied and not was_occupied:
                        passes += 1
                    was_occupied = occupied

                capacity = float(passes) / (float(test_length)) * 60**2
                capacity_both.append(capacity)
            capacities.append(capacity_both)
        result.append([n, capacities])
        if verbose:
            print(f"for {n}, capacity is {capacities}")
    return result


def measure_station_travel_times_real_time(model, metro_specifications, max_steps=20000):
    train = model.trains[0]

    dt = metro_specifications.get("dt", 1.0)

    blocks = model.signalling_control.blocks
    stations = [b for b in blocks if b.signal == Color.STATION]
    stations.sort(key=lambda b: b.position.start)

    station_indices = {id(s): i for i, s in enumerate(stations)}

    last_station_id = None
    last_time = None
    travel_times = []

    for step in range(max_steps):
        model.step()
        pos = train.position.bounds[1]

        for station in stations:
            if station.position.start <= pos <= station.position.end:
                sid = id(station)

                if last_station_id is None:
                    last_station_id = sid
                    last_time = step
                    break

                if sid != last_station_id:
                    steps_taken = step - last_time
                    time_seconds = steps_taken * dt

                    travel_times.append(time_seconds)

                    print(
                        f"Van station {station_indices[last_station_id]} "
                        f"naar station {station_indices[sid]}: "
                        f"{time_seconds:.1f} s"
                    )

                    last_station_id = sid
                    last_time = step

                    if len(travel_times) >= len(stations):
                        return travel_times
                break

    return travel_times

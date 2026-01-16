import copy
import numpy as np
from scipy.stats import dirichlet

from simulation.position import *
from simulation.model import *
from simulation.block import *

epsilon = 1

def add_trains(model, n, train_specification):
    length = model.signalling_control.length
    train_length = train_specification['length']

    if model.type == "moving":
        starts = np.linspace(0, length, n, False)
        starts = starts[::-1]
        for i in range(n):
            model.add_train(Position(starts[i], starts[i] + train_length, length), train_specification)

    else:
        blocks = model.signalling_control.blocks
        i = n
        for block in blocks:
            if block.signal == Color.STATION:
                continue
            start = block.position.bounds[0] + 1
            model.add_train(Position(start, start + train_length, length), train_specification)
            i -= 1
            if i == 0:
                break
        if i > 0:
            return False

    return True

def get_trains(number_trains, standard_specifications, dif_acc=0.5, dif_braking=0.5, acc_dist=[0, 1, 0], braking_dist=[0, 1, 0]):
    """
    standard_specifications: the train specifications on which the random trains are based
    dif_acc: difference in acceleration
    dif_braking: difference in brake
    acc_dist: the distribution of lower, normal or higher acceleration in a list
    braking_dist: the distribution of lower, normal or higher braking in a list

    returns a list with different train_specifications
    """
    assert(sum(acc_dist) == 1)
    assert(sum(braking_dist) == 1)

    trains = []
    for i in range(number_trains):
        cur_train_specs = standard_specifications.copy()
        # alter max_acceleration based on acceleration distribution
        cur_train_specs["max_acceleration"] += np.random.choice([-dif_acc, 0, dif_acc], p=acc_dist)
        # alter max_braking based on braking distribution
        cur_train_specs["max_braking"] += np.random.choice([-dif_braking, 0, dif_braking], p=braking_dist)
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
    
    # determine equally split distances
    distance = rail_length / number_stations
    equal_distances = [distance for i in range(number_stations)]

    # random distances with minimum distances
    min_distances = [min_distance for i in range(number_stations)]
    remaining_length = rail_length - number_stations * min_distance
    rand_distances = dirichlet.rvs(np.ones(number_stations), size=1) * remaining_length

    # total random distances
    total_rand_distances = min_distances + rand_distances

    # distances is weighted average between equal distances and random distances
    distances = (1 - variation) * equal_distances + variation * total_rand_distances

    assert(rail_length - 1 <= sum(distances) <= rail_length + 1)

    return distances


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


def test_capacity(trainless_model: Railroad, train_specification, wind_up=600, test_length=3600, min_trains=1, max_trains=5, verbose=False):
    n = 1
    length = trainless_model.signalling_control.length
    result = []

    for n in range(min_trains, max_trains + 1):
        model: Railroad = copy.deepcopy(trainless_model)
        # Add n trains to the model
        if add_trains(model, n, train_specification) == False:
            break

        for i in range(wind_up):
            model.step()

        passes = 0
        was_occupied = model.signalling_control.block_contains_train(model.signalling_control.blocks[0])
        for i in range(test_length):
            model.step()
            occupied = model.signalling_control.block_contains_train(model.signalling_control.blocks[0])
            if occupied and not was_occupied:
                passes += 1
            was_occupied = occupied

        capacity = float(passes) / float(test_length) * 60**2
        result.append([n, capacity])
        if verbose:
            print(f"for {n}, capacity is {capacity:.1f}")
    return np.array(result)

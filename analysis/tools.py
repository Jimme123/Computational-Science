import copy
import numpy as np

from simulation.position import *
from simulation.model import *
from simulation.block import *

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

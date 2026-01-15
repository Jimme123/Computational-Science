import copy
import numpy as np

from simulation.position import *
from simulation.model import *

def add_trains(model, length, n, train_length, train_args):
    starts = np.linspace(0, length, n + 1, False)
    starts = starts[::-1]
    for i in range(n):
        model.add_train(Position(starts[i], starts[i] + train_length, length), *train_args)

def test_capacity(trainless_model: Railroad, train_length, train_args, wind_up=600, test_length=3600, min_trains=1, max_trains=5, verbose=False):
    n = 1
    length = trainless_model.signalling_control.length
    result = []

    for n in range(min_trains, max_trains + 1):
        model: Railroad = copy.deepcopy(trainless_model)
        # Add n trains to the model
        add_trains(model, length, n, train_length, train_args)

        for i in range(wind_up):
            model.step()

        passes = 0
        check = Position(0, 1, length)
        was_occupied = model.train_in_area(check)
        for i in range(test_length):
            model.step()
            occupied = model.train_in_area(check)
            if occupied and not was_occupied:
                passes += 1

        capacity = passes / test_length * 60**2
        result.append([n, capacity])
    return np.array(result)

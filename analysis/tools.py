import copy
import numpy as np

from simulation.position import *
from simulation.model import *

def add_trains(model, length, n, train_length, train_args):
    starts = np.linspace(0, length, n + 1, False)
    starts = starts[::-1]
    for i in range(n):
        model.add_train(Position(starts[i], starts[i] + train_length, length), *train_args)

def test_capacity(empty_model: Railroad, train_length, train_args, visualize=False, wind_up=600, test_length=3600, min_trains=0, max_trains=100000):
    n = 1
    length = empty_model.signalling_control.length
    max_capacity = 0
    max_n = 0

    for n in range(min_trains, max_trains):
        model: Railroad = copy.deepcopy(empty_model)
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
        if capacity > max_capacity:
            max_capacity = capacity
            max_n = n
    return (max_n, max_capacity)

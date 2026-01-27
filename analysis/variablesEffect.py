import math
import copy
from trainSpecifications import *
from runExperiment import *

import json

experiment_definitions_model = {
    "sight": [
        {"sight": 40,
         "run_moving": False},
        {"sight": 100,
         "run_moving": False},
        {"sight": 200,
         "run_moving": False},
        {"sight": 300,
         "run_moving": False},
        {"sight": math.inf,
         "run_moving": False}
    ],

    "sight_no_station": [
        {"sight": 40,
         "num_stations": 0,
         "run_moving": False},
        {"sight": 100,
         "num_stations": 0,
         "run_moving": False},
        {"sight": 200,
         "num_stations": 0,
         "run_moving": False},
        {"sight": 300,
         "num_stations": 0,
         "run_moving": False},
        {"sight": math.inf,
         "num_stations": 0,
         "run_moving": False}
    ],

    "num_stations": [
        {"num_stations": 0},
        {"num_stations": 2},
        {"num_stations": 5},
        {"num_stations": 10},
        {"num_stations": 15}
    ],

    "block_size": [
        {"block_size": 3900/5,
         "run_moving": False},
        {"block_size": 3900/4,
         "run_moving": False},
        {"block_size": 3900/3,
         "run_moving": False},
        {"block_size": 3900/2,
         "run_moving": False},
        {"block_size": 3900,
         "run_moving": False}
    ],

    "dt": [
        {"dt": 0.1},
        {"dt": 1},
        {"dt": 2}
    ]
}

experiment_definitions_train = {
    "max_acceleration": [0.7, 1, 1.3, 1.6, 1.9],
    "max_braking": [0.7, 0.9, 1.1, 1.3, 1.5],
    "max_speed": [10, 20, 30, 40, 50]
}


experiment_results = {}

for variable_name, options in experiment_definitions_model.items():  # options is list of dicts
    result = {}
    for option in options:  # option is dict
        print(f"Running {option}")
        wide = run_experiment(**option, run_repetitions=False)
        result[option[variable_name]] = wide
    experiment_results[variable_name] = result
    fp = open("results/result_variables.json", "w")
    json.dump(experiment_results, fp)
    fp.close()


for variable_name, options in experiment_definitions_train.items():  # options is a list of ints
    result = {}
    train = copy.deepcopy(sng_specifications)
    for option in options:
        print(f"Running {option}")
        train[variable_name] = option
        wide = run_experiment(train_specifications=[train], run_repetitions=False)
        result[option] = wide
    experiment_results[variable_name] = result
    fp = open("results/result_variables.json", "w")
    json.dump(experiment_results, fp)
    fp.close()
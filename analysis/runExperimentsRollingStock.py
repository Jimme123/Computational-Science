from trainSpecifications import *
from runExperiment import *

import json

experiment_definitions = {
    "all mixed": {
        "num_stations": 0,
        "train_specifications": [sng_specifications,virm_specifications, freight_train_specifications],
        "train_distribution": [0.4, 0.4, 0.2]
    },
    "freight": {
        "num_stations": 0,
        "train_specifications": [freight_train_specifications],
        "train_distribution": [1]
    },
    "intercity": {
        "num_stations": 5,
        "train_specifications": [virm_specifications],
        "train_distribution": [1]
    },
    "IC and SPR": {
        "num_stations": 5,
        "train_specifications": [virm_specifications, sng_specifications],
        "train_distribution": [0.5, 0.5]
    },
    "sprinter": {
        "num_stations": 5,
        "train_specifications": [sng_specifications],
        "train_distribution": [1]
    }
}

experiment_results = {}

for key, value in experiment_definitions.items():
    print(f"running {key}")
    wide, static, moving = run_experiment(**value)
    experiment_results[key] = {"wide": wide, "static": static, "moving": moving}

fp = open("rollingstock_result.json", "w")
json.dump(experiment_results, fp)
fp.close()

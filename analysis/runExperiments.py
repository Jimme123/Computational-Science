import json

import allTrainsExperiment
print("1")
import freightTrainsExperiment
print("2")
import intercityExperiment
print("3")
import passengerTrainExperiment
print("4")
import sprinterExperiment
print("5")

experiment_results = {
    "all mixed": {"wide": allTrainsExperiment.result_wide, "static": allTrainsExperiment.result_static, "moving": allTrainsExperiment.result_moving},
    "freight": {"wide": freightTrainsExperiment.result_wide, "static": freightTrainsExperiment.result_static, "moving": freightTrainsExperiment.result_moving},
    "intercity": {"wide": intercityExperiment.result_wide, "static": intercityExperiment.result_static, "moving": intercityExperiment.result_moving},
    "intercity and sprinter": {"wide": passengerTrainExperiment.result_wide, "static": passengerTrainExperiment.result_static, "moving": passengerTrainExperiment.result_moving},
    "sprinter": {"wide": sprinterExperiment.result_wide, "static": sprinterExperiment.result_static, "moving": sprinterExperiment.result_moving},
}

fp = open("result.json", "w")
json.dump(experiment_results, fp)
fp.close()
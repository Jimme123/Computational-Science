import json

import allTrainsExperiment
# import freightTrainsExperiment
# import intercityExperiment
# import passengerTrainExperiment
# import sprinterExperiment

experiment_results = {
    "all mixed": allTrainsExperiment.result,
#     "intercities": intercityExperiment.result,
#     "sprinters": sprinterExperiment.result,
#     "intercities and sprinters": passengerTrainExperiment.result,
#     "freight trains": freightTrainsExperiment.result,
}

fp = open("result.json", "w")
json.dump(experiment_results, fp)
fp.close()
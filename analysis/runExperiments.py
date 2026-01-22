import json

import allTrainsExperiment
# import freightTrainsExperiment
# import intercityExperiment
# import passengerTrainExperiment
# import sprinterExperiment

experiment_results = {
    {"all mixed": {"wide": allTrainsExperiment.result_wide, "static": allTrainsExperiment.result_static, "moving": allTrainsExperiment.result_moving}},
#     "intercities": intercityExperiment.result,
#     "sprinters": sprinterExperiment.result,
#     "intercities and sprinters": passengerTrainExperiment.result,
#     "freight trains": freightTrainsExperiment.result,
}

fp = open("result.json", "w")
json.dump(experiment_results, fp)
fp.close()
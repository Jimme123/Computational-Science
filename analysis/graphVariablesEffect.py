import json
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

with open("results/result_variables.json", 'r') as fp:
    data = json.load(fp)

# Prepare data
data_to_plot = {}
for variable_name, experiment in data.items():
    data_to_plot[variable_name] = {"y": {"moving": [], "static": []}, "x": []}
    for value, result in experiment.items():
        static_max = max(result, key=lambda x: x[1][0][0])[1][0][0]
        data_to_plot[variable_name]['y']['static'].append([static_max])

        value = value if variable_name == "sight" else float(value)
        data_to_plot[variable_name]['x'].append(value)

        if variable_name not in ["sight", "sight_no_station", "block_size"]:
            moving_max = max(result, key=lambda x: x[1][0][1])[1][0][1]
            data_to_plot[variable_name]['y']['moving'].append([moving_max])
        else:
            data_to_plot[variable_name]['y']['moving'].append([None])


fig, axs = plt.subplots(2, 4, figsize=(12, 7))

i = 0
for variable_name, plot_data in data_to_plot.items():
    if variable_name == "sight_no_station":
        continue
    ax = axs[i%2][i//2]
    i += 1
    if variable_name == "sight":
        ax.plot(plot_data['x'], plot_data['y']['static'], label='with stations', marker='o', linestyle='', color="darkgoldenrod")
        ax.plot(plot_data['x'], data_to_plot['sight_no_station']['y']['static'], label='no stations', marker='o', linestyle='', color="darkolivegreen")
        ax.legend()
    else:
        ax.plot(plot_data['x'], plot_data['y']['static'], label='static', marker='o', color="cornflowerblue")
        ax.plot(plot_data['x'], plot_data['y']['moving'], label='moving', marker='o', color="indianred")
    ax.set_xlabel(variable_name)
    ax.set_ylabel("Capacity")
    ax.set_title(f"Capacity over {variable_name}")
    ax.grid(True)
    ax.set_ylim(bottom=0)
axs[-1, -1].axis('off')

ax.legend()
fig.suptitle("Influence of variables", fontsize=15)
fig.tight_layout()
plt.savefig("../plots/variable_effect.png", bbox_inches="tight", dpi=300)
plt.show()

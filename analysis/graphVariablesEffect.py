import json
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

with open("result_variables.json", 'r') as fp:
    data = json.load(fp)

# Prepare data
data_to_plot = {}
for variable_name, experiment in data.items():
    data_to_plot[variable_name] = {"y": [], "x": []}
    for value, result in experiment.items():
        static_max = max(result, key=lambda x: x[1][0][0])[1][0][0]
        moving_max = max(result, key=lambda x: x[1][0][1])[1][0][1]
        data_to_plot[variable_name]['y'].append([static_max, moving_max])
        data_to_plot[variable_name]['x'].append(value)
print(data_to_plot)

fig, axs = plt.subplots(2, 4, figsize=(12, 7))
i = 0
for variable_name, plot_data in data_to_plot.items():
    ax = axs[i%2][i//2]
    plot_data_y = np.array(plot_data['y'])
    ax.plot(plot_data['x'], plot_data_y[:, 0], label='static', marker='o', color="cornflowerblue")
    ax.plot(plot_data['x'], plot_data_y[:, 1], label='moving', marker='o', color="indianred")
    ax.set_xlabel(variable_name)
    ax.set_ylabel("Capacity")
    ax.set_title(f"Capacity over {variable_name}")
    ax.grid(True)

ax.legend(fontsize=15)
fig.suptitle("Influence of variables")
plt.savefig("../plots/variable_effect.png", bbox_inches="tight", dpi=300)
plt.show()

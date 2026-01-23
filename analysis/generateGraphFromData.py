import json
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

with open("result.json", 'r') as fp:
    data = json.load(fp)

groups = [key for key in data.keys()]

no_station_groups = groups[0:2]
with_station_groups = groups[2:5]

def prepare_data(selected_groups):
    data_to_plot = []
    medians = {'static': [], 'moving': []}
    for experiment in selected_groups:
        result = data[experiment]
        for signalling_type in ['static', 'moving']:
            max_data = max(result[signalling_type], key=lambda x: reduce(lambda s, x: s + x[0], x[1], 0))
            unwrapped_data = [c[0] for c in max_data[1]]
            data_to_plot.append(unwrapped_data)
            medians[signalling_type].append(np.median(unwrapped_data))
    return data_to_plot, medians

data_no_station, medians_no_station = prepare_data(no_station_groups)
data_with_station, medians_with_station = prepare_data(with_station_groups)

width = 0.2
in_group_spacing = 0.12
group_spacing = 0.8
fig, axs = plt.subplots(
    1, 2, figsize=(14, 6),
    gridspec_kw={'width_ratios': [0.85, 1.15]}
)

for idx, (ax, group_set, data_set, medians_set, title) in enumerate(zip(
    axs,
    [no_station_groups, with_station_groups],
    [data_no_station, data_with_station],
    [medians_no_station, medians_with_station],
    ["No Station", "With Station"]
)):
    center_x = np.arange(len(group_set)) * group_spacing
    bar_right_x = center_x + in_group_spacing
    bar_left_x = center_x - in_group_spacing
    box_x = np.sort(np.concatenate([bar_left_x, bar_right_x]))

    ax.boxplot(data_set, positions=box_x, widths=width)
    ax.bar(bar_left_x, medians_set['static'], width=width, label="static", color='cornflowerblue')
    ax.bar(bar_right_x, medians_set['moving'], width=width, label="moving", color='indianred')

    for i in range(len(group_set)):
        y = max(data_set[2*i] + data_set[2*i+1])
        rel_diff = medians_set['moving'][i] / medians_set['static'][i] - 1
        ax.text(center_x[i], y + 2, f"{int(rel_diff*100)}% increase", rotation=90,
                horizontalalignment='center', verticalalignment='bottom')

    ax.set_xticks(center_x)
    ax.set_xticklabels(group_set)
    ax.set_title(title)

    if idx == 0:
        ax.set_ylim(0, 225)
        ax.set_ylabel('Max capacity')
        ax.legend(loc='upper left')
    else:
        ax.set_ylim(0, 60)

plt.suptitle("Moving vs Static", fontsize=16)
plt.tight_layout()
plt.savefig("../plots/Situations.png", dpi=300)
plt.show()

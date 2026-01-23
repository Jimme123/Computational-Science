import json
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

with open("result.json", 'r') as fp:
    data = json.load(fp)

groups = [key for key in data.keys()]

data_to_plot = []
trains_plotted = []
medians = {'static': [], 'moving': []}

for experiment in groups:
    result = data[experiment]
    for signalling_type in ['static', 'moving']:
        max_data = max(result[signalling_type], key=lambda x: reduce(lambda s, x: s + x[0], x[1], 0))
        trains_plotted.append(max_data[0])
        unwrapped_data = [c[0] for c in max_data[1]]
        data_to_plot.append(unwrapped_data)
        medians[signalling_type].append(np.median(unwrapped_data))


width = 0.2
in_group_spacing = 0.1
group_spacing = 0.8
center_x = np.arange(len(groups))
bar_right_x = center_x+in_group_spacing
bar_left_x = center_x-in_group_spacing
box_x = np.sort(np.concat([bar_left_x, bar_right_x]))

plt.figure()
fig = plt.gcf()

plt.boxplot(data_to_plot, positions=box_x, widths=width)
plt.bar(bar_left_x, medians['static'], width=width, label="static", color='cornflowerblue')
plt.bar(bar_right_x, medians['moving'], width=width, label="moving", color='indianred')

# for x, y, trains in zip(box_x, data_to_plot, trains_plotted):
#     plt.text(x, max(y)+2, f"{trains} trains", rotation=90, horizontalalignment='center', verticalalignment='bottom')

for i in range(len(groups)):
    y = max(*data_to_plot[2*i], *data_to_plot[2*i+1])
    rel_diff = medians['moving'][i] / medians['static'][i] - 1
    plt.text(center_x[i], y+2, f"{int(rel_diff*100)}% increase", rotation=90, horizontalalignment='center', verticalalignment='bottom')

plt.ylim(0, 90)
plt.ylabel('Max capacity')
plt.xticks(center_x, groups)

under_fig = -8
plt.plot([center_x[0], center_x[1]], [under_fig] * 2, clip_on=False, color="black")
plt.plot([center_x[2], center_x[4]], [under_fig] * 2, clip_on=False, color="black")
plt.text((center_x[0] + center_x[1]) / 2, under_fig - 2, "no station", horizontalalignment="center", verticalalignment="top")
plt.text((center_x[2] + center_x[4]) / 2, under_fig - 2, "with station", horizontalalignment="center", verticalalignment="top")


plt.title('Moving vs Static')
plt.legend()

plt.savefig("../plots/Situations.png", bbox_inches="tight", dpi=300)
plt.show()
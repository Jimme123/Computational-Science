import osloMetro
from tools import *
import matplotlib.pyplot as plt
import numpy as np


static_model = osloMetro.generate_metro("static", station_size=0)
moving_model = osloMetro.generate_metro("moving")
result = test_capacity([static_model, moving_model], [osloMetro.metro_specifications], max_trains=20, repetitions=1, verbose=False)

static_capacities = []
moving_capacities = []

for entry in result:
    print(entry)
    static = entry[1][0][0]
    moving = entry[1][0][1]
    static_capacities.append(static)
    moving_capacities.append(moving)

reference_max_static = 28
reference_max_moving = 40
max_static = max(static_capacities)
max_moving = max(moving_capacities)

print("Max static:", max_static)
print("Max moving:", max_moving)


groups = ['Reference', 'Our model']
static_values = [reference_max_static, max_static]
moving_values = [reference_max_moving, max_moving]
width = 0.2
in_group_spacing = 0.05
group_spacing = 0.8

x = np.arange(len(groups)) 
plt.figure()
plt.bar(x - (width/2 + in_group_spacing), static_values, width, label='Static', color='red')
plt.bar(x + (width/2 + in_group_spacing), moving_values, width, label='Moving', color='blue')

plt.ylabel('Max capacity')
plt.xticks(x, groups)
plt.title('Vergelijking Oslo vs Simulatie')
plt.legend()

plt.savefig("../plots/Oslo_plot.png", bbox_inches="tight", dpi=300)
plt.show()

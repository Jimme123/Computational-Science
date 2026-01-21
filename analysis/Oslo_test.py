import osloMetro
from tools import *
import matplotlib.pyplot as plt


static_model = osloMetro.generate_metro("static", station_size=0)
moving_model = osloMetro.generate_metro("moving")
result = test_capacity([static_model, moving_model], [osloMetro.metro_specifications], max_trains=20, repetitions=1, verbose=True)

static_capacities = []
moving_capacities = []

for entry in result:
    print(entry)
    static = entry[1][0][0]
    moving = entry[1][0][1]
    static_capacities.append(static)

max_static = max(static_capacities)
max_moving = max(moving_capacities)
print("Max static:", max_static)
print("Max moving:", max_moving)

labels = ['Static', 'Moving']
values = [max_static, max_moving]

plt.figure()
plt.bar(labels, values)
plt.ylabel('Max capacity')
plt.title('JooiJooijOijo')

plt.show()

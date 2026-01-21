import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *

model = generate_metro(signalling_type="static", verbose=True)

metro_specifications['max_braking'] /= 2

add_trains(model, 10, metro_specifications)



# times = measure_station_travel_times_real_time(model, metro_specifications)

# print("\nTijd tussen stations:")
# for i, t in enumerate(times):
#     print(f"Traject {i + 1}: {t:.1f} s ({t/60:.2f} min)")

visualize(model, 500)

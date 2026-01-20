import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *
from generateModel import *

model = generate_model(signalling_type="static", 
                       distances_variation=1, 
                       acc_dist=[0.25, 0.5, 0.25], 
                       braking_dist=[0.25, 0.5, 0.25])
# print(test_capacity(model, metro_specifications, max_trains=30, verbose=True))

# add_trains(model, 10, metro_specifications)

# times = measure_station_travel_times_real_time(model, metro_specifications)

# print("\nTijd tussen stations:")
# for i, t in enumerate(times):
#     print(f"Traject {i + 1}: {t:.1f} s ({t/60:.2f} min)")

visualize(model, 500)

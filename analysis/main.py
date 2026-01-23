import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *
from generateModel import *

model = generate_model(signalling_type="moving",
                       distances_variation=1,
                       train_specifications=[sng_specifications, virm_specifications, freight_train_specifications],
                       num_trains=2,
                       num_stations=5,
                       block_size=1150,
                       min_station_distance=1300,
                       train_distribution=[1, 0, 0]
                       )
# print(test_capacity(model, max_trains=30, verbose=True))

# add_trains(model, 10, metro_specifications)

# times = measure_station_travel_times_real_time(model, metro_specifications)

# print("\nTijd tussen stations:")
# for i, t in enumerate(times):
#     print(f"Traject {i + 1}: {t:.1f} s ({t/60:.2f} min)")
for i in range(0, 500):
    model.step()

visualize(model, 500, "Circular Railway Simulation")

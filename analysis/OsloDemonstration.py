import osloMetro
from trainSpecifications import *
from simulation.tools import *
from simulation.visualize import *
import matplotlib.pyplot as plt
import numpy as np

moving_model = osloMetro.generate_metro("moving")
add_trains(moving_model, [metro_specifications]*14)

for i in range(1000):
    moving_model.step()

visualize(moving_model, 1000, "Oslo metro moving")

static_model = osloMetro.generate_metro("static", station_size=0)
add_trains(static_model, [metro_specifications]*10)

for i in range(1000):
    static_model.step()

visualize(static_model, 1000, "Oslo metro static")

moving_model_jam = osloMetro.generate_metro("moving")
add_trains(moving_model_jam, [metro_specifications]*20)

for i in range(1000):
    moving_model_jam.step()

visualize(moving_model_jam, 1000, "Oslo metro moving jam")

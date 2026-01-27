import osloMetro
from trainSpecifications import *
from simulation.tools import *
from simulation.visualize import *
import matplotlib.pyplot as plt
import numpy as np

moving_model = osloMetro.generate_metro("moving")
add_trains(moving_model, [metro_specifications]*14)

visualize(moving_model, 500, "Oslo metro moving")

import osloMetro
from tools import *
from visualize import *
import matplotlib.pyplot as plt
import numpy as np

moving_model = osloMetro.generate_metro("moving")
add_trains(moving_model, [metro_specifications]*14)

visualize(moving_model, 500, "Oslo metro moving")

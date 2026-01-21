import osloMetro
from tools import *

static_model = osloMetro.generate_metro("static", station_size=0)
moving_model = osloMetro.generate_metro("moving")
result = test_capacity([static_model, moving_model], [osloMetro.metro_specifications], max_trains=40, repetitions=1, verbose=True)
print(result)
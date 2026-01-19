import numpy as np

from simulation.model import *
from simulation.staticBlockSignalling import *
from simulation.movingBlockSignalling import *
from simulation.position import *

from tools import *
from visualize import *
from osloMetro import *

model = generate_metro(signalling_type="moving", verbose=False)

metro_specifications['max_braking'] /= 2

print(test_capacity(model, metro_specifications, min_trains=1, max_trains=5, verbose=True))
add_trains(model, 10, metro_specifications)

def measure_station_travel_times_real_time(model, metro_specifications, max_steps=20000):
    train = model.trains[0]

    dt = metro_specifications.get("dt", 1.0)

    blocks = model.signalling_control.blocks
    stations = [b for b in blocks if b.signal == Color.STATION]
    stations.sort(key=lambda b: b.position.start)

    station_indices = {id(s): i for i, s in enumerate(stations)}

    last_station_id = None
    last_time = None
    travel_times = []

    for step in range(max_steps):
        model.step()
        pos = train.position.bounds[1]

        for station in stations:
            if station.position.start <= pos <= station.position.end:
                sid = id(station)

                if last_station_id is None:
                    last_station_id = sid
                    last_time = step
                    break

                if sid != last_station_id:
                    steps_taken = step - last_time
                    time_seconds = steps_taken * dt

                    travel_times.append(time_seconds)

                    print(
                        f"Van station {station_indices[last_station_id]} "
                        f"naar station {station_indices[sid]}: "
                        f"{time_seconds:.1f} s"
                    )

                    last_station_id = sid
                    last_time = step

                    if len(travel_times) >= len(stations):
                        return travel_times
                break

    return travel_times

times = measure_station_travel_times_real_time(model, metro_specifications)

print("\nTijd tussen stations:")
for i, t in enumerate(times):
    print(f"Traject {i + 1}: {t:.1f} s ({t/60:.2f} min)")

visualize(model, 1000)

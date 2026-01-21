import copy
import numpy as np

from simulation.position import *
from simulation.model import *
from simulation.block import *

def measure_station_travel_times_real_time(model, metro_specifications, max_steps=20000, verbose=False):
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

    if verbose:
        print("\nTijd tussen stations:")
        for i, t in enumerate(times):
            print(f"Traject {i + 1}: {t:.1f} s ({t/60:.2f} min)")

    return travel_times


def add_trains(model, n, train_specification):
    length = model.signalling_control.length
    train_length = train_specification['length']

    if model.type == "moving":
        starts = np.linspace(0, length, n, False)
        starts = starts[::-1]
        for i in range(n):
            model.add_train(Position(starts[i], starts[i] + train_length, length), train_specification)

    else:
        blocks = model.signalling_control.blocks
        i = n
        for block in blocks:
            if block.signal.is_station:
                continue
            start = block.position.bounds[0] + 1
            model.add_train(Position(start, start + train_length, length), train_specification)
            i -= 1
            if i == 0:
                break
        if i > 0:
            return False

    return True


def test_capacity(trainless_model: Railroad, train_specification, wind_up=600, test_length=3600, min_trains=1, max_trains=5, verbose=False):
    n = 1
    length = trainless_model.signalling_control.length
    result = []

    for n in range(min_trains, max_trains + 1):
        model: Railroad = copy.deepcopy(trainless_model)
        # Add n trains to the model
        if add_trains(model, n, train_specification) == False:
            break

        for i in range(wind_up // model.dt):
            model.step()

        passes = 0
        was_occupied = model.signalling_control.block_contains_train(model.signalling_control.blocks[0])
        for i in range(test_length // model.dt):
            model.step()
            occupied = model.signalling_control.block_contains_train(model.signalling_control.blocks[0])
            if occupied and not was_occupied:
                passes += 1
            was_occupied = occupied

        capacity = float(passes) / (float(test_length)) * 60**2
        result.append([n, capacity])
        if verbose:
            print(f"for {n}, capacity is {capacity:.1f}")
    return np.array(result)

from osloMetro import generate_metro, metro_specifications
from simulation.tools import *

station_names = [
    "Majorstuen",
    "Nationaltheatret",
    "Stortinget",
    "Jernbanetorget",
    "Grønland",
    "Tøyen",
    "Grønland",
    "Jernbanetorget",
    "Stortinget",
    "Nationaltheatret",
]

moving_model = generate_metro("static", station_size=0)

measure_station_travel_times_real_time(moving_model, metro_specifications, station_names=station_names, verbose=True)
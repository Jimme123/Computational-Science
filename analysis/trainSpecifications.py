from simulation.train import TrainSpecifications

metro_specifications = TrainSpecifications(
    max_speed=19.4,
    max_acceleration=1.27,
    max_braking=1.35,
    max_power=1.68*2*10**6,
    weight=141.5*1000*2,
    length=108.68
    )

virm_specifications = TrainSpecifications(
    max_speed=38.89,
    max_acceleration=0.6,
    max_braking=1.2,
    max_power=2412*10**3,
    weight=349*1000,
    length=162.06
    )

sng_specifications = TrainSpecifications(
    max_speed=38.89,
    max_acceleration=1.3,
    max_braking=1.1,
    max_power=2400*10**3,
    weight=138*1000,
    length=75.760
    )

freight_train_specifications = TrainSpecifications(
    max_speed=44.44,
    max_braking=0.9,
    max_power=6400*10**3,
    weight=2155*10**3,
    length=575.5,
    tractive_effort=300*10**3
    )

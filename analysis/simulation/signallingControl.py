import mesa

from simulation.positionalAgent import *
from simulation.position import *
from simulation.block import *

class SignallingControl:
    def __init__(self, model, length):
        self.model = model
        self.length = length  # length of track
        self.trains = []
        self.blocks = []

    def add_train(self, train):
        # check if new train overlaps with existing train
        for other_train in self.trains:
            if overlap(train.position, other_train.position):
                raise Exception("New train overlaps with existing train")
        self.trains.append(train)

    def remove_train(self, train):
        self.trains.remove(train)

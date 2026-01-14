import mesa

from simulation.positionalAgent import *
from simulation.position import *
from simulation.block import *

class SignallingControl:
    def __init__(self, model, length):
        self.model = model
        self.length = length
        self.trains = []
        self.blocks = []

    def add_train(self, train):
        for other_train in self.trains:
            if overlap(train, other_train):
                raise Exception("New train overlaps with existing train")
        self.trains.append(train)

    def remove_train(self, train):
        self.trains.remove(train)

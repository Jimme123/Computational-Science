import mesa

from positionalAgent import *
from position import *
from block import *

class SignallingControl:
    def __init__(self, model, length):
        self.model = model
        self.length = length
        self.trains = []
        self.blocks = []
    
    def add_train(self, train):
        self.trains.append(train)

    def remove_train(self, train):
        self.trains.remove(train)

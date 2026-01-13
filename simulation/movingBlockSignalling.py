from signallingControl import *


class MovingBlockSignalling(SignallingControl):

    def __init__(self, model, length):
        super().__init__(model, length)

    def next_signal(self, train):
        train_before = self.get_train_before(train)
        if train_before is None:
            return (Color.GREEN, 1000000)
        distance = get_distance(train.position, train_before.position)
        return (Color.RED, distance)

    def get_train_before(self, train):
        index = self.trains.index(train)
        return self.trains[index - 1]

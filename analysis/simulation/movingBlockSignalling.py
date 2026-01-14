from simulation.staticBlockSignalling import *


class MovingBlockSignalling(StaticBlockSignalling):

    def __init__(self, model, length):
        super().__init__(model, length)

    def next_signal(self, train):
        train_before = self.get_train_before(train)
        train_distance = get_distance(train.position, train_before.position, self.length)
        station = self.get_nearest_station(train)
        if station is not None:
            station_distance = get_distance(train.position, station.position, self.length)
        else:
            return (Color.RED, train_distance)

        if train_distance <= station_distance:
            return (Color.RED, train_distance)
        elif station_distance > 1500:
            return (Color.GREEN, station_distance)
        else:
            return (Color.STATION, station_distance)


    def get_train_before(self, train):
        index = self.trains.index(train)
        return self.trains[index - 1]

    def get_nearest_station(self, train):
        """Returns nearest station to the train, if there are no stations returns None"""
        current_best_distance = self.length
        current_best_block = None
        for block in self.blocks:
            if get_distance(train.position, block.position, self.length) < current_best_distance:
                current_best_distance = get_distance(train.position, block.position, self.length)
                current_best_block = block
        return current_best_block

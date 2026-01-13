class Position:
    """
        Contains the position of an object with length.
        Oriented from the start of the line to the end of the line. (So the start of a train is at the back.)
    """
    def __init__(self, start, end, rail_length):
        assert(start <= rail_length)
        assert(end <= rail_length)
        self.start = start
        self.end = end
        self.rail_length = rail_length

    def __iadd__(self, other):
        assert(isinstance(other, float) or isinstance(other, int))
        start = (self.start + other) % self.rail_length
        end = (self.end + other) % self.rail_length
        return Position(start, end, self.rail_length)

    def __str__(self):
        return f"{self.start:.0f} - {self.end:.0f}"

    @property
    def bounds(self):
        return (self.start, self.end)


def overlap(position_a, position_b):
    """
    Determines if the positions a and b have overlap when in a circle track
    """
    start_a, end_a = position_a.bounds
    start_b, end_b = position_b.bounds
    if start_a > end_a and start_b > end_b:
        return True
    if start_a > end_a or start_b > end_b:
        if start_a > end_a and \
                (end_b <= end_a <= start_b or end_b <= start_a <= start_b):
            return True
        elif start_b > end_b and \
                (end_a <= end_b <= start_a or end_a <= start_b <= start_a):
            return True
        else:
            return False
    if start_a <= start_b <= end_a or\
        start_a <= end_b <= end_a or \
        (start_b <= start_a and end_a <= end_b):
        return True
    return False


def get_distance(position_a, position_b, rail_length):
    """Gets distance from end a to start b, so b is infront of a!!!"""
    if overlap(position_a, position_b):
        return 0
    start_a, end_a = position_a.bounds
    start_b, end_b = position_b.bounds
    return (start_b - end_a) % rail_length
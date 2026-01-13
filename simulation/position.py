class Position:
    """
        Contains the position of an object with length.
        Oriented from the start of the line to the end of the line. (So the start of a train is at the back.)
    """
    def __init__(self, start, end, rail_length):
        assert(start < rail_length)
        assert(end < rail_length)
        self.start = start
        self.end = end
        self.rail_length = rail_length

    def __add__(self, other):
        assert(isinstance(other, float) or isinstance(other, int))
        self.start = (self.start + other) % self.rail_length
        self.end = (self.end + other) % self.rail_length
        return self

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
    if start_a > end_a and \
            (end_b <= end_a <= start_b or start_b <= start_a <= end_b):
        return True
    if start_b > end_b and \
            (end_a <= end_b <= start_a or start_a <= start_b <= end_a):
        return True
    if start_a <= start_b <= end_a or\
        start_a <= end_b <= end_a or \
        (start_b <= start_a and end_a <= end_b):
        return True
    return False


def get_distance(position_a, position_b):
    if overlap(position_a, position_b):
        return 0
    start_a, end_a = position_a.bounds
    start_b, end_b = position_b.bounds
    if end_a < start_b:
        return start_b - end_a
    else:
        return start_a - end_b

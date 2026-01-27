"""
Containts the position class and multiple helper functions related to the
position
"""
class Position:
    """
        Contains the position of an object with length in a circle.
    """
    def __init__(self, start, end, rail_length):
        assert(0 <= start < rail_length)
        assert(0 <= end < rail_length)
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

    @property
    def length(self):
        return (self.end - self.start + self.rail_length) % self.rail_length



def get_segments(position):
    """
    input: position
    output: the bounds of the position if the position does not overlap
    with the start/end of the rail track else the position is split up
    into the part until the end of the track and the part starting at
    the start
    """
    start, end = position.bounds
    if end > start:
        return [(start, end)]
    else:
        return [(start, position.rail_length), (0, end)]


def overlap(position_a, position_b):
    """
    Determines if the positions a and b have overlap when in a circle track
    """
    segments_a = get_segments(position_a)
    segments_b = get_segments(position_b)

    for start_a, end_a in segments_a:
        for start_b, end_b in segments_b:
            if start_a <= start_b <= end_a or\
                start_a <= end_b <= end_a or \
                (start_b <= start_a and end_a <= end_b):
                return True
    return False


def get_distance(position_a, position_b, overlap_is_zero=True):
    """
        Gets distance from end a to start b, so b is in front of a!
    """
    assert(position_a.rail_length == position_b.rail_length)
    if overlap(position_a, position_b) and overlap_is_zero:
        return 0

    rail_length = position_a.rail_length

    start_a, end_a = position_a.bounds
    start_b, end_b = position_b.bounds
    return (start_b - end_a) % rail_length
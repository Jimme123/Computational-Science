class Position:
    """
        Contains the position of an object with length.
        Oriented from the start of the line to the end of the line. (So the start of a train is at the back.)
    """
    def __init__(self, start, end):
        assert(start < end)
        self.start = start
        self.end = end

    def __add__(self, other):
        assert(isinstance(other, float) or isinstance(other, int))
        self.start += other
        self.end += other
        return self

    def __str__(self):
        return f"{self.start} - {self.end}"
    
    @property
    def bounds(self):
        return (self.start, self.end)

def overlap(position_a , position_b):
    start_a, end_a = position_a.bounds
    start_b, end_b = position_b.bounds
    if start_a <= start_b <= end_a or\
                start_a <= end_b <= end_a or \
                (start_b <= start_a and end_a <= end_b):
        return True
    return False

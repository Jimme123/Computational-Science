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
        assert(isinstance(other, float))
        self.start += other
        self.end += other


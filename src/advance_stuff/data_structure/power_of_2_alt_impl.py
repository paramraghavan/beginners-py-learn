#https://www.programiz.com/python-programming/iterator
class PowTwoAltImpl:
    """Class to implement an iterator
    of powers of two"""

    def __init__(self, max=0):
        self.max = max

    # no need for implementation of __next__
    # iter is slef contained
    def __iter__(self):
        self.n = 0
        while self.n <= self.max:
            result = 2 ** self.n
            yield result
            self.n += 1
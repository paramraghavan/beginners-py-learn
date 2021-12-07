# Data Structures and Algorithms Using Python
# CHAPTER 1: Abstract Data Tpyes
# The Bag Abstract Data Type: List-Based Implementation
# http://home.ustc.edu.cn/~huang83/ds/Data%20Structures%20and%20Algorithms%20Using%20Python.pdf

class Bag:
    """
    Implements the Bag ADT container using a Python list.
    """

    # Constructs an empty bag.
    def __init__(self):
        self._theItems = list()

    # Returns the number of items in the bag.
    def __len__(self):
        return len(self._theItems)

    # Determines if an item is contained in the bag.
    def __contains__(self, item):
        return item in self._theItems

    # Adds a new item to the bag.
    def add(self, item):
        self._theItems.append(item)

    # Removes and returns an instance of the item from the bag.
    def remove(self, item):
        assert item in self._theItems, "The item must be in the bag"
        ndx = self._theItems.index(item)
        return self._theItems.pop(ndx)

    # Returns an iterator for traversing the list of items.
    def __iter__(self):
        return _BagIterator(self._theItems)

    def __repr__(self):
        return f'<a Bag object with items -> {self._theItems}>'

class _BagIterator:
    def __init__(self, theList):
        self._bagItems = theList
        self._curItems = 0
    #
    # def __iter__(self):
    #     return self

    # returns the next item in the list
    def __next__(self):
        if self._curItems < len(self._bagItems):
            item = self._bagItems[self._curItems]
            self._curItems += 1
            return item
        else:
            raise StopIteration

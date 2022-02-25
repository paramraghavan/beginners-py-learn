def printName(name):
    print(f'My name is {name}')


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f'Node content: {self.data}'

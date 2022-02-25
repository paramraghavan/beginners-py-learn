'''
See details at https://realpython.com/linked-lists-python/
'''

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            # pop usually pops the last or the nth item in the list like a stack
            node = Node(data=nodes.pop(0))
            self.head = node
            # lists from 0th to nth index
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    # traverse linked list
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next


    # insert at the beginning of the list
    def add_first(self, node):
        if self.head is None:
            self.head = node
            node.next = None
        else:
            node.next = self.head
            self.head = node

    # Inserting a new node at the end of the list forces you to traverse
    # the whole linked list first and to add the new node when you reach the end.
    def add_last(self, node):
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        # this is the last node in the list
        current_node.next = node


    def add_after(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return

        raise Exception("Node with data '%s' not found" % target_node_data)


    def add_before(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        # if self.head.data == target_node_data:
        #     return self.add_first(new_node)

        prev_node = self.head
        for node in self:
            if node.data == target_node_data:
                prev_node.next = new_node
                new_node.next = node
                return
            prev_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)

    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.data == target_node_data:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)


    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

if __name__ == '__main__':
    # exercise link list
    llist = LinkedList(["b", "c","d"])
    llist.add_before("d", Node("c1"))

    print(llist)



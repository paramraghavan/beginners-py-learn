# node class
# node class
class Node:

    def __init__(self, data):
        # left child
        self.left = None
        # right child
        self.right = None
        # node's value
        self.data = data

    # print function
    def PrintTree(self):
        print(self.data)

    def __repr__(self):
        if self.data is not None:
            # print(self.data)
            return f'<Node data -> {self.data}>'
        else:
            # print('None')
            pass
# # test driver
# root = Node(27)
# root.PrintTree()
'''
  Recursive binary tree
  https://www.section.io/engineering-education/binary-tree-data-structure-python/#implementing-a-binary-tree
'''
class BinaryTree:
    def __init__(self, nodes=None):
        self.root = None
        if nodes is None:
            pass
        else:
            print('To implement.')
            pass #todo


    def insert_node(self, entry):
        if self.root is None:
           self.root = Node(entry)
        else:
            entry_node = Node(entry)
            curr_node = self.root
            while(curr_node is not None):
                if curr_node.data > entry_node.data:
                    # move left
                   if curr_node.left is None:
                       curr_node.left = entry_node
                       break
                   else:
                        curr_node = curr_node.left
                else:
                    # curr_node is <= entry node
                    if  curr_node.right is None:
                        curr_node.right = entry_node
                        break
                    else:
                        curr_node = curr_node.right

    # iterate in the sort order
    # traverse linked list depth first
    '''
        1) Create an empty stack S.
        2) Initialize current node as root
        3) Push the current node to S and set current = current->left until current is NULL
        4) If current is NULL and stack is not empty then
         -> Pop the top item from stack.
         -> Print the popped item, set current = popped_item->right 
         -> Go to step 3.
        5) If current is NULL and stack is empty then we are done.
        looop:
            #left
            first traverse all the way to the left, 
            keep storing the current node to the stack 
            until you find the leaf node or the current node.left is None
            if there are items in stack then
             pop node out of the stack, assign it to current node
            
            # print node
            print curent node
            
            #right
            Now check if this current node has right node
            check if the node does not have a right node then
             pop item from stack and assign it to current node
        continue the loop 
    '''
    def __iter__(self):
        current_node = self.root
        stack = []

        stack.append(current_node)
        while True:
            if current_node is None and len(stack) == 0:
                break;
            while current_node is not None:
                current_node = current_node.left
                if current_node is not None:
                    stack.append(current_node)
            if current_node is None and len(stack) > 0:
                popped_item = stack.pop()
                # print(popped_item.data)
                yield popped_item.data
                current_node = popped_item.right
                if current_node is not None:
                    stack.append(current_node)
                continue


    # def __repr__(self):
    #     pass

# DIRVER
binary_tree = BinaryTree()

binary_tree.insert_node(10)
binary_tree.insert_node(7)
binary_tree.insert_node(12)
binary_tree.insert_node(6)
binary_tree.insert_node(9)
binary_tree.insert_node(4)
binary_tree.insert_node(3)
binary_tree.insert_node(8)
binary_tree.insert_node(11)
binary_tree.insert_node(16)

print('iterate.........')
# for item in binary_tree:
#     print(f'in order {item.data}')

it = iter(binary_tree)

for item in it:
    print(item)

    # # traverse linked list
    # def __iter__(self):
    #     node = self.head
    #     while node is not None:
    #         yield node
    #         node = node.next
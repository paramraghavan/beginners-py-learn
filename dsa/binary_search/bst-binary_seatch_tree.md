# Binary Search Tree (BST) - Theory and Implementation

A Binary Search Tree is a hierarchical data structure where each node has at most two children, and it maintains the BST
property: for every node, all values in the left subtree are smaller, and all values in the right subtree are larger.

## BST Structure

```
        8
      /   \
     3     10
   /  \      \
  1    6     14
      / \    /
     4   7  13
```

## Implementation## Time Complexities

### Average Case (Balanced Tree):

- **Search**: O(log n) - eliminates half the tree at each step
- **Insertion**: O(log n) - traverse from root to leaf position
- **Deletion**: O(log n) - find node + restructure
- **Traversal**: O(n) - must visit every node

### Worst Case (Skewed Tree):

When the tree becomes a linked list (all nodes in one direction):

- **Search**: O(n) - linear search through all nodes
- **Insertion**: O(n) - traverse to the end
- **Deletion**: O(n) - find node at the end
- **Traversal**: O(n) - still need to visit all nodes

### Space Complexity:

- **Storage**: O(n) - one node per element
- **Recursive operations**: O(h) where h is height
    - Average case: O(log n)
    - Worst case: O(n)

## Why These Complexities?

**Balanced Tree (O(log n)):**

```
        8          Height = 3, Nodes = 7
      /   \        At each level, we eliminate
     3     10      half the remaining nodes
   /  \      \     
  1    6     14    Search path: 8 → 3 → 6 (3 steps)
      / \          log₂(7) ≈ 3
     4   7
```

**Skewed Tree (O(n)):**

```
1                 Height = 6, Nodes = 6
 \                Must traverse entire chain
  3               Search for 6: 1→3→6→8→10→14
   \              (6 steps = n steps)
    6
     \
      8
       \
        10
         \
         14
```

## BST Properties

**Advantages:**

- Dynamic size (unlike arrays)
- Efficient search, insertion, deletion in average case
- Inorder traversal gives sorted sequence
- No need to shift elements (unlike arrays)

**Disadvantages:**

- Can become unbalanced, leading to O(n) operations
- Extra memory overhead for pointers
- No constant-time access by index

**When to Use BST:**

- Frequent search, insertion, and deletion operations
- Need to maintain sorted order dynamically
- Don't know the data size in advance

**Real-world Applications:**

- Database indexing
- File systems
- Expression parsing
- Priority queues (with modifications)
- Auto-complete systems

> Other trees AVL trees or Red-Black trees sacrifice some insertion/deletion speed for guaranteed logarithmic search
> time, making them ideal for read-heavy applications requiring consistent performance.
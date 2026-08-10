"""
Essential Data Structure Implementations for CodeSignal GCA
Complete implementations with test examples

DATA STRUCTURES INCLUDED:
1. Linked List (singly)
   - append, prepend, delete, search, reverse, to_list

2. Binary Tree
   - inorder, preorder, postorder, level_order traversals
   - is_balanced, lowest_common_ancestor, max_depth, min_depth

3. Graph (adjacency list)
   - add_edge, add_undirected_edge
   - dfs, bfs, has_cycle, topological_sort

4. Stack
   - push, pop, peek, is_empty, size
   - valid_parentheses function

5. Queue
   - enqueue, dequeue, front, is_empty, size
   - Uses deque internally (O(1) operations)

6. Trie (prefix tree)
   - insert, search, starts_with
   - get_words_with_prefix

7. Binary Search Tree (BST)
   - insert, search, delete
   - Handles single node and multiple node cases

HOW TO USE THIS FILE:
1. Study each data structure class
2. Understand all methods and their complexity
3. Run the test section to see examples
4. Implement each structure from scratch
5. Practice building them without reference
6. Use as reference during interviews

PRACTICE TIPS:
- Implement from scratch without copying
- Trace through examples manually
- Understand each method's purpose
- Know the time/space complexity of each operation
- Practice building multiple instances
"""

from typing import Optional, List, Any


# ============================================================================
# LINKED LIST
# ============================================================================

class ListNode:
    """Node for singly linked list."""

    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


class SingleLinkedList:
    """Singly linked list implementation."""

    def __init__(self):
        self.head = None

    def append(self, val: int) -> None:
        """Add node at end."""
        if not self.head:
            self.head = ListNode(val)
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = ListNode(val)

    def prepend(self, val: int) -> None:
        """Add node at beginning."""
        self.head = ListNode(val, self.head)

    def delete(self, val: int) -> None:
        """Remove first occurrence of value."""
        if not self.head:
            return

        if self.head.val == val:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.val == val:
                current.next = current.next.next
                return
            current = current.next

    def search(self, val: int) -> bool:
        """Check if value exists."""
        current = self.head
        while current:
            if current.val == val:
                return True
            current = current.next
        return False

    def reverse(self) -> None:
        """Reverse the linked list."""
        prev = None
        current = self.head

        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp

        self.head = prev

    def to_list(self) -> List[int]:
        """Convert to Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result


# Common Linked List Problems

def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse linked list iteratively."""
    prev = None
    current = head

    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp

    return prev


def detect_cycle(head: Optional[ListNode]) -> bool:
    """Detect cycle using Floyd's algorithm (fast/slow pointers)."""
    if not head or not head.next:
        return False

    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False


def find_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """Find node where cycle starts."""
    if not head:
        return None

    slow = fast = head

    # Find intersection point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow


def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """Merge two sorted linked lists."""
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return dummy.next


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """Remove nth node from end of list."""
    dummy = ListNode(0, head)
    fast = slow = dummy

    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        if not fast:
            return head
        fast = fast.next

    # Move both pointers until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next
    return dummy.next


# ============================================================================
# BINARY TREE
# ============================================================================

class TreeNode:
    """Node for binary tree."""

    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


class BinaryTree:
    """Binary tree implementation."""

    def __init__(self, root: Optional[TreeNode] = None):
        self.root = root

    def inorder(self, node: Optional[TreeNode] = None, result: List = None) -> List[int]:
        """Inorder traversal (left, root, right)."""
        if result is None:
            result = []
            node = self.root

        if node:
            self.inorder(node.left, result)
            result.append(node.val)
            self.inorder(node.right, result)

        return result

    def preorder(self, node: Optional[TreeNode] = None, result: List = None) -> List[int]:
        """Preorder traversal (root, left, right)."""
        if result is None:
            result = []
            node = self.root

        if node:
            result.append(node.val)
            self.preorder(node.left, result)
            self.preorder(node.right, result)

        return result

    def postorder(self, node: Optional[TreeNode] = None, result: List = None) -> List[int]:
        """Postorder traversal (left, right, root)."""
        if result is None:
            result = []
            node = self.root

        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.val)

        return result

    def level_order(self) -> List[List[int]]:
        """
        Level-order traversal (BFS).
        Returns nodes grouped by level.
        Time: O(n), Space: O(w) where w is max width

        Can also use index-based queue (no imports):
            queue = [self.root]
            index = 0
            while index < len(queue):
                level_size = len(queue) - index
                for _ in range(level_size):
                    node = queue[index]
                    index += 1
                    # process node...
        """
        if not self.root:
            return []

        from collections import deque
        result = []
        queue = deque([self.root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)

        return result

    def is_balanced(self, node: Optional[TreeNode] = None) -> bool:
        """Check if tree is height-balanced."""
        if node is None:
            node = self.root

        def check_balance(node: Optional[TreeNode]) -> tuple:
            """Returns (is_balanced, height)."""
            if not node:
                return True, 0

            left_balanced, left_height = check_balance(node.left)
            if not left_balanced:
                return False, 0

            right_balanced, right_height = check_balance(node.right)
            if not right_balanced:
                return False, 0

            if abs(left_height - right_height) > 1:
                return False, 0

            return True, max(left_height, right_height) + 1

        balanced, _ = check_balance(node)
        return balanced

    def lowest_common_ancestor(self, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        """Find LCA of two nodes (BST)."""
        node = self.root

        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node

        return None


# Common Binary Tree Problems

def max_depth(root: Optional[TreeNode]) -> int:
    """Maximum depth of tree."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def min_depth(root: Optional[TreeNode]) -> int:
    """Minimum depth to leaf node."""
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Check if tree is valid BST."""
    def validate(node: Optional[TreeNode], min_val: int, max_val: int) -> bool:
        if not node:
            return True

        if node.val <= min_val or node.val >= max_val:
            return False

        return validate(node.left, min_val, node.val) and validate(node.right, node.val, max_val)

    return validate(root, float('-inf'), float('inf'))


def path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """Check if path from root to leaf equals target sum."""
    if not root:
        return False

    if not root.left and not root.right:
        return root.val == target_sum

    return path_sum(root.left, target_sum - root.val) or path_sum(root.right, target_sum - root.val)


def diameter_of_tree(root: Optional[TreeNode]) -> int:
    """Diameter (longest path between two nodes)."""
    diameter = [0]

    def height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0

        left_height = height(node.left)
        right_height = height(node.right)

        diameter[0] = max(diameter[0], left_height + right_height)

        return 1 + max(left_height, right_height)

    height(root)
    return diameter[0]


# ============================================================================
# GRAPH
# ============================================================================

class Graph:
    """Graph using adjacency list."""

    def __init__(self):
        self.graph = {}

    def add_edge(self, u: Any, v: Any) -> None:
        """Add edge (u -> v)."""
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def add_undirected_edge(self, u: Any, v: Any) -> None:
        """Add undirected edge."""
        self.add_edge(u, v)
        self.add_edge(v, u)

    def dfs(self, start: Any) -> List[Any]:
        """DFS traversal."""
        visited = set()
        result = []

        def dfs_helper(node):
            visited.add(node)
            result.append(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    dfs_helper(neighbor)

        dfs_helper(start)
        return result

    def bfs(self, start: Any) -> List[Any]:
        """
        BFS traversal.
        Time: O(V + E), Space: O(V)

        Can also use index-based queue (no imports):
            queue = [start]
            index = 0
            visited = {start}
            while index < len(queue):
                node = queue[index]
                index += 1
                for neighbor in self.graph.get(node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        """
        from collections import deque
        visited = {start}
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def has_cycle(self) -> bool:
        """Detect cycle using DFS."""
        visited = set()
        rec_stack = set()

        def dfs_cycle(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs_cycle(node):
                    return True

        return False

    def topological_sort(self) -> List[Any]:
        """Topological sort for DAG."""
        visited = set()
        stack = []

        def dfs_topo(node):
            visited.add(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    dfs_topo(neighbor)

            stack.append(node)

        for node in self.graph:
            if node not in visited:
                dfs_topo(node)

        return stack[::-1]


# ============================================================================
# STACK
# ============================================================================

class Stack:
    """Stack implementation using list."""

    def __init__(self):
        self.items = []

    def push(self, val: Any) -> None:
        """Add element to top."""
        self.items.append(val)

    def pop(self) -> Any:
        """Remove and return top element."""
        return self.items.pop() if self.items else None

    def peek(self) -> Any:
        """View top element without removing."""
        return self.items[-1] if self.items else None

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.items) == 0

    def size(self) -> int:
        """Return stack size."""
        return len(self.items)


def valid_parentheses(s: str) -> bool:
    """Check if parentheses are valid."""
    stack = Stack()
    pairs = {'(': ')', '{': '}', '[': ']'}

    for char in s:
        if char in pairs:
            stack.push(char)
        else:
            if stack.is_empty() or pairs[stack.pop()] != char:
                return False

    return stack.is_empty()


# ============================================================================
# QUEUE
# ============================================================================

class Queue:
    """
    Queue implementation using deque.

    Current: Uses deque for O(1) popleft()

    Alternative: Index-based implementation (no imports):
        class Queue:
            def __init__(self):
                self.items = []
                self.index = 0

            def enqueue(self, val):
                self.items.append(val)

            def dequeue(self):
                if self.index < len(self.items):
                    val = self.items[self.index]
                    self.index += 1
                    # Cleanup if needed
                    if self.index > len(self.items) // 2:
                        self.items = self.items[self.index:]
                        self.index = 0
                    return val
                return None

    Both achieve O(1) amortized dequeue performance.
    """

    def __init__(self):
        from collections import deque
        self.items = deque()

    def enqueue(self, val: Any) -> None:
        """Add element to rear."""
        self.items.append(val)

    def dequeue(self) -> Any:
        """Remove and return front element."""
        return self.items.popleft() if self.items else None

    def front(self) -> Any:
        """View front element without removing."""
        return self.items[0] if self.items else None

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.items) == 0

    def size(self) -> int:
        """Return queue size."""
        return len(self.items)


# ============================================================================
# TRIE (PREFIX TREE)
# ============================================================================

class TrieNode:
    """Node for Trie."""

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Trie implementation for strings."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end = True

    def search(self, word: str) -> bool:
        """Search for exact word."""
        node = self.root

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix."""
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """Get all words with given prefix."""
        result = []
        node = self.root

        for char in prefix:
            if char not in node.children:
                return result
            node = node.children[char]

        def dfs(node, word):
            if node.is_end:
                result.append(word)

            for char, child in node.children.items():
                dfs(child, word + char)

        dfs(node, prefix)
        return result


# ============================================================================
# BINARY SEARCH TREE
# ============================================================================

class BST:
    """Binary Search Tree implementation."""

    def __init__(self):
        self.root = None

    def insert(self, val: int) -> None:
        """Insert value into BST."""
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_helper(self.root, val)

    def _insert_helper(self, node: TreeNode, val: int) -> None:
        if val < node.val:
            if node.left:
                self._insert_helper(node.left, val)
            else:
                node.left = TreeNode(val)
        else:
            if node.right:
                self._insert_helper(node.right, val)
            else:
                node.right = TreeNode(val)

    def search(self, val: int) -> bool:
        """Search for value in BST."""
        return self._search_helper(self.root, val)

    def _search_helper(self, node: Optional[TreeNode], val: int) -> bool:
        if not node:
            return False

        if node.val == val:
            return True
        elif val < node.val:
            return self._search_helper(node.left, val)
        else:
            return self._search_helper(node.right, val)

    def delete(self, val: int) -> None:
        """Delete value from BST."""
        self.root = self._delete_helper(self.root, val)

    def _delete_helper(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not node:
            return None

        if val < node.val:
            node.left = self._delete_helper(node.left, val)
        elif val > node.val:
            node.right = self._delete_helper(node.right, val)
        else:
            # Node to delete found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Find inorder successor
                min_larger_node = self._find_min(node.right)
                node.val = min_larger_node.val
                node.right = self._delete_helper(node.right, min_larger_node.val)

        return node

    def _find_min(self, node: TreeNode) -> TreeNode:
        while node.left:
            node = node.left
        return node


# ============================================================================
# TEST EXAMPLES - Input/Output for all data structures
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DATA STRUCTURES - TEST EXAMPLES")
    print("=" * 80)

    # LINKED LIST
    print("\n### LINKED LIST ###")

    # Single Linked List
    ll = SingleLinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    print(f"SingleLinkedList.append(1,2,3) → {ll.to_list()}")
    print("  Expected: [1, 2, 3]")

    ll.prepend(0)
    print(f"After prepend(0) → {ll.to_list()}")
    print("  Expected: [0, 1, 2, 3]")

    print(f"search(2) → {ll.search(2)}")
    print("  Expected: True")

    ll.delete(2)
    print(f"After delete(2) → {ll.to_list()}")
    print("  Expected: [0, 1, 3]")

    ll.reverse()
    print(f"After reverse() → {ll.to_list()}")
    print("  Expected: [3, 1, 0]")

    # Reverse linked list function
    head = ListNode(1, ListNode(2, ListNode(3)))
    reversed_head = reverse_linked_list(head)
    result = []
    current = reversed_head
    while current:
        result.append(current.val)
        current = current.next
    print(f"\nreverse_linked_list(1→2→3) → {result}")
    print("  Expected: [3, 2, 1]")

    # Detect cycle
    head = ListNode(1, ListNode(2, ListNode(3)))
    head.next.next.next = head.next  # Create cycle: 1→2→3→2
    print(f"detect_cycle(1→2→3→2 [cyclic]) → {detect_cycle(head)}")
    print("  Expected: True")

    # BINARY TREE
    print("\n### BINARY TREE ###")

    #         1
    #        / \
    #       2   3
    #      / \
    #     4   5
    node4 = TreeNode(4)
    node5 = TreeNode(5)
    node2 = TreeNode(2, node4, node5)
    node3 = TreeNode(3)
    root = TreeNode(1, node2, node3)

    tree = BinaryTree(root)

    print(f"inorder(tree) → {tree.inorder()}")
    print("  Expected: [4, 2, 5, 1, 3]")

    print(f"preorder(tree) → {tree.preorder()}")
    print("  Expected: [1, 2, 4, 5, 3]")

    print(f"postorder(tree) → {tree.postorder()}")
    print("  Expected: [4, 5, 2, 3, 1]")

    print(f"level_order(tree) → {tree.level_order()}")
    print("  Expected: [[1], [2, 3], [4, 5]]")

    print(f"max_depth(tree) → {max_depth(root)}")
    print("  Expected: 3")

    print(f"is_balanced(tree) → {tree.is_balanced()}")
    print("  Expected: True (height difference ≤ 1)")

    # Valid BST
    bst_root = TreeNode(2, TreeNode(1), TreeNode(3))
    print(f"is_valid_bst(2/1/3 BST) → {is_valid_bst(bst_root)}")
    print("  Expected: True")

    # GRAPH
    print("\n### GRAPH ###")

    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)

    print(f"DFS from 1 → {g.dfs(1)}")
    print("  Expected: [1, 2, 4, 3, 5]")

    print(f"BFS from 1 → {g.bfs(1)}")
    print("  Expected: [1, 2, 3, 4, 5]")

    g_cycle = Graph()
    g_cycle.add_edge(1, 2)
    g_cycle.add_edge(2, 3)
    g_cycle.add_edge(3, 1)  # Creates cycle
    print(f"has_cycle(1→2→3→1) → {g_cycle.has_cycle()}")
    print("  Expected: True")

    g_dag = Graph()
    g_dag.add_edge(5, 2)
    g_dag.add_edge(5, 0)
    g_dag.add_edge(4, 0)
    g_dag.add_edge(4, 1)
    g_dag.add_edge(2, 3)
    g_dag.add_edge(3, 1)
    print(f"topological_sort() → {g_dag.topological_sort()}")
    print("  Expected: [5, 4, 2, 3, 1, 0] or similar valid topological order")

    # STACK
    print("\n### STACK ###")

    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"After push(1,2,3): size={stack.size()}, peek={stack.peek()}")
    print("  Expected: size=3, peek=3")

    popped = stack.pop()
    print(f"After pop(): popped={popped}, size={stack.size()}")
    print("  Expected: popped=3, size=2")

    print(f"valid_parentheses('{{[()]}}') → {valid_parentheses('{[()]}')}")
    print("  Expected: True")

    print(f"valid_parentheses('{{[}})') → {valid_parentheses('{[})')}")
    print("  Expected: False")

    # QUEUE
    print("\n### QUEUE ###")

    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print(f"After enqueue(1,2,3): size={queue.size()}, front={queue.front()}")
    print("  Expected: size=3, front=1")

    dequeued = queue.dequeue()
    print(f"After dequeue(): dequeued={dequeued}, size={queue.size()}")
    print("  Expected: dequeued=1, size=2")

    # TRIE
    print("\n### TRIE ###")

    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("apricot")
    trie.insert("bat")

    print(f"search('apple') → {trie.search('apple')}")
    print("  Expected: True")

    print(f"search('app') → {trie.search('app')}")
    print("  Expected: True")

    print(f"search('appl') → {trie.search('appl')}")
    print("  Expected: False (incomplete word)")

    print(f"starts_with('ap') → {trie.starts_with('ap')}")
    print("  Expected: True")

    print(f"get_words_with_prefix('ap') → {trie.get_words_with_prefix('ap')}")
    print("  Expected: ['apple', 'app', 'apricot']")

    # BINARY SEARCH TREE
    print("\n### BINARY SEARCH TREE ###")

    bst = BST()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(2)
    bst.insert(4)
    bst.insert(6)
    bst.insert(8)

    print(f"BST.search(4) → {bst.search(4)}")
    print("  Expected: True")

    print(f"BST.search(9) → {bst.search(9)}")
    print("  Expected: False")

    bst.delete(3)
    print(f"After delete(3): search(3)={bst.search(3)}")
    print("  Expected: False (node deleted)")

    print(f"After delete(3): search(4)={bst.search(4)}")
    print("  Expected: True (right child promoted)")

    print("\n" + "=" * 80)

"""Beginner DFS examples.

Mental model:
DFS means "go as deep as possible, then come back."

Use DFS when:
- You need to visit everything connected to a starting node.
- You need to search paths in a tree or graph.
- You need to mark connected components, islands, or reachable nodes.

Why visited matters:
Graphs can contain cycles. Without a visited set, DFS may revisit the same nodes
forever.
"""


def dfs(graph, start, visited=None):
    """Recursive DFS that also handles sparse graphs.

    A sparse graph may mention a neighbor that is not itself a key in the
    dictionary. `graph.get(start, [])` prevents KeyError for those leaf nodes.
    """
    if visited is None:
        visited = set()

    visited.add(start)
    # Use .get() to handle nodes that don't exist as keys
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

# Example 1: Complete graph (all nodes as keys)
# ========================================
graph1 = {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]}
start = 1
result1 = dfs(graph1, start)
print(f"Graph: {graph1}")
print(f"Start: {start}")
print(f"Output: {result1}")
# Output: {1, 2, 3, 4, 5}

# Example 2: Sparse graph (leaf nodes not as keys) - using .get()
# ==============================================================
graph2 = {1:[2,3], 2:[4], 3:[5]}  # 4 and 5 are not keys
start = 1
result2 = dfs(graph2, start)
print(f"\nGraph: {graph2}")
print(f"Start: {start}")
print(f"Output: {result2}")
# Output: {1, 2, 3, 4, 5}

# Example 3: Disconnected graph
# =============================
graph3 = {1:[2], 2:[3], 4:[5], 5:[]}  # 1-2-3 and 4-5 are separate
start = 1
result3 = dfs(graph3, start)
print(f"\nGraph: {graph3}")
print(f"Start: {start}")
print(f"Output: {result3}")
# Output: {1, 2, 3} (4 and 5 not reachable)

# Time: O(V + E), Space: O(V) for recursion


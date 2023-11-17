# Python Memory Management

* In Python everything is an object,  Dynamic Memory Allocation underlies Python Memory Management.
When objects are no longer needed, the Python Memory Manager will automatically reclaim memory from them.
* Automatic Memory Management: Python automates memory allocation and deallocation through a built-in garbage collector. This means that developers don't need to manually manage memory, which simplifies coding but also requires understanding of how Python handles memory to optimize performance.
* Garbage Collection:  
  * **Reference Counting**: The primary method Python uses for garbage collection is reference counting. Each object in Python has a reference count that tracks how many references point to it. When this count reaches zero, it means the object is no longer needed, and Python can reclaim the memory.
  * **Cyclic Garbage Collector**: Python also has a cyclic garbage collector to handle reference cycles. These cycles occur when two or more objects reference each other but are otherwise not needed. The cyclic garbage collector periodically runs to identify and clean up these cycles.
*  Memory Pools: Python uses memory pools for efficient memory management. Small objects (up to 512 bytes) are allocated from memory pools, which helps reduce fragmentation and overhead in memory allocation.
*  Immutable Objects: Some Python objects (like strings and tuples) are immutable, meaning they cannot be changed after they are created. If you modify an immutable object, Python creates a new object and the old one is garbage collected if no references remain.
* Memory Profiling Tools: Tools like tracemalloc, objgraph, and memory_profiler can help in identifying memory leaks and understanding memory usage, which is crucial for optimizing memory in larger applications.
*  Best Practices for Memory Management:
    * Avoid circular references or break them manually if necessary.
    * Use generators and iterators for large data processing to save memory.
    * Be cautious with global variables as they may persist throughout the life of a program.
    * Use del to remove references to objects when they are no longer needed.
    * Understand the scope of your variables; local variables are garbage collected sooner than global variables.


# References:
- https://realpython.com/python-memory-management/ ***
- https://docs.python.org/3/c-api/memory.html


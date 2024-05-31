# Basics of Programming with Stack, Heap, and Virtual Memory

## 1. Stack
The stack is a region of memory used for storing temporary variables created by each function. It works in a last-in, first-out (LIFO) manner. Each time a function is called, a new frame is pushed onto the stack containing that function's local variables and some control information. When the function returns, its frame is popped off the stack.

- **Characteristics:**
  - Fast access
  - Limited in size
  - Managed automatically by the CPU (through function calls and returns)
  - Stores local variables, function parameters, return addresses

## 2. Heap
The heap is a region of memory used for dynamic memory allocation. Unlike the stack, the heap does not automatically manage memory; it requires manual management (usually via functions like `malloc` and `free` in C, or `new` and `delete` in C++).

- **Characteristics:**
  - Slower access compared to the stack
  - Larger and more flexible
  - Managed manually by the programmer
  - Stores dynamically allocated memory

## 3. Virtual Memory
Virtual memory is a memory management technique that provides an "idealized abstraction of the storage resources" that are actually available on a given machine. It creates an illusion of a very large (main) memory.

- **Characteristics:**
  - Provides large address spaces
  - Uses both hardware and software to enable programs to use more memory than physically available
  - Helps isolate and protect memory spaces of different processes

# CPU Variable Storage

When a program is executed, the CPU needs to know where to store variables. Variables can be stored in:

- **Registers:** Small, fast storage locations within the CPU used for immediate calculations and temporary data.
- **Cache:** A smaller, faster type of volatile computer memory that provides high-speed data access to the CPU and stores frequently used computer programs, applications, and data.
- **Main Memory (RAM):** The primary storage used to store currently executing programs and their data.

# How Does a Computer Know Where to Start the Program and Run?

## Point of Entry

1. **Bootloader:** When a computer is powered on, the BIOS (Basic Input/Output System) or UEFI (Unified Extensible Firmware Interface) initializes hardware components and loads the bootloader from a predefined location (like the hard drive or SSD).

2. **Operating System:** The bootloader loads the operating system into memory. The OS initializes and prepares the system for running programs.

3. **Program Execution:**
   - **Executable File:** Each program is compiled into an executable file, which contains the code, data, and metadata needed for execution.
   - **Entry Point:** The executable file specifies an entry point (typically a function named `main` in C/C++ programs) where the CPU should start executing the program. The operating system loads the executable into memory and sets the instruction pointer (IP) to the entry point.
   - **Initialization:** The OS performs additional setup, such as setting up the stack and heap, before transferring control to the program's entry point.

## Example in Python:
```python
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```
When the above Python program is run:
- The Python interpreter reads the script and identifies the entry point, which is guarded by `if __name__ == "__main__":`.
- The interpreter sets up the necessary runtime environment, including memory management for stack and heap.
- The `main` function is called, and the CPU begins executing the instructions starting from `main`.


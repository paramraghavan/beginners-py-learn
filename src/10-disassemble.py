'''
dis,dis --> displays the python byte code. But this is not the code which runs
inside the CPU - that is the assembly code. To get to assembly code - Compile python to C,
using Cython, then use a C compiler of your choice to get it down to assembly.
'''

import dis


def add_numbers(a,b):
    c = a + b
    return c


dis.dis(add_numbers)
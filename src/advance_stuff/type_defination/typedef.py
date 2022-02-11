'''

Note The Python runtime does not enforce function and variable type annotations. They can be
used by third party tools such as type checkers, IDEs, linters, etc.

Important things to note about type hints:
- They are not enforced at build or run time in any way by Python
- Instead used by type checkers / linters (like mypy or pyright) and IDEs

# In Python 3.8 and earlier, the name of the collection type is
# capitalized, and the type is imported from the 'typing' module
x: List[int] = [1]
x: Set[int] = {6, 7}

https://docs.python.org/3/library/typing.html
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html


# In Python 3.8 and earlier, the name of the collection type is
# capitalized, and the type is imported from the 'typing' module -->  introduced in Python 3.5
x: List[int] = [1]
x: Set[int] = {6, 7}

# For collections, the type of the collection item is in brackets
# (Python 3.9+)
x: list[int] = [1]
x: set[int] = {6, 7}

https://www.python.org/dev/peps/pep-0484/
'''

from typing import List, Set, Dict, Tuple, Optional, Iterator

def greeting(name: str) -> str:
    return 'Hello ' + name

# This is how you annotate a function definition
def stringify(num: int) -> str:
    return str(num)

# And here's how you specify multiple arguments
def plus(num1: int, num2: int) -> int:
    return num1 + num2

number = int
def increment_val(count:number) -> number:
    return count +1

Vector = List[float]
def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

# A generator function that yields ints is secretly just a function that
# returns an iterator of ints, so that's how we annotate it
def g(n: int) -> Iterator[int]:
    i = 0
    while i < n:
        yield i
        i += 1

from typing import Union

def square(number: Union[int, float]) -> Union[int, float]:
    return number ** 2




if __name__ == '__main__':
    print(greeting('Python'))
    print(stringify(23))
    print(increment_val(11))
    # typechecks; a list of floats qualifies as a Vector.
    new_vector = scale(2.0, [1.0, -4.2, 5.4])
    print(new_vector)

    for i in g(10):
        print(i)

    print(square(4.3))
# Map  
map(func, *iterables) --> map object
 > Make an iterator that computes the function using arguments from
 each of the iterables.  Stops when the shortest iterable is exhausted.
return a map object, to make it meaningful wrap this returned object in a list 
 
 
## One iterator parameter 
```
langs = ['spark', 'java', 'python', 'scala']
upper_langs = map(str.upper , langs)
print(list(upper_langs))
# ['SPARK', 'JAVA', 'PYTHON', 'SCALA']
```

## More than one iterator parameters
```
my_strings = ['a', 'b', 'c', 'd', 'e']
my_numbers = [1, 2, 3, 4, 5]
results = list(map(lambda x, y: (x, y), my_strings, my_numbers))
# [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
```

# Filter
 filter(function or None, iterable) --> filter object
  > Return an iterator yielding those items of iterable for which function(item)
   is true. If function is None, return the items that are true.

## example
```python
marks=[50,70,65,99,15,31,91, 49]
def student_with_marks_grtr_than_70(mark):
 return mark > 70
# [99] 
 
list(filter(student_with_marks_grtr_than_70, marks))

marks=[50,' ',65,None,33,31,33, 49]
list(filter(None, marks))
# [50, ' ', 65, 33, 31, 33, 49]

```

# Reduce
 reduce(function, sequence[, initial]) -> value

 >  Apply a **function of two arguments** cumulatively to the items of a sequence,
    from left to right, so as to reduce the sequence to a single value.
    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
    ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
    of the sequence in the calculation, and serves as a default when the
    sequence is empty.
    
# Example
```python
from functools import reduce
numbers = [7,8,3,11,15,20,23,24,25]

def sum2(first, second):
 return first + second
 
reduce(sum2,numbers)
#136
```

#class map in module builtins, map returns iterables
# and we can pass iterables to list to get the result list back

langs = ['spark', 'java', 'python', 'scala']
capitalize_langs = map(str.capitalize , langs)
print(list(capitalize_langs))
# ['Spark', 'Java', 'Python', 'Scala']

my_strings = ['One', 'Two', 'Three', 'Four', 'Five']
my_numbers = [1, 2, 3, 4, 5]
results = list(map(lambda x, y: (x, y), my_numbers, my_strings))
print(results)
# [(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')]

#class filter in module builtins, filter returns iterables
# and we can pass iterables to list to get the result list back
marks = [50, 70, 65, 99, 15, 31, 49]
def student_pass_grade_check(mark):
    return mark >= 70
pass_marks = filter(student_pass_grade_check, marks)
print(list(pass_marks))    
#[70, 99]


```
reduce is not builtin  like map and filter, need to import module functools
from functools import reduce

reduce(...)
    reduce(function, sequence[, initial]) -> value
    
    Apply a function of two arguments cumulatively to the items of a sequence,
    from left to right, so as to reduce the sequence to a single value.
    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
    ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
    of the sequence in the calculation, and serves as a default when the
    sequence is empty.
'''

from functools import reduce
numbers = [7, 8, 3, 11, 15, 20]
def sum2(first, second):
    return first + second
val = reduce(sum2, numbers)
print(val)
# 64

#using intial value with reduce
from functools import reduce
numbers = [7, 8, 3, 11, 15, 20]
def sum2(first, second):
    return first + second
val = reduce(sum2, numbers, 100)
print(val)
# 164


    

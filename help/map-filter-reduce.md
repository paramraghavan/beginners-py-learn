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

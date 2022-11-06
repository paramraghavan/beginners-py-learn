
# Help
```python
dir() # lists all the attributes of dir, but not that useful
s = 'help'
dir(s) #prints all the attributes of the string class
dir(__builtins__) # shows all the methos for str class
help(str)
help(str.lower)  
```  

# Python Operators to perform different operations on variables.
```python
x=5
y=10

### Arithmetic Operators:
x +y --addition
x - y Substraction
x * y Multiplication
x / y Division
x % y Modulus

### Assignment Operators:
x = 1
x += 1
x -= 1
x *= 1

### Comparisin Operator:
x == y
x != y
x > y
x < y

### Logical Operator:
x< 5 and x < 10
x < 5 or x > 4
not(x< 5 and x < 10)
 
### Identity Operator:
x=[1,2,3]
y=x.copy() # makes a shallow copy, works for array
x is y #output :False but x == y output is True
print(f' id of x {id(x)},  id of y: {id(y)}') # id's will be different

x=[1,2,3]
y=x
x is y # true,as x and y have the same id
print(f' id of x {id(x)},  id of y: {id(y)}') # x and y will have same id's


### Membership Operator:
x in y #output :False but x == y output is True
x not in y
1 in y # true
```

# Modules in python

### Built-in Modules
There are several built-in modules in Python. We can directly used the built-in methods with out importing its modules,
if they are available in global namespace. Example map, filter, str etc.

```python
#Get all the builtins in Python
dir(__builtins__)
'''

Some built-in methods are need to be imported like time, datetime etc.
```python
import time
time.sleep(5)

import sys
# Find out all the sys built in modules
sys.builtin_module_names

#Find out where sys is located
sys.prefix

### Using the dir() Function
# We can use dir() built-in function to list all the function names (or variable names) in a module. 

import time
dir(time)
help(time.sleep)
```

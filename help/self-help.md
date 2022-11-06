
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
x is not y 

x=[1,2,3]
y=x
x is y 

### Membership Operator:
x in y
x not in y
```

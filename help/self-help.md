
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

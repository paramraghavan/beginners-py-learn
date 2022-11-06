# Numeric Types:
Python 2.x supports 4 built-in numeric types - int, long, float and complex. 
Of these, the long type has been dropped in Python 3.x - **the int type is now of unlimited length by default.**

### Int
a = 10
type(a)
<class 'int'>

### Float
a = 10.0
type(a)
<class 'float'>

### Complex
a = 3.14j
type(a)
<class 'complex'> 

### Delete object
del a

### Formatting Float
num=10
fl = f'{num :.2f}'
print(fl)

### Casting
In general, the number types are automatically 'up cast' in this order:
Int → Float → Complex. The farther to the right you go, the higher the precedence.

int(), float(), str()

int(1.0)  
int("3")
type(int("3"))
float(1)
float("3")
str(1)
type(str(1)


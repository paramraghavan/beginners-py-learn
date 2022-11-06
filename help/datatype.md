# Datatypes
## Numeric Types:
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

```python
int(1.0)  
int("3")
type(int("3"))
float(1)
float("3")
str(1)
type(str(1)
```

## List

### Updating List. We can also use append method.
```python
lst = ['a','b','c', 'd', 'e']
lst[0]='x'
lst.appned('f')
```

### Delete List Elements. We can also use remove() methods.
del lst[1]

### Length
len(lst)

### Concat
```python
lst1=[1,2,3]
lst2=[3,4,5]
lst1 + lst2

### Membership
lst=[1,2,3,4,5]
3 in lst

### Repetition
lst * 3

### Iteration (For, while Loop or List Comprehension)
#For loop
for i in lst:
	print(i)  

#While Loop
lst = ["apple", "banana", "cherry"]
i = 0
while i < len(lst):
  print(lst[i])
  i = i + 1
```

# List Compression
```python
lst = [1,2,3,4,5]
[x+1 for x in lst]

days= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
lst = [x for x in days if "e" in x]
lst = [x for x in range(15) if x < 3]
lst = [x.upper() for x in days]
lst = ['day' for x in days]
```

### Slicing/Dicing
```python
lst = ['a', 'c', 'd', 'e','f','g','h']
lst[::-1] # reverse list, ['h', 'g', 'f', 'e', 'd', 'c', 'a']
lst[-2]
lst[-3]
lst[-3:]
lst[::-1]
lst[::-6]
lst[::-2] # ['h','f','d','a']
```

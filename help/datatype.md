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
type(str(1))
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
lst1 = [x+1 for x in lst]

days= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
lst = [x for x in days if "e" in x]
lst = [x for x in range(15) if x < 3]
lst = [x.upper() for x in days]
lst = ['day' for x in days]
```

### Concat List as str
```python
lst = ["apple", "banana", "cherry"]
' '.join(lst) # 'apple banana cherry'
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

### Built-in methods that can be applied to list(__builtins__)
```
len
max
min
list
```

### List Methods(dir)
```python
# append() Adds an element at the end of the list
lst = ['a', 'b', 'c', 'd']
lst.append('e')
print(lst)
```

clear()	-->Removes all the elements from the list. Empty List.(Version 3.3)

del keyword delete the list completely.
```python
lst=[1,2,3]
lst.clear()
print(lst)
```
```python
# copy()	--> Returns a copy of the list. Both will have different address id. (Version 3.3)
#Copy a list
list1=["apple", "banana", "cherry"]
list2 = list1  #Copy a list but both point to the same location
id(list1) #Memory ID
id(list2) # Memory ID
#Memory ID of both list 1 and list2 will be same as both are referencing to the same location.
#So changes made to list1 will reflect to list2 and vice versa
    
#Use copy() method
#Memory ID will be different for both the lists.
list2 = list1.copy()
#Also we can use list() method. Memory ID will be different for both the lists.
list2 = list(list1)

# count()	--> Returns the number of elements with the specified value. 
my_list = [1,2,3,4,5,1,2,3]
my_list.count(3) # --> 2

# index(start,stop) -->Returns the index of the first element with the specified value.
#Find the index of an element
my_list = ['a','b','c','d','e']
print(my_list.index('b'))
#Index of Element starting with 2
print(my_list.index('c',2)) 

# # pop()-->Removes the element at the specified position
my_list = [1,2,3,4,5]
#By Default Last Element is deleted
my_list.pop()
#Delete the Second Position Element
my_list.pop(2)
my_list

# remove()-->Removes the item with the specified value
lst = ['a','b','c','d','e']
lst.remove('b')
lst

# reverse()-->Reverses the order of the list
lst=[5,4,-10,15,1]
lst.reverse()   #The parent list will be reverse

#Using Python Built-in functions
list(reversed(lst))   #Parent list will not change

#Also below will work.
lst[::-1]

#help(lst.sort)
#sort(reverse=True)-->Sorts the list
lst.sort()

### sorted() function
# sorted is used to sort any sequence
# sorted(iterable,key, reverse) #Last 2 parameters are optional
# Returns a list

list=[5,3,9,11,2,27]
print(sorted(list))

list = ['Python','Spark','Java','C']
print(sorted(list, key=len))
print(sorted(list, key=len),reverse=True)

list = [(3, 5, 8), (6, 2, 8), (2, 9, 4), (6, 8, 5)]
sorted(list, key=lambda x: x[1])
## output
## [(6, 2, 8), (3, 5, 8), (6, 8, 5), (2, 9, 4)]

```





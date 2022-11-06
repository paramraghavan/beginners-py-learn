# Tuples:
 - Immutable 
 - Ordered. Once a tuple is created, you cannot add items to it. Tuples are unchangeable.
 - Are faster than lists.

### How to Create
```
Create tuples with round brackets.
     t = ('a','b','c','a')
     t= () #Empty Tuple
Tuple containing single element – Put a comma after the first element.
       t =(10,).
Like lists, tuples can also be sliced, concatenated and membership.

Methods dir():
t=(1,2,3,4,5,1)
count() -->Returns the number of times a specified value occurs in a tuple
t.count(1) #2

index() -->Searches the tuple for a specified value and returns the position of where it was found
t.index(3)
```

# Set
 - Unordered : No Index
 - Unchangeable: Elements can be added(add()) or deleted(remove()) but can’t changed.
 - Duplicates Not Allowed.

### show that duplicates have been removed
```
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)                      
```

### membership testing
```
'orange' in basket                 
# True
```

### Support Math operations like union, intersection, difference, symmetric difference etc
```
a = set('abracadabra')
b = set('alacazam')
a                                  # unique letters in a
a | b                              # letters in a or b or both
a & b                              # letters in both a and b
a ^ b                              # letters in a or b but not both
```

### Support List comprehensions
```
{x for x in 'abracadabra' if x not in 'abc'}
```

### Set functions(dir():

s1 = {1,2,3,4,5}
s2 = {4,5,6,7,8}

- add 
 s1.add(6))

- difference
s1.difference(s2)
- difference_update (The output will be updated to the first set)
s1.difference_update(s2)

-symmetric_difference
s1.symmetric_difference(s2)

-symmetric_difference_update
s1.symmetric_difference_update(s2)

-Intersection
```
s1.intersection(s2)
intersection_update
s1.intersection_update(s2)
```

- union
s1.union(s2)

- Discard (Remove an element from a set if it is a member. If the element is not a member, do nothing)
s1.discard(10)

- Isdisjoint
s1.isdisjoint(s2)
- issubset
s1.issubset(s2)
- Issuperset
s1.issuperset(s2)

```
pop
remove
clear
copy
update
```

## Dictionary
```
Dictionaries: We can use Dictionaries to store data in key:value pairs.
  -- Changable
  -- No Duplicates
  -- Ordered (As of Python version 3.7, dictionaries are ordered. In Python 3.6 and earlier, dictionaries are not-ordered.)

###
flowers = {'rose' : 'red', 'hibiscus' : 'orange'}
flowers['lavendar'] = 'Purple'
flowers['Lily'] = 'Green'
del flowers['hibiscus']
	
### Length
len(flowers)	

### Accessing Items
flowers['rose']
or
flowers.get("rose")

###Get Keys and Values
flowers.keys()
flowers.values()
flowers.items() #Return each item in a dictionary, as tuples in a list.

### Check if key exists
'rose' in flowers

### Loop
# same as flowers.keys()
for x in flowers:
	print(x)
	
for x in flowers.values():
	print(x)
	
for x in flowers.keys():
	print(x)
	
for x in flowers.items():
	print(f'key: {x[0]},  value: {x[1]}')
	

### Functions

#The clear() method empties the dictionary.
flowers.clear()

# Copy a Dictionary
Copy a Dictionary
dict2 = dict1 #Problem dict2 will only be a reference to dict1, and changes made in dict1 will automatically also be made in dict2.
dict2 = dict1.copy()

#fromkeys()
x = ('key1', 'key2', 'key3')
y = 10

dict.fromkeys(x, y)

print(thisdict)

#The pop() method removes the item with the specified key name:
flowers.pop('lily')
#The popitem() method removes the last inserted item (in versions before 3.7, a random item is removed instead):
flowers.popitem('lily')

#setdefault()
Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
flowers.setdefault('rose','white')

# Update
flowers['rose'] = 'white'
Or
flowers.update({"rose" : "black"})

### Delete an Item
#The del keyword removes the item with the specified key name:
del flowers['rose']

```






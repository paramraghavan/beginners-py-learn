
numbers = [1,2,3,4,5]

# see contents of the array
print(numbers)

# length of the array
print(len(numbers))

#add to array
numbers.append(6)



namelist = []
#namelist = list()

# add names
namelist.append('name')

name = input("Enter your name: ")
if name in namelist:
    print("I know you!")
else:
    print("Sorry, I don't know who you are :(")


#Advanced - append vs extend
x = [1, 2, 3]
x.append([4, 5])
print(x)

y = [1, 2, 3]
y.extend([4, 5])
print(y)

a = [1, 2, 3]
b = a.copy()

print(b)

b.append(4)
# note b and a
print(b)
print(a)

'''
Tuples
Tuples are a lot like lists, but they're immutable so they can't be
changed in-place. We create them like lists, but with () instead of [].
'''
thing = (1, 2, 3)
print(thing)
for item in thing:
    print(item)
#try
thing.append(4)


numbers = [1,2,3,4,5]

# see contents of the array
print(numbers)

# length of the array
print(len(numbers))

#add to array
numbers.append(6)

# slicing
# variable[start:stop] returns the portion of the variable that
# starts with position start, and up to but not including position stop.
# see more https://towardsdatascience.com/a-skill-to-master-in-python-d6054394e073
numbers_sliced = numbers[1:3]
print(f' numbers_sliced : {numbers_sliced}')

num_list = [0,5,10,15,20,25,30,35,40]
num_list = num_list[::2]
# result --> num_list : [0, 10, 20, 30, 40]
print(f' num_list : {num_list}')

num_list = [0,5,10,15,20,25,30,35,40]
num_list = num_list[::-1]
# reverses the list result --> num_list : [40, 35, 30, 25, 20, 15, 10, 5, 0]
print(f' num_list : {num_list}')


namelist = []
#namelist = list()

# add names
namelist.append('python')

name = input("Enter your name[enter 'python' for match]: ")
if name in namelist:
    print("I know you! : {name}")
else:
    print(f"Sorry, I don't know who you are : {name}")


#Advanced - append vs extend
x = [1, 2, 3]
x.append([4, 5])
print(f'append list: {x}')

y = [1, 2, 3]
y.extend([4, 5])
print(f'extend list: {y}')

print(f'add list: {[*x,*y]}')


a = [1, 2, 3]
b = a.copy()

print(f'a.copy into  b : {b}')
b.append(4)
# note b and a
print(f'note b after b.append : {b}')
print(f'note a : {a}')

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

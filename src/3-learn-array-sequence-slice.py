'''
deleting a list using slice
Note: Strings and tuples are not mutable. Thus we can not edit or mutate them like we can with lists.
'''

num_list = [0,5,10,15,20,25,30,35,40]
del num_list[2:5]
# result [0,5,25,30,35,40]
print(f'current list is ; {num_list}')

'''
Slicing Strings vs. Lists
Slicing a list will return a copy of that list and not a reference to the original list.
We can see this here: if we assign our list slice to another list, since the list slice 
returns a copy and not a reference to the original list, we can modify the new list
(since lists are mutable) without affecting the original list:
'''

# lists
num_list = [0,5,10,15,20,25,30,35,40]
# assign a slice of num_list to new_list
new_list = num_list[2:5]
new_list
#[10,15,20]
# replace the third element of new_list with 3
new_list[2] = 3
# new_list changes
new_list
#[10,15,3]

# Note the original num_list remains the same
num_list
#[0,5,10,15,20,25,30,35,40]

'''
In contrast, when we slice a string, a reference to the original string 
object is returned, and not a copy. And remember, strings are not mutable

We can use Python’s identity operator (is) and the equality operator (==) to confirm that 
slicing a list returns a copy or a different object than the original list, but slicing a 
string returns a reference to the original string object.

The equality operator (==) checks if the values are equal. The identity operator 
(is) checks if the two variables point to the same object in memory.
'''

# Lists:
num_list = [0,5,10,15,20,25,30,35,40]
num_list == num_list[:]
#True
num_list is num_list[:]
#False

#Strings:
word = 'Python'
word == word[:]
#True
word is word[:]
#True

'''
Slice Function:

'''

# num_list[:8] is equivalent to num_list[slice(8)]
# num_list[2:8] is equivalent to num_list[slice(2,8,None)]
# num_list[2:] is equivalent to num_list[slice(2,None,None)]

'''
Why use slice
Using the slice function to create a slice object can be useful if we want to save a 
specific slice object and use it multiple times. We can do so by first instantiating a slice
object and assigning it to a variable, and then using that variable within square brackets.
See example
'''

num_list = [0,5,10,15,20,25,30,35,40]
evens = slice(None,None,2)
odds = slice(1,None,2)

print(f'Even list {num_list[evens]}')
print(f'Odd list {num_list[odds]}')


print(f'Sum of even list {sum(num_list[evens])}')
print(f'Sum of odd list {sum(num_list[odds])}')


'''
Exercise1:
Exercise check if a string is a palindrome  using slice.
A string is a palindrome if the reverse of the string is identical
to the original string. For example, ‘civic’ is a palindrome, but 
‘radio’ is not, since the reverse of ‘radio’ is ‘oidar’, but 
the reverse of ‘civic’ is ‘civic’.

'''
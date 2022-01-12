'''

StringIO performing almost the same as +=. I was expecting it to perform at least twice as
well since it’s referenced in the Python 3 docs alongside .join as a way to concatenate
str objects.

join is the fastest

ref: https://betterprogramming.pub/python-and-string-concatenation-31772a10fed
'''


from io import StringIO

mylist = ["hello ", "here ", "is ", "a an example ", "of ", "Stringbuilder"]
buffer = StringIO()
for i in range(len(mylist)):
    buffer.write(mylist[i])
print(buffer.getvalue())


'''
join vs +
join is preferred  mechanism to concatenate strings in python as it is was faster than '+'
'''

'''
problem with +=, +
Since strings are immutable, whenever you join a string to another one it’s creating a new
 string. With the strings getting bigger and bigger, more data needs to be copied in order 
 to create these bigger string
'''

name = 'Guido van Rossum'
year = 1991
val = 'Python was created by ' + name + ' and released in ' + year

'''
f-string
'''
name = 'Guido van Rossum'
year = 1991
val = f'Python was created by {name} and released in {year}'


'''
join()
When you want to join multiple strings stored in a list, the easiest option is to use the join() method.
Note:
Using  the join() method can be 4 times faster than using + to join the strings in the list.
ref: https://towardsdatascience.com/do-not-use-to-join-strings-in-python-f89908307273
'''

str1 = "I love "
str2 = "Python."
val = ''.join([str1, str2])


words = ['Python', 'was', 'created', 'by', 'Guido', 'van', 'Rossum', 'and', 'first', 'released', 'in', '1991']
val = ' '.join(words)

'''
str.format( )
We can use the str.format() to concatenate strings in Python. We only need to insert 
curly braces {} for every variable we want to add inside a string
'''
name = 'Guido van Rossum'
year = 1991

val =  "Python was created by {} and released in {}".format(name, year)





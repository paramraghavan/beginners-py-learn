'''
Instead of adding line1, line2 to mymsg individually, use list and join.
'''

# Don't
mymsg='line1\n'
mymsg+='line2\n'


# Better choice:
mymsg=['line1','line2']
'\n'.join(mymsg)


'''
Avoid using the + operator for strings
Don’t use the + operator for concatenation if you can avoid it. Because strings are immutable, every time you add an element to a string, 
Python creates a new string and a new address. This means that new memory needs to be allocated each time the string is altered
'''
mymsg = ' my '
# Don't
msg='hello'+mymsg+'world'


# Better
msg='hello %s world' % mymsg
msg= f'hello {mymsg} world'


'''
Use Generators
Generators allow you to create a function that returns one item at a time rather than all the items at once.
This means that if you have a large dataset, you don’t have to wait for the entire dataset to be accessible.
'''
def __iter__(self):
    return self._generator()


def _generator(self):
    for itm in self.items():
        yield itm

# Put evaluations outside the loop

'''
If you are iterating through data, you can use the cached version of the regex.

import re
match_regex=re.compile("foo|bar")

# some string
big_it = None

for i in big_it:
    m = match_regex.search(i)
    pass
'''

'''
Assign a function to a local variable, especially when invoking inside a loop.
Python accesses local variables much more efficiently than global variables. 
Assign functions to local variables then use them.

myLocalFunc=myObj.func
for i in range(n):
    myLocalFunc(i)

'''


'''
Use built-in functions and libraries
Use built-in functions and libraries whenever you can. Built-in functions are often implemented using the best memory usage practices.
'''

# Dont' do this
oldList =  ['abcSSS', 'ererWWWWW']
mylist=[]
for myword in oldList:
      mylist.append(myword.lower())

print(mylist)

# Better choice
mylist_better = map(str.lower, oldList)
print(list(mylist_better))
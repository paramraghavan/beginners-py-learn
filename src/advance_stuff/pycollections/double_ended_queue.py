'''
It's also possible to do these things in the beginning of a list, 
but lists were not designed to be used that way and it would be slow if our list would be big. 
The pycollections.deque class makes appending and popping from both ends easy and fast.
 It works just like lists, but it also has appendleft and popleft methods.
'''

import collections

names = collections.deque(['theelous3', 'Nitori', 'RubyPinch'])
print(names)

names.appendleft('wub_wub')
names.append('goldfish')
print(names)

value = names.popleft()
print(value)
# default pop is pop right
value = names.pop()
print(value)
print(names)

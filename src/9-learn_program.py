'''
Roll your dice
'''

# to get help
help(str.split)

import random

x= ''
while x != 'xit':
    '''
    randint - A random integer takes in range [start, end] including the end points.
    every time we execute randint it will give random values from 1 thru 6 including 1 and 6
    '''
    print(random.randint(1, 6))
    x= input('Roll the dice again, xit to Exit')

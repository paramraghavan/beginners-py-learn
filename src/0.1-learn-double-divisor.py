'''
The Double Division operator in Python returns the floor value for both integer
and floating-point arguments after division.
'''
length = 4
middle = (length+1)/2 #2.5
# using divisor
print(f'middle/ : {middle}')
# using double divisor
middle = (length+1)//2 #2
print(f'middle// : {middle}')

# .9 using divisor
print(f'/ : {(.8+1)/2}')
# .6
print(f'/ : {(.2+1)/2}')

# using double divisor
# 0, rounded down to 0
print(f'// : {(.8+1)//2}')
# 0, rounded down to 0
print(f'// : {(.2+1)//2}')

# checkout math.ceil

elem = { 'TableList' : [ \
                 {'Name': 'table1'},  {'Name': 'table2'},  {'Name': 'table3'} \
                ] \
}

'''
see the usage of for loop with the square brackets,
building a array of dictionary items

Result:
[{'name': 'table1'}, {'name': 'table2'}, {'name': 'table3'}]
'''
tables = []
tables += [
                {
                    "name": table["Name"],
                }
                for table in elem["TableList"]
            ]

print(tables)


print('Strings are immutable')
'''
Strings are immutable once you create a string you cannot change it.
function 'id' Returns the identity of an object.
ref: https://www.geeksforgeeks.org/is-python-call-by-reference-or-call-by-value/
'''

'''
As strings are immutable the string 'first' has the same address location 
even when it is assigned to a new variable.
Let's check it out using function id
'''
a = "first"
b = "first"

# Returns the actual location
# where the variable is stored
print(f'address of a first: {id(a)}')

# Returns the actual location
# where the variable is stored
print(f'address of b first: {id(b)}')

# Returns true if both the variables
# are stored in same location
# And this returns trus
print(f'Are strings a and b both are one and the same? {a is b}')

print('')

print('Lists are mutable')

'''
Now let's use list. list's are immutable so in this case new arrays are created every time
and assigned to a and b. But a and c are the one and the same immutable list, so they will 
have the same address assigned
'''
a = [10, 20, 30]
b = [10, 20, 30]
c = a

# return the location
# where the variable
# is stored
print(f'address of list a {id(a)}')

# return the location
# where the variable
# is stored
print(f'address of list b {id(b)}')

# return the location
# where the variable
# is stored
print(f'address of list c {id(c)}')


# Returns true if both the variables a and b
# are stored in or point to the different location/address
# And this returns false
print(f'Are lists a and b both are one and the same? {a is b}')

# Returns true if both the variables a and c
# are stored in or point to the same location/address
# And this returns true
print(f'Are lists a and c both are one and the same? {a is c}')

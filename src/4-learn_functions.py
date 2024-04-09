'''
function() calls a function without any arguments, and function(1, 2, 3)
 calls a function with 1, 2 and 3 as arguments.
When a function is called, it does something and returns something.
function(arguments) is "replaced" with the return value in the code that called it. For example,
stuff = function() calls a function, and then does stuff = the_return_value and the return value
ends up in stuff.
Python comes with print and input. They are built-in functions.
Avoid variable names that conflict with built-in functions.

we used functions, print('hello'), here print is a built in function
'''

print(print)

# lets see what print returns
return_value = print('hello')
print(f'return_value: {return_value}')

return_value = print(123)
print(f'return_value: {return_value}')


def add_function(value1, value2):
    total = value1 + value2


return_value = add_function(1,4);
print(f'adding numbers add_function: {return_value}')

def add_function_second(value1, value2):
    total = value1 + value2
    return total

return_value = add_function_second(1,4);
print(f'adding numbers add_function_second: {return_value}')

'''

Multiple return values
Function can take multiple arguments, but they can only return one value. But sometimes it makes sense to return multiple values as well:

def login():
    username = input("Username: ")
    password = input("Password: ")
    # how the heck are we going to return these?
The best solution is to return a tuple of values, and just unpack that wherever the function is called:

def login():
    ...
    return (username, password)

username, password = login()
'''

def login()->tuple[str, str]:
    username = 'user1' #input("Username: ")
    password = 'password' #input("Password: ")

    return (username, password)

username, password = login()
print(80*'-')
print(f'username : {username}, password: {password}')
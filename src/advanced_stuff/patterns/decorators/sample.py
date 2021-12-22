'''
ref: https://www.datacamp.com/community/tutorials/decorators-python
'''


def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper

def say_hi():
    return 'hi there'

decorate = uppercase_decorator(say_hi)
decorate()
print(decorate())

print('----------------------------------------------------------------------------')
print('----------------------------------------------------------------------------')

'''
Here is the decorator annotated as @uppercase_decorator
'''
@uppercase_decorator
def say_hello():
    return 'hello there'

print(say_hello())

print('----------------------------------------------------------------------------')
print('----------------------------------------------------------------------------')

'''
Applying Multiple Decorators to a Single Function
'''
def split_string(function):
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string

    return wrapper


'''
Application of decorators is from the bottom up. 
Had we interchanged the order, we'd have seen an error since lists don't have an upper attribute.
The sentence has first been converted to uppercase and then split into a list.
'''
@split_string        # second applied
@uppercase_decorator # first applied
def say_hello():
    return 'hello there'


print(say_hello())

print('----------------------------------------------------------------------------')
print('----------------------------------------------------------------------------')

'''
 Function defination  with parameters
'''
def decorator_with_arguments(function):
    def wrapper_accepting_arguments(arg1, arg2):
        print("Parameters passed to the function are: {0}, {1}".format(arg1,arg2))
        function(arg1, arg2)
    return wrapper_accepting_arguments


@decorator_with_arguments
def cities(city_one, city_two):
    print("Cities I love are {0} and {1}".format(city_one, city_two))

cities("Duluth", "Leesburg")

print('----------------------------------------------------------------------------')
print('----------------------------------------------------------------------------')

def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(*args,**kwargs):
        print('The positional arguments are', args)
        print('The keyword arguments are', kwargs)
        function_to_decorate(*args, *kwargs)
    return a_wrapper_accepting_arguments


@a_decorator_passing_arguments
def function_with_positional_keyword_arguments(param1, param2, service="glue", region='us-east-1'):
    print("This has both keyword and arguments")
    print(f'param1: {param1} param2: {param2} service: {service} region: {region}')


function_with_positional_keyword_arguments('first-parameter', 'second-parameter')
print('----------------------------------------------------------------------------')
print('----------------------------------------------------------------------------')

function_with_positional_keyword_arguments('first-parameter', 'second-parameter', 's3', 'us-east-2')



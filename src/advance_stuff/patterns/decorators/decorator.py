'''
A decorator is a design pattern that allows a user to add new functionality to an
existing object without modifying its structure.

ref: https://www.geeksforgeeks.org/timing-functions-with-decorators-python/
'''

def my_decorator(func):
	def wrapper_function(*args, **kwargs):
		print("*"*10)
		result = func(*args, **kwargs)
		print("*"*10)
		return result
	return wrapper_function


def say_hello():
	print("Hello Python!")

@my_decorator
def say_bye():
	print("Bye Python!")


# applying decorator literally
say_hello_with_decorator_wrapper = my_decorator(say_hello)
say_hello_with_decorator_wrapper()
print()
print('-----------------------------------')
print()
# applying the decorator  using the @decortor_name  above the say_bye method defination
say_bye()

@my_decorator
def say_hello_param(param_value):
	print(param_value)

say_hello_param('parameter value')

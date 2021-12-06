'''
A decorator is a design pattern that allows a user to add new functionality to an existing object
without modifying its structure.

ref: https://www.geeksforgeeks.org/timing-functions-with-decorators-python/
'''

def my_decorator(func):
	def wrapper_function(*args, **kwargs):
		print("*"*10)
		func(*args, **kwargs)
		print("*"*10)
	return wrapper_function


def say_hello():
	print("Hello Geeks!")

@my_decorator
def say_bye():
	print("Bye Geeks!")


# applying decorator literally
say_hello_with_decorator_wrapper = my_decorator(say_hello)
say_hello_with_decorator_wrapper()
print()
print('-----------------------------------')
print()
# applying the decorator  using the @decortor_name  above the say_bye method defination
say_bye()

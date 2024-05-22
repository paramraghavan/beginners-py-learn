'''
In Python, __call__ and __init__ are special methods that serve different purposes:
__init__
Purpose: The __init__ method initializes an instance of a class. It is called automatically
when a new instance of the class is created. You define the __init__ method to set up the initial state of the object,
such as initializing attributes.
'''

class MyClass:
    def __init__(self, value):
        self.value = value

obj = MyClass(10)  # __init__ is called here
print(obj.value)   # Output: 10

'''
__call__
The __call__ method allows an instance of a class to be called as a function. If a class defines __call__, 
its instances can be called like a regular function. You define the __call__ method to make instances of the class 
callable. This can be useful for creating objects that behave like functions.

Using __call__ without __init__ can be appropriate in certain situations where the object does not require any 
initialization parameters or state setup at the time of its creation.

Use __call__, when the class is designed to be stateless and acts like a simple function.
'''

class MyCallableClass:
    def __init__(self, value):
        self.value = value

    def __call__(self, x):
        return self.value + x

obj = MyCallableClass(10)
result = obj(5)  # __call__ is called here
print(result)    # Output: 15

'''
creating a class that acts as a stateless function, meaning it does not need to maintain or initialize any internal state.
'''
class Adder:
    def __call__(self, x, y):
        return x + y

add = Adder()
result = add(3, 4)  # __call__ is invoked
print(result)       # Output: 7


## utility class
class Printer:
    def __call__(self, message):
        print(message)

printer = Printer()
printer("Hello, World!")  # __call__ is invoked, prints "Hello, World!"

class Multiplier:
    def __call__(self, a, b):
        return a * b

multiply = Multiplier()
result = multiply(5, 6)  # __call__ is invoked
print(result)            # Output: 30

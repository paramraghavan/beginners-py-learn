# method overloading and overriding

## Method Overloading in Python

Method Overloading in Python is a type of Compile-time Polymorphism using which we can define two or more methods in the
same class with the same name but with a different parameter list.

We cannot perform method overloading in the Python programming language as everything is considered an object in Python.
Out of all the definitions with the same name, it uses the latest definition for the method. Hence, we can define
numerous methods with the same name, but we can only use the latest defined method.

In Python, we can make our code have the same features as overloaded functions by defining a method in such a way that
there exists more than one way to call it. See example [overloading.py](overloading.py)


## Method Overriding

Method Overriding is a type of Run-time Polymorphism. A child class method overrides (or provides its implementation)
the parent class method of the same name, parameters, and return type. It is used to over-write (redefine) a parent
class method in the derived class.  See example [overriding.py](overriding.py)




>
> Reference: https://www.scaler.com/topics/overloading-and-overriding-in-python/
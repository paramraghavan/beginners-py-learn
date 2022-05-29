# Source: Class and Instance Variables
# https://docs.python.org/2/tutorial/classes.html#class-and-instance-variables

'''
In the absence of any other superclasses that you specifically want to inherit from, the superclass should always be object,
which is the root of all classes in Python.
object is technically the root of "new-style" classes in Python.
But, if you don't explicitly use the word object when creating classes, then Python 3.x implicitly
inherits from the **object superclass**.

1. Class variable
2. instance variable
3. MyClass explicitly inherits from the **object superclass**

Python class variables are declared within a class and their values are the same across all instances of a class. 
Python instance variables can have different values across multiple instances of a class. Class variables share 
the same value among all instances of the class

'''''


class MyClass(object):
    # class variable
    my_CLS_var = 10

    # sets "init'ial" state to objects/instances, use self argument
    def __init__(self):
        # self usage => instance variable (per object)
        self.my_OBJ_var = 15

        # also possible, class name is used => init class variable
        MyClass.my_CLS_var = 20

    def printValues(self):
        # PRINTS    10    (class variable)
        print(11 * '*' + '   NOTE    ' + 11 * '*')
        print(f'printValues-->self.my_OBJ_var: {self.my_OBJ_var}')
        print(f'printValues--> Note Class viaraible accessed via object self(instance)-->self.my_CLS_var: {self.my_CLS_var}')
        print(f'printValues-->MyClass.my_CLS_var: {MyClass.my_CLS_var}')
        print(11 * '*' + '     -    ' + 11 * '*')

def run_example_func():
    # PRINTS    10    (class variable)
    print(f'run_example_func-->MyClass not initialized yet, MyClass.my_CLS_var: {MyClass.my_CLS_var}')

    # executes __init__ for obj1 instance
    # NOTE: __init__ changes class variable above
    obj1 = MyClass()

    obj1.printValues()

    # PRINTS    15    (instance variable)
    print(f'run_example_func-->obj1.my_OBJ_var: {obj1.my_OBJ_var}')

    # Note, PRINTS    20
    print(f'run_example_func-->Note Class variable accessed via object instance--> obj1.my_CLS_var: {obj1.my_CLS_var}')

    # PRINTS    20    (class variable, changed value)
    print(f'run_example_func-->MyClass.my_CLS_var : {MyClass.my_CLS_var}')


run_example_func()

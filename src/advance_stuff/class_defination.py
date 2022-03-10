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


def run_example_func():
    # PRINTS    10    (class variable)
    print(MyClass.my_CLS_var)

    # executes __init__ for obj1 instance
    # NOTE: __init__ changes class variable above
    obj1 = MyClass()

    # PRINTS    15    (instance variable)
    print(obj1.my_OBJ_var)

    # PRINTS    20    (class variable, changed value)
    print(MyClass.my_CLS_var)


run_example_func()
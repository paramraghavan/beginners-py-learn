# Source: Class and Instance Variables
# https://docs.python.org/2/tutorial/classes.html#class-and-instance-variables


'''
1. Class variable
2. instance variable

'''

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
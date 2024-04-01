# Define a metaclass that ensures all classes have a 'required_method'
class RequiredMethodMeta(type):
    """
    In this example, the RequiredMethodMeta metaclass checks that any class using it
     (or any subclass of a class using it) implements a method called required_method. If a
     class is missing this method, a TypeError is raised
    """

    def __init__(cls, name, bases, attrs):
        if 'required_method' not in attrs:
            raise TypeError(f'Class {name} is missing implementation of required_method')
        super().__init__(name, bases, attrs)

# Use the metaclass to create a base class
class BaseClass(metaclass=RequiredMethodMeta):
    def required_method(self):
        pass

# This class is fine because it has 'required_method'
class GoodSubClass(BaseClass):
    def required_method(self):
        print("Implementing required method")

# This class will raise a TypeError because it's missing 'required_method'
class BadSubClass(BaseClass):
    pass

if __name__ == '__main__':
    # all good as required_method is implemented.
    good = GoodSubClass()
    # throws exception TypeError: Class BadSubClass is missing implementation of required_method
    bad = BadSubClass()
'''
Protected variables are those data members of a class that can be accessed within the class and the classes derived from that class.
In Python, there is no existence of “Public” instance variables. However, we use underscore ‘_’ symbol to determine the access control of a
data member in a class. Any member prefixed with an underscore should be treated as a non-public part of the API or any Python code,
whether it is a function, a method or a data member.
'''''


'''
In the absence of any other superclasses that you specifically want to inherit from, the superclass should always be object,
which is the root of all classes in Python.
object is technically the root of "new-style" classes in Python.
But, if you don't explicitly use the word object when creating classes, then Python 3.x implicitly
inherits from the **object superclass**.
'''''



# Defining a class
# init is short for initialization. It is a constructor which gets called when you make an instance of the class and it is not necessary.
# Note here no __init__
# Here Geek explicitly inherits from the **object superclass**
class Geek(object):
    ## protected data members
    _name = "R2J"
    _roll = 1706256

    # public member function
    def displayNameAndRoll(self):
        # accessing protected data members
        print("Name: ", self._name)
        print("Roll: ", self._roll)

    # creating objects of the class


obj = Geek()

# calling public member
# functions of the class
obj.displayNameAndRoll()

'''
the protected variables _length and _breadth of the super class Shape are accessed within the class by a member function displaySides() 
and can be accessed from class Rectangle which is derived from the Shape class. The member function calculateArea() of class Rectangle accesses 
the protected data members _length and _breadth of the super class Shape to calculate the area of the rectangle.
'''


# program to illustrate protected
# data members in a class

# here Shape implicitly inherits from the **object superclass**
# super class
class Shape:

    # constructor
    def __init__(self, length, breadth):
        self._length = length
        self._breadth = breadth

        # public member function

    def displaySides(self):
        # accessing protected data members
        print("Length: ", self._length)
        print("Breadth: ", self._breadth)

    # derived class


class Rectangle(Shape):

    # constructor
    def __init__(self, length, breadth):
        # Calling the constructor of
        # Super class
        Shape.__init__(self, length, breadth)

        # public member function

    def calculateArea(self):
        # accessing protected data members of super class
        print("Area: ", self._length * self._breadth)

    # creating objects of the


# derived class
obj = Rectangle(80, 50)

# calling derived member
# functions of the class
obj.displaySides()

# calling public member
# functions of the class
obj.calculateArea()

'''
 class variable shared by all instances
 instance variable unique to each instance
'''
class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

d = Dog('Romeo')
e = Dog('Luca')
d.kind
print(80 *'-')
print(f'class variable shared by all instances d.kind --> {d.kind} and e.kind -->  {e.kind}')
print(f'instance variable unique to each instance d.name --> {d.name} and e.name --> {e.name}')


'''
Notes:
https://docs.python.org/3/tutorial/classes.html#class-objects
'''
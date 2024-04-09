# Metaclass ?

A metaclass in Python is a class of a class that defines how a class behaves. A class is an instance of a metaclass. You
typically use a metaclass when you need to control the creation of classes, modify the behavior of classes, or add
functionality to classes.

**Common Uses**

- One common use case for metaclasses is to ensure that all classes of a certain type follow a particular pattern or
  protocol. For example, you might use a metaclass to ensure that all subclasses of a particular base class implement a
  specific set of methods. usecase1
- Singleton pattern implementation. The Singleton pattern ensures that a class has only one instance and provides a
  global point of access to that instance. use_case2

## Base class call the methods in Driver/Child Class

A base class cannot directly access methods of a derived (child) class unless those methods are called within the
derived class itself and the base class has a reference to the derived class instance. However, this is not a common or
recommended practice in object-oriented programming, as it can lead to tight coupling between the base and derived
classes.
See [base_derived.py](base_derived.py)

# ClassMethod vs StaticMethod
In Python, both class methods and static methods are used to define methods that are not tied to any particular instance of a class.
## classmethod
- A classmethod is a method that receives the class as its first argument rather than the instance of the class. It's defined using the @classmethod decorator.
  - First Parameter: cls (the class)
  - Bound to: Class, not the instance
  - Can Modify Class State: Yes, since it has access to the class object
  - Typical Use Cases:
    - Factory methods that create an instance of the class using different parameters than those provided by the constructor.
    - Methods that need to access or modify the class state, such as a global configuration relevant to the entire class.
## Example Date object
```py
class Date(object):
    
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

date2 = Date.from_string('11-09-2012')
is_date = Date.is_date_valid('11-09-2012')
```
In the above example Here we have __init__, a typical initializer of Python class instances, which receives arguments as a typical 
instance method, having the first non-optional argument (self) that holds a reference to a newly created instance.

Let's assume that we want to create a lot of Date class instances having date information coming from an outer source encoded as a string with format 
'dd-mm-yyyy'. Suppose we have to do this in different places in the source code of our project.

So what we must do here is:

Parse a string to receive day, month and year as three integer variables or a 3-item tuple consisting of that variable.
Instantiate Date by passing those values to the initialization call.
This will look like:
```py
day, month, year = map(int, string_date.split('-')) 
date1 = Date(day, month, year)
```
**KindOf Implement Overloading like in Java**
With java can implement such a feature with overloading, but Python lacks this overloading. Instead, we can use classmethod. Let's create another constructor.
```py
    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

date2 = Date.from_string('11-09-2012')
```
Let's look more carefully at the above implementation, and review what advantages we have here:
- We've implemented date string parsing in one place and it's reusable now.
- Encapsulation works fine here (if you think that you could implement string parsing as a single function elsewhere, this solution fits the OOP paradigm far better).
- **cls is the class itself, not an instance of the class**. It's pretty cool because if we inherit our Date class, all children will have from_string defined also.

## staticmethod
A staticmethod does not receive an implicit first argument at all. It's defined using the @staticmethod decorator.

- First Parameter: None
- Bound to: Neither the class nor the instance
- Can Modify Class State: No, unless it explicitly accesses class variables or methods
- Typical Use Cases:
  - Utility functions that perform a task in isolation and do not need to access or modify class or instance state.
  - Functions that are logically related to the class but do not need to access any class-specific data.

```py
#Example
    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

# usage:
is_date = Date.is_date_valid('11-09-2012')
```

ref: https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner

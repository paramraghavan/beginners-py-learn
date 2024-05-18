# __str__

In Python, you can add a __str__ method to your class to define how an instance of the class should be converted to a
string, similar to the toString method in Java. Here's an example:

```python
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

# Creating an instance of the Car class
car = Car("Honda", "Accord", 2003)

# Printing the instance to see the string representation
print(car)
```
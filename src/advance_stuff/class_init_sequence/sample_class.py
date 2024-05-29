class MyClass:
    # Class variable
    class_variable = "I am a class variable"
    map_class_variable = {}

    def __init__(self, instance_variable):
        # Instance variable
        self.instance_variable = instance_variable

    def add_object_to_map(self):
        MyClass.map_class_variable[id(self)] = object()

    @staticmethod
    def get_object_count():
        return len(MyClass.map_class_variable.keys())

    @staticmethod
    def static_method():
        print("I am a static method")

    def instance_method(self):
        print(f"Instance variable: {self.instance_variable}")
        print(f"Class variable: {self.class_variable}")


# Creating an instance of MyClass
obj1 = MyClass("Instance 1 variable")
obj1.add_object_to_map()
obj2 = MyClass("Instance 2 variable")
obj2.add_object_to_map()
obj3 = MyClass("Instance 3 variable")
obj3.add_object_to_map()

print(f'Count of map_class_variable {MyClass.get_object_count()}')
assert MyClass.get_object_count() == 3, "Count of map_class_variable should be 3"

print(80*'#')
# Accessing instance and class variables
print(' Instance Variables')
print(obj1.instance_variable)  # Instance 1 variable
print(obj2.instance_variable)  # Instance 2 variable
print(obj3.instance_variable)  # Instance 3 variable
print(80*'#')
print(' Class Variables')
print(obj1.class_variable)  # I am a class variable
print(obj2.class_variable)  # I am a class variable
print(obj3.class_variable)  # I am a class variable

# Calling static method
print(80*'#')
print('Accessing static method')
MyClass.static_method()  # I am a static method

print(80*'#')
print('Accessing instance method')
# Accessing instance method
obj1.instance_method()


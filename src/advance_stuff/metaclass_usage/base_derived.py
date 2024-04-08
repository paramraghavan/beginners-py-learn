class BaseClass:
    def call_child_method(self, child_instance: 'DerivedClass'):
        if not isinstance(child_instance, DerivedClass):
            raise TypeError("child_instance must be an instance of DerivedClass or its subclass")

        # Call a method of the derived class through the instance
        return child_instance.child_method()

class DerivedClass(BaseClass):
    def child_method(self):
        return "This is a method of the derived class."

class Derived1Class(BaseClass):
    def child_method(self):
        return "This is a method of the derived 1 class."

# Create an instance of the derived class
derived_instance = DerivedClass()
derived_instance_1 = Derived1Class()
# The base class accesses the derived class method through the instance
result = derived_instance.call_child_method(derived_instance)
print(result)  # Output: This is a method of the derived class.

result_1 = derived_instance_1.call_child_method(derived_instance_1)
print(result_1)  # Output: This is a method of the derived class.


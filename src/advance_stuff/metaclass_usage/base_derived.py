class BaseClass:

    def start_process(self):
        print("Running " + str(self))

    def call_child_method(self, child_instance: 'DerivedClass'):
        if not isinstance(child_instance, DerivedClass):
            raise TypeError("\n\nchild_instance must be an instance of DerivedClass or its subclass")

        # Call a method of the derived class through the instance
        return child_instance.child_method()

class DerivedClass(BaseClass):
    def child_method(self):
        return "This is a method of the derived class."

class Derived1Class(BaseClass):
    def child_method_1(self):
        return "This is a method of the derived 1 class."

# Create an instance of the derived class
derived_instance = DerivedClass()
derived_instance_1 = Derived1Class()
derived_instance_2 = Derived1Class() # this will invoke the
# The base class accesses the derived class method through the instance
result = derived_instance.call_child_method(derived_instance)
print(result)  # Output: This is a method of the derived class.
derived_instance.start_process()

derived_instance_1.start_process()


result2 = derived_instance_2.call_child_method(derived_instance_2)
print(result2)  # Output: This is a method of the derived class.
derived_instance_2.start_process()



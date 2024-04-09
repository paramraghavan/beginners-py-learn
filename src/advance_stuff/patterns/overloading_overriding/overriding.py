# Parent Class
class A:
    def first(self):
        print("First function of class A")

    def second(self):
        print('Second function of class A')


# Derived Class
class B(A):
    # Overriden Function
    def first(self):
        print("Redefined function of class A in class B")

    def display(self):
        print('Display Function of Child class')


class C(A):
    """
    Derived Class using base implementation
    """
    def process(self):
        print("process invoked by class C instance")
        self.first()


# Driver Code
if (__name__ == "__main__"):
    # Creating child class object
    child_obj = B()

    # Calling the overridden method
    print("Method Overriding\n")
    child_obj.first()


    # Calling the original Parent class method
    # Using parent class object.
    A().first()

    child_obj_C = C()
    child_obj_C.process()

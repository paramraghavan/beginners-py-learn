'''
he BaseClass constructor accepts a parameter base_param, and the MySingletonImpl class's constructor accepts both value and
base_param parameters. When creating a Singleton instance, the base_param is passed to the BaseClass constructor using
super().__init__(base_param). This way, the Singleton class can pass parameters to the BaseClass while
still enforcing the Singleton pattern.
Singleton is a creational design pattern, which ensures that only one object of its kind exists and provides a single
point of access to it for any other code

'''
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class BaseClass:
    def __init__(self, base_param):
        self.base_param = base_param

    def base_method(self):
        print(f"Method in BaseClass, base_param: {self.base_param}")

    def create(self):
        print('create')

    def update(self):
        print('update')


class SingletonBaseClassImpl(BaseClass, metaclass=SingletonMeta):
    def __init__(self, value, base_param):
        super().__init__(base_param)
        self.value = value



if __name__ == '__main__':
    # Usage
    my_singleton_impl1 = SingletonBaseClassImpl("First Instance", "Base Param 1")
    # new instance will not be created,  my_singleton_impl1 is returned for my_singleton_impl2s
    my_singleton_impl2 = SingletonBaseClassImpl("Second Instance", "Base Param 2")

    print(my_singleton_impl1.value)  # Output: First Instance
    print(my_singleton_impl2.value)  # Output: First Instance

    print(my_singleton_impl1 is my_singleton_impl2)  # Output: True

    my_singleton_impl1.base_method()  # Output: Method in BaseClass, base_param: Base Param 1
    my_singleton_impl2.base_method()  # Output: Method in BaseClass, base_param: Base Param 1

    my_singleton_impl1.create()
    my_singleton_impl2.update()

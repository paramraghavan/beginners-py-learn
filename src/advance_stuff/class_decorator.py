'''
The @classmethod Decorator
This decorator exists so you can create class methods that are passed the actual class object within the function call,
much like self is passed to any other ordinary instance method in a class.

In those instance methods, the self argument is the class instance object itself, which can then be used to act on
instance data. @classmethod methods also have a mandatory first argument,but this argument isn't a class instance,
it's actually the uninstantiated class itself. So, while a typical class method might look like this:

class Student(object):

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

scott = Student('Scott',  'Robinson')

One can still use the same @classmethod for sub-classes as well.

ref: https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/
'''

'''
@classmethod methods also have a mandatory first argument,
but this argument isn't a class instance, it's actually the uninstantiated class itself.
This follows the static factory pattern very well, encapsulating the parsing logic inside of the method itself.
'''

class Student(object):

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    '''
    If a Student object could be serialized in to many different formats. You could use this same strategy to parse them all:
    '''
    @classmethod
    def parse_student_string(cls, name_str):
        first_name, last_name = map(str, name_str.split(' '))
        student = cls(first_name, last_name)
        return student

    # @classmethod
    # def from_json(cls, json_obj):
    #     # parse json...
    #     return student


student_scott = Student.parse_student_string('Scott Robinson')
print(student_scott.first_name, student_scott.last_name)



'''
@staticmethod - contain some type of logic pertaining to the class itself, like a helper or utility method.

The @staticmethod decorator is similar to @classmethod in that it can be called from an uninstantiated class object, although in this case there is no cls parameter passed to its method.
Since no self object is passed either, that means we also don't have access to any instance data, and thus this method can not be called on an instantiated object either.

These types of methods aren't typically meant to create/instantiate objects, but they may contain some type of logic pertaining to the class itself, like a helper or utility method.

class Student(object):

    # Constructor removed for brevity

    @staticmethod
    def is_full_name(name_str):
        names = name_str.split(' ')
        return len(names) > 1

Student.is_full_name('Scott Robinson')   # True
Student.is_full_name('Scott')            # False
'''
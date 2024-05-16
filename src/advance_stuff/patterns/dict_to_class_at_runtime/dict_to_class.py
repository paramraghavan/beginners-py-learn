def dict_to_class(class_name, d):
    # Dynamically create a new class
    new_class = type(class_name, (object,), {})

    # Add dictionary items as attributes
    for key, value in d.items():
        setattr(new_class, key, value)

    return new_class


if __name__ == "__main__":
    # Example dictionary
    student_dict = {
        'name': 'John Doe',
        'age': 18,
        'email': 'johndoe@example.com',
        'college':'GeorgiaTech'
    }

    # Convert dictionary to class
    Student = dict_to_class('Student', student_dict)

    # Create an instance of the class
    student_instance = Student()

    # Access attributes
    print(student_instance.name)  # Output: John Doe
    print(student_instance.age)  # Output: 18
    print(student_instance.email)  # Output: johndoe@example.com
    print(student_instance.college)

    # List all attributes of the class (including methods and built-in attributes)
    class_attributes = dir(Student)
    print("Class attributes:")
    print(class_attributes)

    # List all attributes of the instance (including methods and built-in attributes)
    instance_attributes = dir(student_instance)
    print("\nInstance attributes:")
    print(instance_attributes)

    # Filter out built-in attributes and methods
    user_defined_attributes = [attr for attr in dir(student_instance) if
                               not callable(getattr(student_instance, attr)) and not attr.startswith("__")]

    print("\nUser-defined attributes of the instance:")
    print(user_defined_attributes)



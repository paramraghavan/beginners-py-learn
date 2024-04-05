class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def printName(self):
        print(self.name)

if __name__ == '__main__':
    person = Person("Alice", 30)
    attribute_name = "age"
    age = getattr(person, attribute_name, f"Attribute {attribute_name} not found")
    print(age)  # Output: 30
    attribute_name = "address"
    address = getattr(person, attribute_name, f"Attribute {attribute_name} not found")
    attribute_name = "printName"
    getattr(person, attribute_name, f"Attribute {attribute_name} not found")()
    print(address)  # Attribute address not found
```
class Person:
    # constructor
    def __init__(self,age):
        self.new_age = age
    def sleep(self,hours):
        return str(hours * 60) + 'minutes'
    def get_age(self):
        return self.new_age
    def set_age(self,age):
        self.new_age = age

robert = Person(20)
print(robert.get_age())

robert.set_age(25)
print(robert.get_age())


class Teacher:
    def __init__(self,name,age,salary):
        self.name = name
        self.age = age
        self.salary = salary
    def get_salary(self):
        return self.salary
        
class College:
    def __init__(self,name,max_teachers):
        self.name = name
        self.max_teachers = max_teachers
        self.teachers = []
    def add_teacher(self,teacher):
        if len(self.teachers) < self.max_teachers:
            self.teachers.append(teacher)
            return True
        else:
            return False
    def get_average_salary(self):
        total_salary = 0
        for t in self.teachers:
            total_salary = total_salary + t.get_salary()
        avg_salary = total_salary / len(self.teachers)
        return avg_salary



t1 = Teacher('Robert', 25, 10000)
t2 = Teacher('Reid',30, 15000)

c1 = College("Oxford",2)
c1.add_teacher(t1)
c1.add_teacher(t2)

print(len(c1.teachers))
print(c1.teachers[0].name)
print(c1.teachers[1].name)

print("The Average Salary is " + str(c1.get_average_salary()))

class Pet
    # class attribute
    number_of_pets = 0
    def __init__(self,name, age)
        self.name = name
        self.age = age
        Pet.number_of_pets += 1

p1 = Pet('cat',1)
p2 = Pet('dog',2)
p3 = Pet('cow',5)
print(Pet.number_of_pets)

```

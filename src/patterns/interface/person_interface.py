from abc import ABC, abstractmethod
class Person(ABC):
  @abstractmethod
  def whoami(self):
    pass

class Student(Person):
  def whoami(self):
    print ("I am a student")

class Teacher(Person):
  def whoami(self):
    print ("I am a teacher")

class Parent(Person):
    pass

student = Student()
student.whoami()
teacher = Teacher()
teacher.whoami()

print('x'*60)
print('Parent will error out as the abstract method whoami is not implemented')
import traceback
try:
    parent = Parent()
    parent.whoami()
except Exception as e:
    traceback.print_exc()
    #print(e)
print('x'*60)



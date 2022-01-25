# beginners-py-learn
An attempt to teach kids a programming language - beginners python 

# Any one of these IDE's
- pycharm community editon - using pycharm
- visual studio code
- spyder
- notepad

# Start Learning
[Click here and start with 0-learn_variables.py](src/)

# install virtualenv
- Virtual env --> https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
- py -m pip install virtualenv / python -m pip install virtualenv

# create virtual env and activate
- virtualenv venv
- venv\Scripts\activate
- Use [this](src/advance_stuff/inspect_local_python_env.py) to inspect you local venv settings

# [Select and activate a environment/virtual environment in Visual Studio Code](https://code.visualstudio.com/docs/python/environments)
By default, the Python extension looks for and uses the first Python interpreter it finds in the system path. To select a specific environment, 
use the Python: Select Interpreter command from the Command Palette (Ctrl+Shift+P).

![img_1.png](img_1.png)

The Python: Select Interpreter command displays a list of available global environments, conda environments, and virtual environments. 
The following image, for example, shows several Anaconda and CPython installations along with a conda environment and a virtual environment 
(env) that's located within the workspace folder:

![img_2.png](img_2.png)

# install packages
pip install package-name
# how to use requirements.txt to recreate all the required python libraries
pip install -r requirements.txt

# create requirements
pip freeze > requirements

# What's Python Module, Package, Library, Framework
- Module is a file which contains various Python functions and global variables. It is simply just .py extension file which has python executable code.
- Package is a collection of modules. It must contain an init.py file as a flag so that the python interpreter processes it as such. The init.py could be an empty file without causing issues.
- Library is a collection of packages.
- Framework is a collection of libraries.

# try
- help('builtins')


# Inheritance in Python with abstract base class abc
## Abstract Base Classes (ABCs)
Abstract base classes are a form of interface checking. They are classes that contain abstract methods, which are methods declared but without implementation. ABCs are blueprint, cannot be instantiated, and require subclasses to provide implementations for the abstract methods.
In Python, we use the module ABC. ABC works by
defining an abstract base class, and ,
use concrete class implementing an abstract class either by
— register the class with the abc or,
— subclass directly from the abc

### Example

<pre>
from abc import ABC, abstractmethod
class Flour(ABC):
  @abstractmethod
  def make_bread(self):
    pass
    
class Toast(Flour):
  pass
  
x = Toast()
========================
Traceback (most recent call last):
  File "main.py", line 11, in <module>
    x = Toast()
TypeError: Can't instantiate abstract class Toast with abstract methods make_bread
</pre>

- You can see we can’t implement Toast class without implementing the make_bread method.
<pre>
from abc import ABC, abstractmethod
class Flour(ABC):
  @abstractmethod
  def make_bread(self):
    pass
class Toast(Flour):
  def make_bread(self):
  print ("this is a delicious toast")
x = Toast()
x.make_bread()
========================
this is a delicious toast
</pre>

- [click here to learn more on python inheritance](https://elfi-y.medium.com/inheritance-in-python-with-abstract-base-class-abc-5e3b8e910e5e)

# [Python and Patterns - code examples ](src/advance_stuff/patterns)
  - Class for Name  - load module class or via file load.
  - copy, deep copy
  - decorator
  - interface
  - multithreading
  - stringbuilder  

# [Data Structure and Python](https://towardsdatascience.com/which-python-data-structure-should-you-use-fa1edd82946c)
![img.png](img.png)
- Tuples are immutable, you cannot add, delete, or change items after a tuple is created.
- Book on [Data Structure with Python](http://home.ustc.edu.cn/~huang83/ds/Data%20Structures%20and%20Algorithms%20Using%20Python.pdf) 
- [Python and Data Structure - code examples](src/advance_stuff/data_structure)

# Mobile development using python - oh yes
- https://docs.beeware.org/
- https://kivy.org/#home. **Note**  packages for iOS can only be generated with Python 2.7 at the moment.
- https://www.activestate.com/blog/the-best-python-frameworks-for-mobile-development-and-how-to-use-them/#can-i-use-python-for-mobile-app-development-on-both-android-and-ios


References
----------------------
- https://github.com/Akuli/python-tutorial **
- https://github.com/OmkarPathak/Python-Programs
- https://github.com/geekcomputers/Python
- https://greenteapress.com/thinkpython2/html/thinkpython2002.html
- https://dev.to/lucs1590/python-module-vs-package-vs-library-vs-framework-4i0p
- [fun with python](https://python-course.eu/applications-python)
- [bigO](https://medium.com/@zoebai_70369/big-o-notation-time-and-space-complexity-305a1e301e35)
- [big0](https://developerinsider.co/big-o-notation-explained-with-examples/#:~:text=O(2n)&text=An%20example%20of%20an%20O,very%20shallow%2C%20then%20rising%20meteorically)

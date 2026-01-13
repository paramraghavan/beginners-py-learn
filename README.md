# beginners-py-learn
An attempt to teach python to beginners with examples.

## **Basics of how a program works**
[How does a program really works](src/how-does-a-program-run.md)

## Start Learning
- [Click here and start with 0-learn_variables.py](src/)
- [Quick 101](quick101)
- [Advanced](src/advance_stuff/readme.md)

# Setting up Environment and more...
## Any one of these IDE's
- pycharm community edition - using pycharm
- visual studio code
- spyder
- notepad

## GitHub 101
- [Github 101 ](quick101/how-to-git/github-101.md)
- [How To Use Github - simple use case](quick101/how-to-git/how-to-use-github.md)
- [simple_git_setup_common_msitakes.md](simple_git_setup_common_msitakes.md)

## Math for Computer Science
- https://courses.csail.mit.edu/6.042/spring18/mcs.pdf

## Linter and misc
These are comprehensive code analysis, style guide compliance, code formatter pep8 style fixes and more
These tools do:
* pylint: comprehensive code analysis
* flake8: style guide enforcement
* black: code formatter
* mypy: type checking
* autopep8: PEP 8 style fixes
* isort: import sorter
* bandit: security linter
* [code_review](quick101%2Fcode_review)
More details: [linter-misc.md](quick101%2Fcode_review%2Flinter-misc.md)

## Vulnerability
- [vulnerability-check.md](quick101%2Fvulnerability-check.md)

### [Select and activate a environment/virtual environment in Visual Studio Code](https://code.visualstudio.com/docs/python/environments)
By default, the Python extension looks for and uses the first Python interpreter it finds in the system path. To select a specific environment, 
use the Python: Select Interpreter command from the Command Palette (Ctrl+Shift+P).

![img_1.png](img_1.png)

The Python: Select Interpreter command displays a list of available global environments, conda environments, and virtual environments. 
The following image, for example, shows several Anaconda and CPython installations along with a conda environment and a virtual environment 
(env) that's located within the workspace folder:

![img_2.png](img_2.png)


## Install virtualenv
- [Virtual env](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
- py -m pip install virtualenv # use this
- python -m pip install virtualenv # or this

>Note: If pip isn’t installed
>> you need to download the get-pip.py (https://bootstrap.pypa.io/get-pip.py) script 
>> and run as follows
>>> $ python get-pip.py

## Create virtual env and activate
- virtualenv venv
- venv\Scripts\activate
   > on mac-os:
   > source ./venv/bin/activate   
- above will get you into the virtual environmant shell
- Now to install all your packages(from requirements.txt) into the above newly created virtual enviroment, use
  - pip install -r requiremments.txt
- Creating the requirements file, this list all the packages used by your current python environment 
  - pip freeze > requirements.txt 
- See [here](src/advance_stuff/inspect_local_python_env.py) to inspect you local venv settings

# Why is pipfile better than requirements.txt
The `Pipfile` and `Pipfile.lock` system, introduced by the `pipenv` tool, offers some advantages over the traditional `requirements.txt` approach for managing Python package dependencies. Here's why some developers consider `Pipfile` to be better:

1. **Clearer Separation of Production and Development Dependencies**: `Pipfile` allows for a clearer distinction between packages required for production and those required for development. This separation can be seen in the `[packages]` and `[dev-packages]` sections.
2. **Deterministic Builds with `Pipfile.lock`**: `Pipfile.lock` ensures that you're using the same exact versions of libraries every time you install, leading to deterministic builds. This means that if it works on one machine (e.g., your local development machine), it will work on another machine (e.g., production) without any surprises.
3. **Better Dependency Resolution**: `pipenv` resolves dependencies in a more sophisticated manner than `pip` does with `requirements.txt`. It creates a dependency graph and resolves conflicts before generating the `Pipfile.lock`.
4. **Integrated Environment Management**: `pipenv` integrates package management (`pip`) and virtual environment management (`virtualenv`) into one tool. This means you don't need separate tools or commands to manage virtual environments.
5. **Enhanced Security Features**: `pipenv` checks for security vulnerabilities in your dependencies and informs you about them. It integrates with Python's security database to provide these checks.
6. **Simpler Syntax**: Some developers find the `Pipfile` syntax to be simpler and more human-readable than `requirements.txt`.
7. **Support for Multiple Python Versions**: With `pipenv`, you can specify which version of Python you want to use for your project, and it will manage the virtual environment accordingly.

>However, it's essential to note that both systems have their own use cases:
- **Use Case for `requirements.txt`**: If you need a lightweight and straightforward way to pin specific package versions, `requirements.txt` is still a good choice. It is also widely recognized and supported by many CI/CD systems and cloud platforms.
- **Use Case for `Pipfile`**: If you want a more comprehensive solution that manages both package dependencies and virtual environments and offers deterministic builds, `Pipfile` and `pipenv` might be the way to go.
In summary, while `Pipfile` offers some advantages over `requirements.txt`, the best choice depends on the specific needs and preferences of your project.


## requirements.txt
### install packages
pip install package-name
#### how to use requirements.txt to recreate all the required python libraries
pip install -r requirements.txt
#### create requirements
pip freeze > requirements.txt

## creating and using pipfile 
- **pipenv install [package(s)]** , creates a Pipfile - Pipfile and Pipfile.lock, if it does not exist
  - To install a specific version of a package, you can use pipenv install package==version. 
    For example, pipenv install requests==2.25.1
- **pipenv run pip install [package(s)]**
- **pip list**
- **pipenv shell** , activates virtualenv. this will create a virtual enviroment if it does'nt aleady exist
- **pipenv --rm** , removes the virtual environment
- **pipenv shell** , activates virtual memory
- **pipenv install --dev** , installs the dev dependencies like pytest, pytest-mock, etc..
- **pipenv --venv** , gives you the virtual env location
- pipenv run pytest -vv test/
- pipenv run list freeze
- pipenv graph -  to inspect the versions actually installed in the virtualenv.
- pipenv lock -r > requirements.txt
- brew install pipenv
- pipenv run python <your_script.py>, run any Python script within the virtual environment that pipenv set up.


## pipenv lock
- `pipenv lock --clear`
- pipenv lock: This generates a Pipfile.lock, which is used to produce deterministic builds. The Pipfile.lock ensures that every time you (or someone else) installs the dependencies using pipenv, the exact same versions of the dependencies are installed.
- --clear: When this option is added to pipenv lock, it clears the caches. This means that pipenv will ignore any cached package files it has and fetch the packages again from the Python Package Index (PyPI) or other repositories. This can be useful if you believe that the cache might be causing issues or if you want to ensure that you're getting the latest package files from the source.
> In essence, the pipenv lock --clear command will regenerate the Pipfile.lock after clearing the caches, ensuring that the lock file is based on the most recent package files from the repositories.

- **Sample PipFile**
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]
pytest = ">=6.2.4"
moto = "==2.2.0"

[packages]
urllib3 = ">=1.26.5"
wheel = ">=0.36.2"
pyspark = ">=3.3.0"
boto3 = ">=1.17.48"
bumpversion = "==0.6.0"

[requires]
python_version = ">=3.7"
```

## Error with pipenv install, [pipenv.exceptions.ResolutionFailure]: Warning: Your dependencies could not be resolved.
Try the following
 - Check for Direct Conflicts:
      Go through your Pipfile and ensure that there are no direct version conflicts. For instance, if you have specified two packages that depend on different versions of a third package, that could cause a conflict.
   Update Pipenv & Pip:
   Sometimes, issues can be resolved simply by updating pip and pipenv.
   ```sh
      pip install --upgrade pip pipenv
   ```
 - Clear Caches:
   Old cache data can sometimes lead to resolution errors. You can clear pipenv caches with:
   ```sh
   pipenv --clear
   ```
 - Use the --pre Option:
   If one of your dependencies has a pre-release version that you want to use (or need to use), you can tell pipenv to consider pre-releases during dependency resolution:
   ```sh
   pipenv lock --pre
   ```

- Verbose Logging:
Use verbose logging to get more detailed information about where the resolution is failing.
```sh
pipenv lock --verbose
```
- Manually Specify Versions:
If you know a specific package is causing the issue, you can try locking it to a specific version in the Pipfile.    


## How to convert a requirements.txt to a Pipfile 
- Install pipenv: If you haven't installed pipenv yet, you can do so using pip:
```shell
pip install pipenv
```
- Navigate to the Project Directory: Ensure you're in the directory that contains your requirements.txt.
To generate Pipfile from requirements.txt: run the following command:
```shell
pipenv install -r requirements.txt
```
- This will create a Pipfile and Pipfile.lock in your project directory based on the dependencies listed 
in requirements.txt. If a Pipfile already exists in the directory, pipenv will add the dependencies from requirements.txt
to it. Separating Dev and Main Dependencies (Optional): If you have development-specific dependencies 
(like testing libraries) that you don't want to be installed in a production environment, you can separate them. 
First, move these dev dependencies to a separate file, say dev-requirements.txt. Then, run:
```shell
pipenv install --dev -r dev-requirements.txt
```
- Above will add the development dependencies to the [dev-packages] section of the Pipfile.
- Final Steps: After the conversion, review the generated Pipfile to ensure all dependencies are
correctly specified. You might want to manually specify versions or ranges if needed. 

### Specify a Python Version for a New Project:
If you're starting a new project and know the version of Python you want to use, you can specify it 
when creating a new virtual environment. For instance, to use Python 3.8:
```shell
pipenv --python 3.8
```
### pipenv specify python version
- Setting Python Version in Pipfile. Inside the Pipfile, you can specify the version of 
Python for your project under the [requires] section:
```
[requires]
python_version = "3.8"
```
### Switching Between Projects:
When you change to a different project directory and run **pipenv shell** or
**pipenv run**, pipenv will automatically activate the virtual environment 
associated with that project, which includes using the correct Python 
version specified for that project.

### Changing Python Version for an Existing Project:
- If you need to change the Python version for an existing project:
- Update the Pipfile with the desired version under the **[requires]** section.
- Remove the existing virtual environment using **pipenv --rm**.
- Recreate the virtual environment with the new Python version using **pipenv install**.

# Python nuances
## What's Python Module, Package, Library, Framework
- Module is a file which contains various Python functions and global variables. It is simply just a **'.py'** extension file which has python executable code.
- Package is a collection of modules inside a directory/folder. This directory/folder must contain an init.py file as a flag so that the python interpreter 
processes it as such. The init.py could be an empty file without causing issues.
- Library is a collection of packages.
- Framework is a collection of libraries.

## Variable access control: public, protected, and private variables
These are conventions rather than strict enforcement like in languages such as Java or C++. 
Here's how they work in python

---

### **1. Public Variables**

- Can be accessed from anywhere (inside and outside the class).
- No special prefix needed.

```python
class Example:
    def __init__(self):
        self.public_var = "I am public"


obj = Example()
print(obj.public_var)  # 🟢 Accessible
obj.public_var = "Modified"  # 🟢 Can be modified
print(obj.public_var)
```

---

### **2. Protected Variables**

- Indicated by a **single underscore (`_`)**.
- Meant to be used only within the class and its subclasses.
- Still accessible from outside, but it's a convention not to access it directly.

```python
class Example:
    def __init__(self):
        self._protected_var = "I am protected"


obj = Example()
print(obj._protected_var)  # 🟢 Accessible (but should be treated as private)
obj._protected_var = "Modified"  # 🟢 Can be modified (not recommended)
print(obj._protected_var)
```

---

### **3. Private Variables**

- Indicated by a **double underscore (`__`)**.
- Python uses **name mangling** to make it harder to access directly.
- The variable name is changed internally (e.g., `__private_var` becomes `_Example__private_var`).

```python
class Example:
    def __init__(self):
        self.__private_var = "I am private"


obj = Example()
# print(obj.__private_var)  # 🔴 AttributeError: Cannot access directly

# Accessing private variable using name mangling
print(obj._Example__private_var)  # 🟢 Accessible but not recommended
```

---

### **Key Differences**

| Type          | Prefix | Access from Outside Class?        | Best Practice                        |
|---------------|--------|-----------------------------------|--------------------------------------|
| **Public**    | None   | 🟢 Yes                             | Free to use                          |
| **Protected** | `_`    | 🟢 Yes (but avoid)                 | Use inside class and subclasses only |
| **Private**   | `__`   | 🔴 No (can access via name mangling) | Keep within class                    |


## What does the init method do in a Class defination? Why is it necessary? (etc.)

- The first argument of every class method, including init, is always a reference to the current instance of the class. By convention, this argument is always
 named self. In the init method, self refers to the newly created object; in other class methods, it refers to the instance whose method was called.

- **Python doesn't force you on using "self". You can give it any name you want. But remember the first argument in a method definition is a reference
to the object** Python adds the self argument to the list for you; you do not need to include it when you call the methods. if you didn't provide
self in init method then you will get an error:
>TypeError: __init___() takes no arguments (1 given)

- init is short for initialization. It is a constructor which gets called when you make an instance of the class
  and it is not necessary. But usually it our practice to write init method for setting default state of the object.
  If you are not willing to set any state of the object initially then you don't need to write this method.
- [init and new](quick101/init-and-new.md)
- [see](src/advance_stuff/class_defination.py)
- [python class initialization sequence](src/advance_stuff/class_init_sequence/readme.md)
## try
- help('builtins')

## __name__(A Special variable) in Python
 <pre>
 1. __name__(A Special variable) in Python
 
 2. Since there is no main() function in Python, when the command to run a python program is given to the 
   interpreter, the code that is at level 0 indentation is to be executed. However, before doing that, it
   will define a few special variables. __name__ is one such special variable. If the source file is executed
   as the main program, the interpreter sets the __name__ variable to have a value “__main__”. If this file
   is being imported in another module, __name__ will be set to the module’s name.
 
 3.  __name__ is a built-in variable which evaluates to the name of the current module. Thus it can be 
 used to check whether the current script is being run on its own or being imported somewhere else by 
 combining it with if statement.
</pre>
- [see](src/advance_stuff/main/main.py)
## [Sequence in python](src/advance_stuff/pycollections/sequence.md)


## Inheritance in Python with abstract base class abc
### Abstract Base Classes (ABCs)
Abstract base classes are a form of interface checking. They are classes that contain abstract methods, which are methods declared but without implementation. ABCs are blueprint, cannot be instantiated, and require subclasses to provide implementations for the abstract methods.
In Python, we use the module ABC. ABC works by
defining an abstract base class, and ,
use concrete class implementing an abstract class either by
— register the class with the abc or,
— subclass directly from the abc

#### Example

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

- You can see we can’t instantiate Toast class without implementing the make_bread method.
<pre>
from abc import ABC, abstractmethod
class Flour(ABC):
  @abstractmethod
  def make_bread(self):
    pass
class BreadMaker(Flour):
  def make_bread(self):
    print ("this is a delicious bread.")
x = BreadMaker()
x.make_bread()
========================
this is a delicious toast
</pre>

- [click here to learn more on python inheritance](https://elfi-y.medium.com/inheritance-in-python-with-abstract-base-class-abc-5e3b8e910e5e)

## [Python and Patterns - code examples ](src/advance_stuff/patterns)
  - Class for Name  - load module class or via file load.
  - copy, deep copy
  - decorator
  - interface
  - multithreading
  - stringbuilder  

## __dunder__ methods and designing apis
  - [dunder_methods](quick101%2Fdunder-methods%2Freadme.md)
  - [designing-apis](src%2Fadvance_stuff%2Fapis-how-to%2Freadme.md)

## [Data Structure and Python](https://towardsdatascience.com/which-python-data-structure-should-you-use-fa1edd82946c)
![img.png](img.png)
- Tuples are immutable, you cannot add, delete, or change items after a tuple is created.
- Book on [Data Structure with Python](https://doc.lagout.org/science/0_Computer%20Science/2_Algorithms/Data%20Structures%20and%20Algorithms%20using%20Python%20%5BNecaise%202010-12-21%5D.pdf) 
- [Python and Data Structure - code examples](src/advance_stuff/data_structure)

## Python and Databases
- [Setup a local containerized rdbs instances](src/database/README.md), rdbms - Postgresql and nosql- MongoDB. Shows you how to do read operation
  using python database driver psycopg2, write to database is left as an exercise.

## python packages
- https://pypi.org/

## How to build package and manage version numbers
- https://github.com/paramraghavan/pkg_example_project#readme

## profile python code
<pre>
test.py

def big_loop():
    return loop(100000)

def loop(loop_count):
    return "-".join(str(i) for i in range(loop_count))

def call():
    small_loop()
    big_loop()

import cProfile
if __name__ == '__main__':
    cProfile.run('call()')
</pre>

Profile Result
<pre>
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.056    0.056 <string>:1(<module>)
        2    0.000    0.000    0.056    0.028 exercise7_solution_decorator.py:15(wrapper_function)
        1    0.000    0.000    0.008    0.008 exercise7_solution_decorator.py:24(small_loop)
        1    0.000    0.000    0.047    0.047 exercise7_solution_decorator.py:28(big_loop)
        2    0.000    0.000    0.055    0.028 exercise7_solution_decorator.py:32(loop)
   120002    0.039    0.000    0.039    0.000 exercise7_solution_decorator.py:33(<genexpr>)
        1    0.000    0.000    0.056    0.056 exercise7_solution_decorator.py:35(call)
        1    0.000    0.000    0.056    0.056 {built-in method builtins.exec}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        4    0.000    0.000    0.000    0.000 {built-in method time.time}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        2    0.000    0.000    0.000    0.000 {method 'format' of 'str' objects}
        2    0.016    0.008    0.055    0.028 {method 'join' of 'str' objects}

</pre>
[ref](https://stackoverflow.com/questions/582336/how-do-i-profile-a-python-script)


## inline profile
Profiling spark job submitted to EMR cluster, the results written to the cluster can be copied over to S3 location - have not tried, not sure how it will pan out. Better option may be to capture the time to execute each function - old style. As with spark jobs -jobs are broken to stages and task, tasks run on individual nodes. 
<pre>
test.py

def big_loop():
    return loop(100000)

def loop(loop_count):
    return "-".join(str(i) for i in range(loop_count))

def call():
    small_loop()
    big_loop()

if __name__ == '__main__':
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    call()
    profiler.disable()
    # Export profiler output to file
    stats = pstats.Stats(profiler)
    stats.dump_stats('test.pstat')
</pre>

## pip install vs python -m pip install

### pip install

This command directly invokes the pip executable. Depending on how Python is configured on your system or installed,
this typically points to a pip that is associated with one of the Python interpreters installed on your system. When you
use pip install, you're trusting the system's environment to use the correct pip associated with the correct Python
version you intend to use.

### python -m pip install

This command explicitly tells Python to run the pip module as a script. The key advantage here is that you are
specifying which Python interpreter you want to use to install packages. This is particularly useful in environments
where multiple Python versions are installed or in virtual environments. Using python -m pip install ensures that you
are executing pip for the Python interpreter you are currently using or have specified, and it avoids confusion about
which Python version pip will operate on.

When working within virtual environments created by venv or virtualenv. It ensures that the packages are installed in
the virtual environment's site-packages directory, rather than the global Python environment.

python -m pip install makes it explicit which Python interpreter's pip is being used, reducing the risk of installing
packages into the wrong Python's site-packages directory.

## How to convert python script to binary
- [building_binary_files_for_python_scripts.md](building_binary_files_for_python_scripts.md)

## profiling with ui
- sankeviz profiler
  - saves the profile to test.profile, - saves the profile  to test.profile, python -m cProfile -o test.pstats test.py
  - Install snakeviz, pip install snakeviz
  - snakeviz test.profile
- gprof2dot profiler
  - saves the profile to test.stats, - saves the profile  to test.pstats, python -m cProfile -o test.pstats test.py
  - Install gprof2dot, pip install gprof2dot
  - brew install graphviz
  - ~~gprof2dot -f pstats test.pstats | dot -Tpng -o output.png && eog output.png~~ could get eog(eye of Gnome) installed)
  - gprof2dot -f pstats test.pstats | dot -Tpng -o output.png

- pip install viztracer
  - viztracer -o result.json -- test.py arg1 arg2 arg3
  - vizviewer result.json
[ref](https://medium.com/@narenandu/profiling-and-visualization-tools-in-python-89a46f578989)

## References
----------------------
- https://github.com/Akuli/python-tutorial **
- https://developers.google.com/edu/python **
- https://github.com/OmkarPathak/Python-Programs
- https://github.com/geekcomputers/Python
- https://greenteapress.com/thinkpython2/html/thinkpython2002.html
- https://dev.to/lucs1590/python-module-vs-package-vs-library-vs-framework-4i0p
- [fun with python](https://python-course.eu/applications-python)
- [bigO](https://medium.com/@zoebai_70369/big-o-notation-time-and-space-complexity-305a1e301e35)
- [big0](https://developerinsider.co/big-o-notation-explained-with-examples/#:~:text=O(2n)&text=An%20example%20of%20an%20O,very%20shallow%2C%20then%20rising%20meteorically)
- [bigO](https://jarednielsen.com/big-o-factorial-time-complexity/)
- https://builtin.com/data-science/dunder-methods-python - __add__, __sub__ examples

## Interesting ToDo
-------------------------------------

- [Computer system status using python](https://github.com/msimms/ComputerStatus) - have not checked it out yet, seems promising

### Image Processing
- https://towardsdatascience.com/image-enhancement-techniques-using-opencv-and-python-9191d5c30d45
- https://www.adobe.com/express/feature/image/resize/png
- [Pencil Sketch image](https://github.com/pythonlessons/background_removal)
- [Artwork Using Python and TensorFlow github](https://github.com/omerbsezer/NeuralStyleTransfer#readme)
- https://towardsdatascience.com/painting-and-sketching-with-opencv-in-python-4293026d78b
- https://github.com/atriwal/Points_Art

### Image Restoration
- https://github.com/shyama95/image-restoration
- https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life
- https://github.com/TencentARC/GFPGAN *


###  D-Tale for interactive data exploration
#### What is  D-Tale?
 D-Tale is the combination of a Flask back-end and a React front-end to bring you an easy way to view & analyze Pandas
 data structures. It integrates seamlessly with ipython notebooks & python/ipython terminals. Currently this tool supports
 such Pandas objects as DataFrame, Series, MultiIndex, DatetimeIndex & RangeIndex.
**Notes**
- pip install dtale
- https://towardsdatascience.com/introduction-to-d-tale-5eddd81abe3f
- https://www.analyticsvidhya.com/blog/2021/06/exploring-pandas-dataframe-with-d-tale/11
- https://pypi.org/project/dtale/

### Mobile development using python - oh yes
- https://docs.beeware.org/
- https://kivy.org/#home. **Note**  packages for iOS can only be generated with Python 2.7 at the moment.
- https://www.activestate.com/blog/the-best-python-frameworks-for-mobile-development-and-how-to-use-them/#can-i-use-python-for-mobile-app-development-on-both-android-and-ios


## Interview Questions
-------------------
- https://www.mygreatlearning.com/blog/python-interview-questions/?amp

 

## To best prepare for Amazon’s Technical Problem Solving Challenge, here are some resources:
-----------------------------------------------------------------------------------------------------
- Cracking the Coding Interview - http://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/098478280X
- Algorithm Fundamentals: - http://algs4.cs.princeton.edu/10fundamentals/
Fundamentals: Go back and re-educate yourself on all data structures & algorithms. You will be challenged on several of the methods in the On-Site interview so you might as well start practicing now! Make sure you even get into more exotic things like hashmaps, b+trees (and variants), caches (and associated algorithms). You may want to visit www.codechef.com
- Project Euler - http://projecteuler.net/ If you’ve been out of practice, complete up to problem 60 or so. You should be prompted to build useful libraries, which will help give practical experience for interview like problems. Don’t cheat or take shortcuts.
- Leetcode has additional practice questions: https://leetcode.com/
- Understand high scale architecture. Go look at how other big sites are structured: http://highscalability.com/blog/category/example
- Get a feel for the interface and functionality with our demo version: https://www.myamcat.com/amazon-lateral-demo

## Licenses in Software Development
--------------------------------
Short summaries of the licenses:
- The MIT, BSD, and ISC licenses are “permissive licenses”. They are extremely short and essentially say “do whatever you want with this, just don’t sue me.”
- The Apache license says “do whatever you want with this, just don’t sue me” but does so with many more words, which lawyers like because it adds specificity. It also contains a patent license and retaliation clause which is designed to prevent patents (including patent trolls) from encumbering the software project.
- The GPL licenses (GPLv3, GPLv2, LGPL, Affero GPL) all contain some kind of share-alike license. They essentially say “if you make a derivative work of this, and distribute it to others under certain circumstances, then you have to provide the source code under this license.” The important thing to know here is that “derivative work” and “certain circumstances” both require some legal analysis to understand the meaning and impact for your project.
- [ref](https://www.exygy.com/blog/which-license-should-i-use-mit-vs-apache-vs-gpl)


## Python and backward compatibility
----------------------------------
99% of the time, if it works on Python 3.x, it'll work on 3.y where y >= x. Enabling warnings when running your code on the older version should pop DeprecationWarnings when you use a feature that's deprecated (and therefore likely to change/be removed in later Python versions). Aside from that, you can read the [What's New docs](https://docs.python.org/3/whatsnew/) for each version between the known good version and the later versions, in particular the Deprecated and Removed sections of each.

Python only ever broke compatibility between Python 2 and 3. If you have something that runs on Python 3.8, it will also work on every following version.

They do break compatibility in small ways between minor versions (and once in a while, even between micro versions, where not changing something leaves a worse bug in place, e.g. the change from 3.5.0 to 3.5.1 that broke code that called vars on namedtuples). Another example was async and await becoming keywords in 3.7 IIRC (which broke the pika package, where 0.11 used async as a variable name, and required the 0.12 release of pika). 
- [Python 3.9 vs 3.10](https://www.analyticsvidhya.com/blog/2021/08/differences-between-python-3-10-and-python-3-9-which-you-need-to-know)

ref: https://stackoverflow.com/questions/70467517/how-can-i-know-what-python-versions-can-run-my-code


## Python Generative AI AWS
- https://www.youtube.com/watch?v=ab1mbj0acDo

## pep8
PEP 8 is the Python Enhancement Proposal which provides guidelines and best practices on how to write Python code. It is not mandatory but considered good practice.

**Key aspects of PEP 8 include:**
* Indentation: Use 4 spaces per indentation level.
* Maximum Line Length: Limit all lines to a maximum of 79 characters for code and 72 characters for comments and docstrings.
* Blank Lines: Use blank lines to separate functions and classes, and larger blocks of code inside functions.
* Imports: Imports should usually be on separate lines and are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
* Whitespace in Expressions and Statements: Avoid extraneous whitespace in various situations, such as immediately inside parentheses, brackets or braces, between a trailing comma and a following close parenthesis, etc.
* Comments: Comments should be complete sentences. If a comment is short, the period at the end can be omitted.
* Naming Conventions: There are various naming conventions for different types of identifiers (e.g., module names, function names, variable names, class names). These conventions include using lowercase with words separated by underscores for function and variable names (function_name), and using CapWords for class names (ClassName).
* Programming Recommendations: Code is read more often than it is written, so make your code as readable as possible. Avoid complex and obscure expressions; straightforward is better than complicated
- [pep8](https://peps.python.org/pep-0008/)

## Get tree structure of you project
- `brew install tree`
- `tree -I 'dir_to_exclude'` - `dir_to_exclude` is the name of the directory that will be skipped.
- `tree -I 'dir1|dir2|*pattern*'` - This command will exclude dir1, dir2, and any directories that match the pattern *pattern*. Remember that the pattern matching is case-sensitive by default.


## Easy documentation/diagramming
- Markdown
- Mermaid and markdown
- drawio.com , https://get.diagrams.net/
- Excalidraw (excalidraw.com) - Free, browser-based, feels like drawing with a pen. Super intuitive and fast.
- tldraw - Similar hand-drawn style, very responsive

## what is devops
- https://www.geeksforgeeks.org/devops/devops-lifecycle/

## Errors

### openssl error on git clone
Following resolves it:
```shell
git config --global http.sslBackend schannel
```
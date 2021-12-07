# kids-py-learn
An attempt to teach kids a programming language - python 

#IDE
- pycharm community editon - using pycharm
- visual studio code
- spyder
- notepad

# install virtualenv
- Virtual env --> https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
- py -m pip install virtualenv / python -m pip install virtualenv

# create virtual env and activate
virtualenv venv
venv\Scripts\activate

# install packages
pip install package-name
# how to use requirements.txt to recreate all the required python libraries
pip install -r requirements.txt.txt

# create requirements
pip freeze > requirements

References
----------------------
- https://github.com/Akuli/python-tutorial **
- https://github.com/OmkarPathak/Python-Programs
- https://github.com/geekcomputers/Python
- https://greenteapress.com/thinkpython2/html/thinkpython2002.html
- https://dev.to/lucs1590/python-module-vs-package-vs-library-vs-framework-4i0p

# What's Python Module, Package, Library, Framework
- Module is a file which contains various Python functions and global variables. It is simply just .py extension file which has python executable code.
- Package is a collection of modules. It must contain an init.py file as a flag so that the python interpreter processes it as such. The init.py could be an empty file without causing issues.
- Library is a collection of packages.
- Framework is a collection of libraries.

# try
- help('builtins')

# [Data Structure and Python](https://towardsdatascience.com/which-python-data-structure-should-you-use-fa1edd82946c)
![img.png](img.png)

Tuples are immutable, you cannot add, delete, or change items after a tuple is created.

ref: http://home.ustc.edu.cn/~huang83/ds/Data%20Structures%20and%20Algorithms%20Using%20Python.pdf

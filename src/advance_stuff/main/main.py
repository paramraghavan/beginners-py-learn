'''
ref: https://www.geeksforgeeks.org/__name__-special-variable-python/
__name__ (A Special variable) in Python

Since there is no main() function in Python, when the command to run a python program is given to the interpreter, the code that
is at level 0 indentation is to be executed. However, before doing that, it will define a few special variables. __name__ is one such special variable.
If the source file is executed as the main program, the interpreter sets the __name__ variable to have a value “__main__”. If this
file is being imported from another module, __name__ will be set to the module’s name.

__name__ is a built-in variable which evaluates to the name of the current module. Thus it can be used to check whether the
current script is being run on its own or being imported somewhere else by combining it with if statement, as shown below.

Consider two separate files File1.

We import file1
'''

import file1

print("file1 is imported and used in main.py,  __name__ = %s" % __name__)

if __name__ == "__main__":
    print("main.py is being run directly")
else:
    print("File2 is being imported")


# Output:
# File1 __name__ = file1
# File1 is being imported
# file1 is imported and used in main.py,  __name__ = __main__
# main.py is being run directly
'''
Module is a file which contains various Python functions and global variables.
It is simply just .py extension file which has python executable code.

Package is a collection of modules. It must contain an init.py file as a
flag so that the python interpreter processes it as such. The init.py
could be an empty file without causing issues.

Library is a collection of packages.

Framework is a collection of libraries.

'''


import json # you need to import this package

# following is a JSON string:
# json is used to share information b/w systems
# which may be programmed in  separate programmimg langaue
# but communicate over web/network - http,  etc
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

print(type(y))
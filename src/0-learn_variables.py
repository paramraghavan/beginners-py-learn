'''
int is short for integer. 1 and 2 are integers.
float is short for floating point number. 1.0 and 3.14 are floats.
str is short for string. "hello" and 'hello' are strings. It doesn't matter if you use 'single quotes' or "double quotes", they do the same thing in Python.
More exercises
What happens if you use + between two strings, like "hello" + "world"? How about "hello" * "world"?
What happens if you use + between a string and an integer, like "hello" + 3? How about "hello" * 3?
What happens if you use + between a float and an integer, like 0.5 + 3? How about 0.5 * 3?
'''

# various data types integer, decimal/float, string
# Stack, heap and virtual heap/memory
# language - compiled - c/c++, bytecode compiled - java and interpreted - python

'''
Natural languages are the languages people speak, such as English, Spanish, and French. 
They were not designed by people (although people try to impose some order on them); 
they evolved naturally.

Formal languages are languages that are designed by people for specific applications. 
For example, the notation that mathematicians use is a formal language that is particularly
good at denoting relationships among numbers and symbols. Chemists use a formal 
language to represent the chemical structure of molecules. And most importantly:

Programming languages are formal languages that have been designed to express computations. 
'''

'''
Languages can be - interpreted, compiled or run-time compiled. 
Interpreted: Python is an example of this. It processes a program line by line. As an example, 
if in a 10 line program, line 3 has a problem, then the program will run line one and line two,
then fail at line 3.

Compiled: c/c++ is an example of this. It will compile the entire program and if there is a single 
failure anywhere it will not run the entire code.

Bytecode compiled:  Java compiles it's program into byte code, when the program runs the java's 
JIT (just in time byte code compiler) compiler will compile  code and optimize 
the code as the porgeam is running/executing.
'''

'''
How to declare a variable in Python
Python is a dynamic-typed language, which means we don't need to mention the variable type 
or declare before using it - unlike Java or C . It makes to Python the most efficient and easy to use language. 
Every variable is treated as an object in Python.

Before declaring a variable, we must follow the given rules.

The first character of the variable can be an alphabet or (_) underscore.
Special characters (@, #, %, ^, &, *) should not be used in variable name.
Variable names are case sensitive. For example - age and AGE are two different variables.
Reserve words cannot be declared as variables.
ref: https://www.javatpoint.com/how-to-declare-a-variable-in-python
'''

# variable declaration example in java
# int value_int = 200

value_int = 200
#value_int = int(200)
value_float = 3.14
value_string = 'hello'
# Built-in classes use lowercase names (like str instead of Str)
# because they are faster to type, but use CapsWord names for your classes.
#value_string = str('hello')

print(value_int)

print(type(value_int))


value_string_concatenation = "hello" + "world?"

var_apple = 'Apple pie'
print(len(var_apple))                           # 9

value_string_float_concatenation = "hello" + 3.14
# How about "hello" * 3 ??

# Arithmetic operators +, *, / and more
value_int_float = value_int + value_float

print(value_int_float)

print("hello " + "World " + 2021)

# string formatting not used
# this works but not preferred
print('value_int : ' + value_int)

# string formatting, f-string
# this is preferred
print(f'value_int : {value_int}')

value_multiplication_operator = value_int * value_float
print(f'result of value_multiplication_operator: {value_multiplication_operator}')

# read --> https://greenteapress.com/thinkpython2/html/thinkpython2002.html
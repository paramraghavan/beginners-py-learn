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
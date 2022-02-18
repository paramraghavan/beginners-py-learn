'''
A lambda function is an anonymous function.
A lambda function can take any number of arguments, but can only have one expression.

lambda arguments : expression

ref: https://www.w3schools.com/python/python_lambda.asp
'''


myfunc = lambda a : a + 10
# prints 15
print(myfunc(5))

myfunc = lambda a, b : a * b
# prints 30
print(myfunc(5, 6))

myfunc = lambda a, b, c : a + b + c
# prints 11
print(myfunc(5, 6, 2))


'''

The power of lambda is when you use them as an anonymous function inside another function.
Say you have a function definition that takes one argument, and that argument will be multiplied with 
an unknown number:
'''

def myfunc(n):
  return lambda a : a * n

mydoublerfunc = myfunc(2)
# prints 22
print(mydoublerfunc(11))
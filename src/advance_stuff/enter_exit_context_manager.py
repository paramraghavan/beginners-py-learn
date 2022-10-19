# ref: https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
'''
In this example I am opening the myfile.txt file with help of open function. The try/finally block ensures that even if
an unexpected exception occurs myfile.txt will be closed.

fp=open(r"C:\Users\SharpEl\Desktop\myfile.txt")
try:
    for line in fp:
        print(line)
finally:
    fp.close()

Now I am opening same file with with statement:

with open(r"C:\Users\SharpEl\Desktop\myfile.txt") as fp:
    for line in fp:
        print(line) 

If you look at the code, I didn't close the file & there is no try/finally block. Because with statement automatically closes myfile.txt .
You can even check it by calling print(fp.closed) attribute -- which returns True.

This is because the file objects (fp in my example) returned by open function has two built-in methods __enter__ and __exit__. 
It is also known as context manager. __enter__ method is called at the start of with block and __exit__ method is called at the end.

Note: with statement only works with objects that support the context management protocol (i.e. they have __enter__ and __exit__ methods).
A class which implement both methods is known as context manager class.
'''

# Define our own context manager class
class Log:
    def __init__(self,filename):
        self.filename=filename
        self.fp=None    
    def logging(self,text):
        self.fp.write(text+'\n')
    def __enter__(self):
        print("__enter__")
        self.fp=open(self.filename,"a+")
        return self    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        self.fp.close()

with Log(r"C:\Users\SharpEl\Desktop\myfile.txt") as logfile:
    print("Main")
    logfile.logging("Test1")
    logfile.logging("Test2")

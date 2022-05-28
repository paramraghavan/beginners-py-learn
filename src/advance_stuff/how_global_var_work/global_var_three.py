'''
 When you assign 42 to the name myGlobal, therefore, Python creates a local variable that shadows the global variable of the same name.
 That local goes out of scope and is garbage-collected when func1() returns; meanwhile, func2() can never see anything other than the
 (unmodified) global name. Note that this namespace decision happens at compile time, not at runtime -- if you were to read the value of
 myGlobal inside func1() before you assign to it, you'd get an UnboundLocalError, because Python has already decided that it must be
 a local variable but it has not had any value associated with it yet.

  But by using the 'global' statement, you tell Python that it should look elsewhere for
  the name instead of assigning to it locally.

  This time 42 is printed
'''
myGlobal = 5
#prints 5
def func0():
    print(f'func0 myGlobal : {myGlobal}')

# modifies global value, myGlobal
def func1():
    global myGlobal
    myGlobal = 42
    print(f'func2 updates global scope myGlobal : {myGlobal}')

# prints 42
def func2():
    print(f'func2 myGlobal : {myGlobal}')

# prints 11
# all the changes are local to func3(), does not modify global value, myGlobal
def func3():
    myGlobal = 11
    print(f'func3 updates local scope myGlobal : {myGlobal}')

# prints 42, Global value, as changes func3() are local to func3()
def func4():
    print(f'func4 myGlobal : {myGlobal}')

func0()
func1()
func2()
func3()
func4()
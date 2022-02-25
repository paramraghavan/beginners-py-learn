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

def func1():
    global myGlobal
    myGlobal = 42


def func2():
    print(f'myGlobal : {myGlobal}')


func1()
func2()
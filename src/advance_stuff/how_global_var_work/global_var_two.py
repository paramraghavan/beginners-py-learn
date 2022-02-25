''''
You might expecting this to print 42, but instead it prints 5. 
'''


myGlobal = 5

def func1():
    myGlobal = 42

def func2():
    print(f'myGlobal : {myGlobal}')

func1()
func2()
```
##### Understanding Tracebook Module and its function print_exc()
###exception_handling.py
import traceback as tb
def test():
    sal = -1
    try:
        if sal < 0 :
            raise Exception('Salary Can not be Less Than 0.')
    except Exception as Argument:
        print("An Exception Occured. ", Argument)
        raise
		
###outer.py		
import exception_handling as eh
import sys
import traceback as tb

def main():
    try:
        eh.test()
    except:
        print(tb.print_exc())
		sys.exit(1)

if __name__ == '__main__':
    main()

##### Perform Backtrace operations using exc_info() function of sys module.
###exception_handling.py
def test():

    try:
        if sal < 0 :
            raise Exception('Salary Can not be Less Than 0.')
    except NameError as Argument:
        print("An Exception Occured. ", Argument)
        raise

		
###outer.py		
import exception_handling as eh
import sys
import traceback as tb

def main():
    try:
        eh.test()
    except:
        ob = sys.exc_info()[2]
        print(ob.tb_lineno)
        print(ob.tb_frame)
        print(ob.tb_next.tb_lineno)
        print(ob.tb_next.tb_frame)

if __name__ == '__main__':
    main()
```

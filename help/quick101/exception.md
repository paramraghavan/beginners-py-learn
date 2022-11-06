```
###
print(sal)
#Exit Code as 1

### Now Handle the error:
try:
    print(sal)
except NameError:
    print("An Exception Occured")
except Exception: #or use just except :
    print("An Exception Occured here ...")
else:
    # all is well and no exception happened,then here
    print("No Error. The Code Executed Successfully !")
finally:
    # always here
    print("This would always be executed.")
#Exit Code 0

### Exception Argument:
try:
    print(sal)
except NameError as Argument:
    print("An Exception Occured", Argument)
else:
    print("No Error. The Code Executed Successfully !", Argument)

	
### User Defined Exception:
sal = -1
try:
    if sal < 0 :
        raise Exception('Salary Can not be Less Than 0.')
except Exception as Argument:
    print("An Exception Occured. ", Argument)

### What a Production Set up looks like
import sys
sal = -1
try:
    if sal < 0 :
        raise Exception('Salary Can not be Less Than 0.')
except Exception as Argument:
    print("An Exception Occured. ", Argument)
    #logger.error("Error Occured" + Arguemnt)
    #Log the Error in the database
    #Send an Email Notification
    #raise
    #sys.exit(0)
```

def test():
    sal = -1
    try:
        if sal < 0 :
            raise Exception('Salary Can not be Less Than 0.')
    except NameError as Argument:
        print("An Exception Occured. ", Argument)
        raise

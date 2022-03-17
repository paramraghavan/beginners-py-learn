'''
Reference:  https://medium.com/swlh/handling-exceptions-in-python-a-cleaner-way-using-decorators-fae22aa0abec

Error Handling Using Decorators
-----------------------------------
'''

'''
Exception handler decorator.
'''
def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            print(f"{func.__name__} only takes numbers as the argument")
    return inner_function


@exception_handler
def area_square(length):
    area_square_val = length * length
    print(area_square_val)
    return area_square_val


@exception_handler
def area_circle(radius):
    print(3.14 * radius ** 2)


@exception_handler
def area_rectangle(length, breadth):
    print(length * breadth)

if __name__ == '__main__':
    print(f'area_square: {area_square(2)}')
    area_circle(2)
    area_rectangle(2, 4)
    area_square("some_str")
    area_circle("some_other_str")
    area_rectangle("some_other_rectangle")
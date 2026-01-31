import inspect


def my_function():
    # stack()[1] contains information about the caller
    caller_frame = inspect.stack()[1]

    caller_name = caller_frame.function
    caller_filename = caller_frame.filename
    caller_lineno = caller_frame.lineno

    print(f"I was called by '{caller_name}' in {caller_filename} at line {caller_lineno}")


def main_process():
    my_function()


main_process()
def my_function():
    x = 10
    y = 20
    arg = [1, 2, 3]
    local_vars = locals()
    print(f'local variables {local_vars}')
    print("Value of x:", local_vars['x'])


    print(f"Value of the first argument {locals()['arg'][0]}")

if __name__ == "__main__":
    my_function()
    # Output:
    # local variables {'x': 10, 'y': 20, 'arg': [1, 2, 3]}
    # Value of x: 10
    # Value of the first argument 1

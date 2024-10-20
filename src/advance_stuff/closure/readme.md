# Closure aka Local Functions

Local functions are functions defined inside other functions, which can access variables from their enclosing scope.
This creates a closure, allowing the inner function to "remember" and use variables from its outer function even 
after the outer function has finished executing.

## Here's a simple example in Python to illustrate this concept:

```python
def simple_outer_function(x):
    """
    return 7
    """    
    x=5
    def inner_function(y):
        return x + y
    val = inner_function(2) # 5 + 2
    return val

print(f'{simple_outer_function(5)}') # prints 7
```
- _inner_function inside simple_outer_function makes it a local function_, also known as a closure. This means inner_function has 
access to the variables in the outer function's scope, in this case `x` variable 
- Inside `simple_outer_function`, we define an `inner_function` that takes a parameter `y`.
- `inner_function` uses both `x` (from the outer function) and `y` (its own parameter) to return their sum.
- `inner_function` uses both `x` (from the outer function) and `y` (its own parameter) to return their sum.

Closures are useful for creating function factories, implementing decorators, and in functional programming patterns.
They allow for more flexible and powerful code organization by encapsulating data within functions.

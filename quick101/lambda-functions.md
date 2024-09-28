# Lambda Functions:
lambda Bound-Variable: Body
``` 
 Example:
  add10 = lambda x : x + 10
  print(add10(5))
  
  add = lambda x,y : x + y
  print(add(1,2))
```

## Where can we use Lambda Function:
It can be used anywhere, but very handy when we use it inside another function.
```
def generic(num):
   return lambda a : a * num

generic(10) # returns a  function reference, <function generic.<locals>.<lambda> at 0x7fc64816a5e0>

double = generic(2) # double is the function reference
double(3)

triple = generic(3)
triple(3)
```

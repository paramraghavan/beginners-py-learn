# Sorting
sorted is a build-in function , help(sorted) or dir(__buildins__)

```python
  a = [5, 1, 4, 3]
  print(sorted(a))  ## [1, 3, 4, 5]
  print(a)  ## [5, 1, 4, 3]
```

## reverse
```python
  strs = ['aa', 'BB', 'zz', 'CC']
  print(sorted(strs))  ## ['BB', 'CC', 'aa', 'zz'] (case sensitive)
  print(sorted(strs, reverse=True))   ## ['zz', 'aa', 'CC', 'BB']
```

## custom sort
```python
  strs = ['ccc', 'aaaa', 'd', 'bb']
  print(sorted(strs, key=len))  ## ['d', 'bb', 'ccc', 'aaaa']
```

## custoem soring using my fucntion
```python
  ## Say we have a list of strings we want to sort by the last letter of the string.
  strs = ['xc', 'zb', 'yd' ,'wa']

  ## Write a little function that takes a string, and returns its last letter.
  ## This will be the key function (takes in 1 value, returns 1 value).
  def MyFn(s):
    return s[-1]

  ## Now pass key=MyFn to sorted() to sort by the last letter:
  print(sorted(strs, key=MyFn))  ## ['wa', 'zb', 'xc', 'yd']
```
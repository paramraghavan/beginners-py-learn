The command `python -m trace --trace test_jwt.py` runs Python's built-in trace module to show **every single line of
code** that gets executed when running your script.

## What it does:

- **Line-by-line execution tracing**: Shows each line as it's executed
- **Import tracing**: Shows what happens during module imports
- **Function call tracing**: Shows when functions are entered/exited
- **Module loading**: Shows which files are loaded and in what order

## Sample output format:

```
 --- modulename: test_jwt, funcname: <module>
test_jwt.py(1): import jwt
 --- modulename: jwt, funcname: <module>
/path/to/jwt/__init__.py(1): # JWT library
/path/to/jwt/__init__.py(2): from .api import encode, decode
 --- modulename: api, funcname: <module>
/path/to/jwt/api.py(1): import base64
...
test_jwt.py(2): token = jwt.decode(...)
 --- modulename: jwt, funcname: decode
```

## For your JWT debugging specifically:

This will show you:

1. **Which JWT module** is actually being imported
2. **Where it's located** on disk
3. **What happens** when you try to call `jwt.decode()`
4. **Any import errors** or missing attributes

## Less verbose alternatives:

```bash
python -m trace --listfuncs test_jwt.py  # Just function calls
python -c "import jwt; print(jwt.__file__)"  # Quick module location check
```

The `--trace` option generates **a lot** of output, so you might want to redirect it to a file:

```bash
python -m trace --trace test_jwt.py > trace_output.txt 2>&1
```

This is much more useful than `strace` for Python debugging because it shows the actual Python code execution flow.
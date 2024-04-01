# getattr() and locals()
Both are python builtin functions

## getattr()
- usecase1
- **Dynamic Attribute Access**: getattr() allows you to access an attribute of an object dynamically using a string. This is
  useful when the name of the attribute is not known until runtime.
- **Default Values**: You can provide a default value to return in case the attribute does not exist, which can prevent
  AttributeError exceptions.
- **Reflection and Introspection**: It is used in reflective programming techniques where the program needs to inspect and
  manipulate its own structure.

## locals()
- usecase2
- **Debugging:** It is commonly used for debugging purposes to inspect the local variables within a function or a block
  of code.
- **Dynamic Variable Access:** You can use it to access local variables dynamically, similar to how getattr() is used
  for attributes.


## Simple Regex Notes

**Regex** means **regular expression**. It is used to search, match, extract, or replace text patterns.

Example uses:

```python
import re

text = "Order ID is 12345"
match = re.search(r"\d+", text)

print(match.group())  # 12345
```

## Common Regex Symbols

| Regex   | Meaning                      | Example                             |      |      |
|---------|------------------------------|-------------------------------------|------|------|
| `.`     | Any one character            | `a.c` matches `abc`, `axc`          |      |      |
| `\d`    | Any digit                    | `\d` matches `5`                    |      |      |
| `\D`    | Not a digit                  | `\D` matches `A`                    |      |      |
| `\w`    | Letter, digit, or underscore | `\w` matches `a`, `7`, `_`          |      |      |
| `\W`    | Not letter/digit/underscore  | `\W` matches `@`, `#`               |      |      |
| `\s`    | Whitespace                   | space, tab, newline                 |      |      |
| `\S`    | Not whitespace               | `A`, `1`, `$`                       |      |      |
| `^`     | Start of string              | `^Hello`                            |      |      |
| `$`     | End of string                | `end$`                              |      |      |
| `*`     | 0 or more times              | `ab*` matches `a`, `ab`, `abb`      |      |      |
| `+`     | 1 or more times              | `ab+` matches `ab`, `abb`           |      |      |
| `?`     | 0 or 1 time                  | `colou?r` matches `color`, `colour` |      |      |
| `{n}`   | Exactly n times              | `\d{3}` matches `123`               |      |      |
| `{n,}`  | n or more times              | `\d{2,}`                            |      |      |
| `{n,m}` | Between n and m times        | `\d{2,4}`                           |      |      |
| `[]`    | One character from set       | `[aeiou]`                           |      |      |
| `[^]`   | Not in set                   | `[^0-9]`                            |      |      |
| `       | `                            | OR                                  | `cat | dog` |
| `()`    | Group                        | `(abc)+`                            |      |      |

## Common Patterns

### Match a number

```python
r"\d+"
```

Matches:

```text
123
45
9000
```

### Match a word

```python
r"\w+"
```

Matches:

```text
hello
abc123
name_1
```

### Match an email, simple version

```python
r"\w+@\w+\.\w+"
```

Matches:

```text
test@gmail.com
```

Better version:

```python
r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
```

### Match a phone number

```python
r"\d{3}-\d{3}-\d{4}"
```

Matches:

```text
703-555-1234
```

### Match date like `2026-05-10`

```python
r"\d{4}-\d{2}-\d{2}"
```

## Python Regex Functions

### `re.search()`

Finds first match anywhere.

```python
re.search(r"\d+", "abc123")
```

### `re.match()`

Checks from the beginning only.

```python
re.match(r"\d+", "123abc")
```

### `re.findall()`

Finds all matches.

```python
re.findall(r"\d+", "A12 B34 C56")
# ['12', '34', '56']
```

### `re.sub()`

Replaces matching text.

```python
re.sub(r"\d+", "XXX", "Order 123")
# Order XXX
```

### `re.split()`

Splits text using a pattern.

```python
re.split(r"\s+", "hello   world")
# ['hello', 'world']
```

## Important Tip: Use Raw Strings

Always prefer:

```python
r"\d+"
```

instead of:

```python
"\\d+"
```

The `r` means **raw string**, which makes regex easier to read.

## Simple Example

```python
import re

text = "Customer ID: 4567, Amount: 89.50"

ids = re.findall(r"\d+", text)

print(ids)
```

Output:

```text
['4567', '89', '50']
```

## Quick Mental Model

Regex is like a **search pattern language**.

```text
\d+        one or more digits
\w+        one or more word characters
\s+        one or more spaces
[A-Z]+     one or more capital letters
.*         anything
```

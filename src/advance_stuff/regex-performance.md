# Regex Performance

```python
import re
import time
from timeit import timeit

# 1. Compiled vs Non-Compiled Regex
text = "Hello world! " * 10000


def using_compiled():
    pattern = re.compile(r'world')
    return pattern.findall(text)


def using_non_compiled():
    return re.findall(r'world', text)


# Benchmark
print("Compiled vs Non-Compiled:")
print(f"Compiled: {timeit(using_compiled, number=1000):.4f} seconds")
print(f"Non-compiled: {timeit(using_non_compiled, number=1000):.4f} seconds")
```

**Key Performance Tips:**

1. **Catastrophic Backtracking**

```python
# Bad pattern - exponential time
bad_pattern = r'(a+)+b'
text = 'a' * 25 + 'c'  # Will be very slow

# Better pattern - linear time
good_pattern = r'a+b'

# Example of how to avoid backtracking
# Bad: Nested quantifiers
bad_email = r'^([a-zA-Z0-9]+)*@example\.com$'
# Good: Avoid nesting
good_email = r'^[a-zA-Z0-9]+@example\.com$'
```

2. **Anchors for Early Termination**

```python
# Without anchors - must scan entire string
slow_pattern = re.compile(r'python')

# With anchors - can fail fast
fast_pattern = re.compile(r'^python')


def test_anchors():
    long_text = "x" * 1000000 + "python"

    # Slow - must scan entire string
    start = time.time()
    slow_pattern.search(long_text)
    print(f"Without anchors: {time.time() - start:.4f} seconds")

    # Fast - fails immediately
    start = time.time()
    fast_pattern.search(long_text)
    print(f"With anchors: {time.time() - start:.4f} seconds")
```

3. **Greedy vs Non-Greedy**

```python
text = "<tag>content</tag>" * 10000

# Greedy (slower for this case)
greedy_pattern = re.compile(r'<.*>')

# Non-greedy (faster)
non_greedy_pattern = re.compile(r'<.*?>')


def compare_greedy():
    # Greedy will try to match as much as possible
    start = time.time()
    greedy_pattern.findall(text)
    print(f"Greedy: {time.time() - start:.4f} seconds")

    # Non-greedy stops at first match
    start = time.time()
    non_greedy_pattern.findall(text)
    print(f"Non-greedy: {time.time() - start:.4f} seconds")
```

4. **Character Classes vs Complex Patterns**

```python
# Slower - complex pattern
complex_pattern = re.compile(r'[aeiou]|[AEIOU]')

# Faster - simple character class
simple_pattern = re.compile(r'[aeiouAEIOU]')

text = "The quick brown fox" * 10000


def compare_patterns():
    # Complex pattern
    start = time.time()
    complex_pattern.findall(text)
    print(f"Complex: {time.time() - start:.4f} seconds")

    # Simple pattern
    start = time.time()
    simple_pattern.findall(text)
    print(f"Simple: {time.time() - start:.4f} seconds")
```

5. **Look-ahead and Look-behind Impact**

```python
text = "password123" * 10000

# Without lookahead (faster)
simple = re.compile(r'\d+')

# With lookahead (slower)
complex = re.compile(r'(?=.*\d+).*')


def compare_lookaround():
    start = time.time()
    simple.search(text)
    print(f"Without lookaround: {time.time() - start:.4f} seconds")

    start = time.time()
    complex.search(text)
    print(f"With lookaround: {time.time() - start:.4f} seconds")
```

6. **Using Alternative Methods When Possible**

```python
text = "The quick brown fox jumps over the lazy dog"


# Slower - regex for simple substring
def using_regex():
    return bool(re.search(r'quick', text))


# Faster - string method
def using_string():
    return 'quick' in text


# Much faster for simple cases
print("Simple substring search:")
print(f"Regex: {timeit(using_regex, number=100000):.4f} seconds")
print(f"String method: {timeit(using_string, number=100000):.4f} seconds")
```

**Best Practices for Performance:**

1. Compile patterns you'll use multiple times
2. Use string methods for simple operations
3. Be careful with nested quantifiers
4. Use anchors when possible
5. Prefer non-greedy quantifiers when appropriate
6. Use simpler patterns when possible
7. Be aware of backtracking
8. Test with realistic data sizes

The key to regex performance is understanding these patterns and choosing the right approach for your specific use case.
Sometimes, a slightly less efficient regex might be more maintainable and clearer, which could be the better choice for
your application.
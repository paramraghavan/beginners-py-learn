# Bad pattern - exponential time

bad_pattern = r'(a+)+b'
text = 'a' * 25 + 'c' # Will be very slow

Let see why `(a+)+b` is a problematic regex pattern that leads to catastrophic backtracking. Let's analyze step by step:

1. **Pattern Breakdown:**
   ```python
   (a+)+b
   ```
    - `a+` means "match one or more 'a' characters"
    - The outer `()+` means "match the group one or more times"
    - `b` means "match the letter 'b'"

2. **The Problem Scenario:**
   ```python
   text = 'a' * 25 + 'c'  # Creates "aaaaaaaaaaaaaaaaaaaaaaaac"
   ```

3. **Here's what happens when trying to match:**
# Let's see how the regex engine tries to match:

Step 1: First a+ group tries these possibilities:
- a
- aa
- aaa
- aaaa
- ... (all the way up to consuming all 25 'a's)

Step 2: For EACH of those possibilities, it then tries the outer + group:
- (a)
- (aa)
- (aaa)
- (a)(a)
- (aa)(a)
- (a)(aa)
- (aaa)(a)
- (a)(aaa)
... and so on

Step 3: After each attempt, it looks for 'b'
- If 'b' isn't found (which it isn't - we have 'c'), 
  it backtracks and tries another combination

**Why It's Exponential:**

```python
# For a string of n 'a's, the number of possible combinations is approximately 2^n
# With 25 'a's, that's 2^25 = 33,554,432 combinations!

# Here's a demonstration:
import re
import time


def test_bad_pattern(n):
    pattern = re.compile(r'(a+)+b')
    text = 'a' * n + 'c'

    start = time.time()
    try:
        pattern.match(text)
    except:
        pass
    return time.time() - start


# Try with increasing lengths
for i in range(15, 30, 5):
    print(f"Length {i}: {test_bad_pattern(i):.4f} seconds")
```

**The Better Solution:**

```python
# Instead, use:
good_pattern = r'a+b'

# This pattern is linear because:
# 1. It simply matches one or more 'a's
# 2. Then looks for a 'b'
# 3. No backtracking needed - just one pass through the string
```

**Real-World Example:**

```python
# A common mistake in email validation:

# Bad pattern (can be slow):
email_bad = re.compile(r'([A-Za-z0-9])+@domain\.com')

# Better pattern:
email_good = re.compile(r'[A-Za-z0-9]+@domain\.com')

# The difference is subtle but important:
# - Bad pattern can try multiple ways to group the characters
# - Good pattern simply matches them in one go
```

The key takeaway is to avoid nested quantifiers (`+` or `*`) when possible, as they can lead to exponential
backtracking. Always try to write patterns that can match the string in a single pass without needing to try multiple
combinations.

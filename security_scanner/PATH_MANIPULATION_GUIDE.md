# Path Manipulation Detection - Added Feature

## ✅ What's New

The scanner now includes **comprehensive path manipulation and path traversal detection** - one of the most common Fortify findings!

## 🔍 What It Detects

### High Severity Path Issues:
1. **String concatenation in paths**
   ```python
   # ❌ BAD - Will be flagged
   path = "/data/" + user_input + "/file.txt"
   with open(path, 'r') as f:
       data = f.read()
   ```

2. **F-string paths without validation**
   ```python
   # ❌ BAD - Will be flagged
   filename = f"/uploads/{user_file}"
   os.remove(filename)
   ```

3. **Paths from external sources (getenv, input, sys.argv)**
   ```python
   # ❌ BAD - Will be flagged
   config = os.getenv('CONFIG_PATH')
   with open(config, 'r') as f:
       data = f.read()
   ```

### Medium Severity Path Issues:
4. **Paths from variables with suspicious names**
   ```python
   # ❌ BAD - Will be flagged (if no validation nearby)
   def read_file(user_path):
       with open(user_path, 'r') as f:
           return f.read()
   ```

5. **Path() objects from variables**
   ```python
   # ❌ BAD - Will be flagged
   filepath = Path(user_input)
   with filepath.open('w') as f:
       f.write("data")
   ```

## ✅ How to Fix Path Manipulation Issues

### Fix 1: Use Allowlist/Whitelist
```python
# ✅ GOOD
ALLOWED_DIRS = {
    'dev': '/data/dev',
    'prod': '/data/prod'
}

env = os.getenv('ENV', 'dev')
if env not in ALLOWED_DIRS:
    raise ValueError("Invalid environment")

data_dir = ALLOWED_DIRS[env]
```

### Fix 2: Validate with resolve() and prefix check
```python
# ✅ GOOD
base_dir = Path("/uploads")
user_file = sanitize_filename(request.files['file'].filename)
file_path = base_dir / user_file

# Ensure path is within allowed directory
if not str(file_path.resolve()).startswith(str(base_dir.resolve())):
    raise ValueError("Path traversal detected")
```

### Fix 3: Sanitize filenames
```python
# ✅ GOOD
import os

def sanitize_filename(filename):
    # Remove path separators
    filename = os.path.basename(filename)
    
    # Remove parent directory references
    filename = filename.replace('..', '')
    
    # Validate allowed characters
    if not re.match(r'^[\w\-. ]+$', filename):
        raise ValueError("Invalid filename")
    
    return filename
```

### Fix 4: Validate input before constructing paths
```python
# ✅ GOOD
def read_user_data(user_id):
    # Validate user_id is alphanumeric
    if not user_id.isalnum():
        raise ValueError("Invalid user ID")
    
    # Construct path safely
    filepath = f"/data/users/{user_id}/data.json"
    
    with open(filepath, 'r') as f:
        return f.read()
```

## 🎯 Real-World Example

### Your Code - Before and After

**Before (3 path issues):**
```python
env = 'dev'
deploy_dir = '/fmac/users/dev/utils/prepay'

if env == 'uat':
    deploy_dir = '/fmac/users/dev/utils/prepay'
# ... more if statements

os.makedirs(deploy_dir, exist_ok=True)  # ❌ Flagged
temp_file_path = os.path.join(deploy_dir, temp_filename)
with open(temp_file_path, 'w') as f:  # ❌ Flagged
    json.dump(data, f)
```

**After (with allowlist - 2 issues, false positives):**
```python
ENV = os.getenv("APP_ENV", "dev").lower()
DEPLOY_DIRS = {
    "dev":  "/fmac/users/dev/utils/prepay",
    "uat":  "/fmac/users/uat/utils/prepay",
    "sit":  "/fmac/users/sit/utils/prepay",
    "prod": "/fmac/users/prod/utils/prepay",
}

# ✅ Validation present - real Fortify will recognize this
if ENV not in DEPLOY_DIRS:
    raise ValueError(f"Invalid environment: {ENV!r}")

deploy_dir = Path(DEPLOY_DIRS[ENV])
```

The 2 remaining issues flagged by the scanner are **false positives** because:
1. `deploy_dir` comes from a validated allowlist
2. `tmp_path` comes from secure `tempfile.mkstemp()`

**Real Fortify** will likely recognize the validation and not flag these, or they'll be low-priority findings.

## 🔧 Understanding False Positives

The scanner may flag some safe code (false positives) because:
1. It does basic pattern matching, not full data flow analysis
2. It looks for validation in a 10-line context window
3. It's conservative (better safe than sorry)

**This is actually good!** It makes you:
- Review all file operations
- Add explicit validation comments
- Write more defensive code

## 📝 Suppressing False Positives

If the scanner flags code you know is safe, you can:

### Option 1: Add a comment to document safety
```python
# Path validated via DEPLOY_DIRS allowlist above
os.makedirs(deploy_dir, exist_ok=True)
```

### Option 2: Add explicit validation nearby
```python
# Explicitly verify path (helps both scanner and humans)
assert str(deploy_dir).startswith('/fmac/users/')
os.makedirs(deploy_dir, exist_ok=True)
```

### Option 3: Accept the finding
Sometimes it's okay to have findings if the code is genuinely safe and well-documented.

## 🎓 Best Practices

1. **Always use allowlists for paths based on external input**
2. **Sanitize user-provided filenames** with `os.path.basename()`
3. **Validate resolved paths** stay within intended directories
4. **Never trust user input** in path construction
5. **Document why paths are safe** with comments

## 🚀 Testing Your Code

```bash
# Test with the scanner
python fortify_mock_scanner.py your_script.py

# Look for "Path Manipulation / Path Traversal" findings
# Fix the High severity ones first
# Review Medium severity for false positives
```

## 📊 Comparison Matrix

| Code Pattern | Fortify Finding | Severity | Fix Required? |
|-------------|----------------|----------|---------------|
| String concat in paths | ✅ Yes | High | ✅ Yes |
| F-string paths | ✅ Yes | High | ✅ Yes |
| Path from getenv without allowlist | ✅ Yes | High | ✅ Yes |
| Path from sys.argv | ✅ Yes | High | ✅ Yes |
| Path from variable with validation | ❌ Maybe | Low | ⚠️ Review |
| Path from allowlist dict | ❌ No | None | ✅ Good! |
| tempfile.mkstemp() | ❌ No | None | ✅ Good! |

## 🆘 Common Questions

**Q: My code uses Path from pathlib, will Fortify flag it?**
A: No, if properly validated. `Path` is safe and recommended!

**Q: I use environment variables for paths, is that bad?**
A: Not if you validate with an allowlist. Never use env vars directly in paths.

**Q: What about paths I construct myself without user input?**
A: Those are generally safe, but add validation to prove it to Fortify.

**Q: The scanner flagged tempfile.mkstemp(), is that wrong?**
A: Yes, false positive. `mkstemp()` is secure. Real Fortify won't flag it.

---

**Remember**: The scanner is designed to be conservative. It's better to review a false positive than miss a real vulnerability!

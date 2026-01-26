# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Download the Scanner
```bash
# Save fortify_mock_scanner.py to your project directory
# or add it to a central location
```

### Step 2: Run Your First Scan
```bash
# Scan a single file
python fortify_mock_scanner.py myfile.py

# Scan your entire project
python fortify_mock_scanner.py .
```

### Step 3: Fix Issues
The scanner will show you:
- **What** the issue is
- **Where** it's located (file and line number)
- **Why** it's a problem
- **How** to fix it

### Step 4: Verify Your Fixes
```bash
# Re-run the scanner
python fortify_mock_scanner.py myfile.py

# Should show: ✓ No security issues found!
```

## 📋 Daily Workflow

```bash
# 1. Write your code
vim app.py

# 2. Scan for issues
python fortify_mock_scanner.py app.py

# 3. Fix any issues found
vim app.py

# 4. Verify fixes
python fortify_mock_scanner.py app.py

# 5. Commit and push
git add app.py
git commit -m "Added feature X with security fixes"
git push

# 6. Jenkins runs real Fortify (should pass!)
```

## 🎯 Most Common Issues & Quick Fixes

### 1. SQL Injection
**❌ Bad:**
```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```
**✅ Good:**
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### 2. Hardcoded Secrets
**❌ Bad:**
```python
API_KEY = ""
```
**✅ Good:**
```python
import os
API_KEY = os.getenv('API_KEY')
```

### 3. Command Injection
**❌ Bad:**
```python
os.system(f"ping {hostname}")
```
**✅ Good:**
```python
subprocess.run(['ping', hostname], shell=False)
```

### 4. Weak Hashing
**❌ Bad:**
```python
hashlib.md5(password.encode()).hexdigest()
```
**✅ Good:**
```python
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### 5. Weak Random
**❌ Bad:**
```python
import random
token = str(random.randint(100000, 999999))
```
**✅ Good:**
```python
import secrets
token = secrets.token_urlsafe(32)
```

## 🔧 Integration Options

### Option 1: Manual (Before Each Commit)
```bash
python fortify_mock_scanner.py .
```

### Option 2: Git Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python fortify_mock_scanner.py . --fail-on high
if [ $? -ne 0 ]; then
    echo "❌ Security issues found! Fix before committing."
    exit 1
fi
```
```bash
chmod +x .git/hooks/pre-commit
```

### Option 3: IDE Integration
**VS Code - Add to tasks.json:**
```json
{
  "label": "Security Scan",
  "type": "shell",
  "command": "python fortify_mock_scanner.py ${file}"
}
```

### Option 4: Makefile
```makefile
.PHONY: security-scan
security-scan:
	python fortify_mock_scanner.py . --fail-on high

.PHONY: test
test: security-scan
	pytest
```

## 📊 Understanding Results

### Exit Codes
- `0` = Clean or only Low/Medium issues
- `1` = Issues at or above your --fail-on threshold
- `2` = Critical issues found

### Severity Levels
- **Critical** = Immediate security risk (SQL injection, hardcoded secrets)
- **High** = Serious vulnerability (weak crypto, command injection)
- **Medium** = Should fix before production (weak random, debug code)
- **Low** = Best practice violations

## ⚡ Pro Tips

1. **Run Early, Run Often** - Don't wait until you're done coding
2. **Start with Critical** - Fix highest severity issues first
3. **Read the CWE** - Understanding the vulnerability helps prevent it
4. **Test Your Fixes** - Some fixes can break functionality
5. **False Positives** - If you're certain code is safe, document why
6. **Use --json** - Generate reports for tracking over time

## 🆘 Troubleshooting

### "No issues found but Fortify still failing?"
This scanner catches common patterns but isn't a complete replacement. Fortify may find:
- Complex data flow issues
- Framework-specific vulnerabilities
- Context-aware issues this scanner can't detect

### "Too many false positives?"
Some code may be flagged incorrectly. Options:
1. Add validation/sanitization to prove safety
2. Refactor to avoid the pattern
3. Document why it's safe in comments
4. Accept the finding if code is genuinely risky

### "Scanner crashes on my file?"
- Check for syntax errors in your Python file
- Make sure file encoding is UTF-8
- Try scanning individual files to isolate the issue

## 📞 Support

- **For this scanner**: Modify the script as needed for your use case
- **For real Fortify**: Contact your DevOps/Security team
- **For security questions**: Consult your organization's security guidelines

---

**Remember**: This scanner is a **time-saving tool**, not a security audit. Always run the official Fortify scan in Jenkins as your final verification!

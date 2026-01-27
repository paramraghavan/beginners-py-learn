# Local Security Scanner - Fortify Mock

A local Python security scanner that mimics Fortify SCA checks. This allows you to catch and fix security vulnerabilities **before** running your Jenkins build with the actual Fortify scanner.

## What It Checks

This scanner detects the following security issues that Fortify typically flags:

### Critical Severity
- **SQL Injection** (CWE-89) - String concatenation, f-strings, .format() in SQL queries
- **Command Injection** (CWE-78) - os.system(), eval(), exec(), subprocess with shell=True
- **Hardcoded Credentials** (CWE-798) - Passwords, API keys, secrets in code
- **Unsafe Deserialization** (CWE-502) - pickle.loads() with untrusted data

### High Severity
- **Path Traversal** (CWE-22) - File operations without path validation
- **Weak Cryptography** (CWE-327) - MD5, SHA1, DES, RC4
- **XML External Entity (XXE)** (CWE-611) - Unsafe XML parsing

### Medium Severity
- **Weak Random** (CWE-330) - Using random module for security
- **Information Exposure** (CWE-489) - Debug code printing secrets
- **Insecure Protocol** (CWE-319) - HTTP instead of HTTPS
- **Insecure Temp Files** (CWE-377) - mktemp usage

## Installation

No installation required! Just download the scanner:

```bash
# Download the scanner
curl -O https://your-repo/fortify_mock_scanner.py

# Make it executable (Linux/Mac)
chmod +x fortify_mock_scanner.py
```

## Usage

### Scan a Single File
```bash
python fortify_mock_scanner.py my_script.py
```

### Scan Entire Project Directory
```bash
python fortify_mock_scanner.py /path/to/your/project
```

### Generate JSON Report
```bash
python fortify_mock_scanner.py my_script.py --json security_report.json
```

### Exclude Directories
```bash
python fortify_mock_scanner.py . --exclude venv tests migrations
```

### Fail Build on High/Critical Issues
```bash
python fortify_mock_scanner.py . --fail-on high
```

## Example Output

```
================================================================================
SECURITY SCAN RESULTS (Fortify-Style)
================================================================================

SUMMARY:
  Total Issues Found: 15
  Critical: 5
  High: 7
  Medium: 3
  Low: 0

ISSUES BY CATEGORY:
  SQL Injection: 3
  Command Injection / Code Injection: 3
  Hardcoded Password/Secret: 3
  Weak Cryptography: 2
  Path Traversal: 1
  Weak Random Number Generator: 2
  Unsafe Deserialization: 1

================================================================================
DETAILED FINDINGS:
================================================================================

[1] CRITICAL: SQL Injection
    File: app.py
    Line: 23
    Code: query = "SELECT * FROM users WHERE username = '" + username + "'"
    Issue: SQL query constructed using string concatenation with potentially unsafe input
    Fix: Use parameterized queries with placeholders (?, %s) instead of string concatenation
    CWE: CWE-89


```

## Workflow Integration

### 1. Local Development Workflow
```bash
# Before committing code
python fortify_mock_scanner.py src/

# Fix any issues found
# Re-scan to verify fixes
python fortify_mock_scanner.py src/

# Commit and push
git add .
git commit -m "Fixed security issues"
git push
```

### 2. Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "Running security scan..."
python fortify_mock_scanner.py . --fail-on high

if [ $? -ne 0 ]; then
    echo "Security scan failed! Fix issues before committing."
    exit 1
fi
```

### 3. CI/CD Integration
Add to your `.gitlab-ci.yml` or `Jenkinsfile`:
```yaml
security-scan:
  stage: test
  script:
    - python fortify_mock_scanner.py . --json security-report.json --fail-on high
  artifacts:
    reports:
      - security-report.json
```

## Common Fixes

### SQL Injection
**Bad:**
```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

**Good:**
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Hardcoded Secrets
**Bad:**
```python
```

**Good:**
```python
import os
API_KEY = os.getenv('API_KEY')
```

### Command Injection
**Bad:**
```python
subprocess.run(f"ls {user_input}", shell=True)
```

**Good:**
```python
subprocess.run(['ls', user_input], shell=False)
```

### Weak Cryptography
**Bad:**
```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Good:**
```python
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Weak Random
**Bad:**
```python
import random
token = str(random.randint(100000, 999999))
```

**Good:**
```python
import secrets
token = secrets.token_urlsafe(32)
```

## Limitations

This is a **mock scanner** that catches common patterns. It may:
- Produce false positives (flag safe code)
- Miss issues the real Fortify scanner would catch
- Not understand complex data flow

Always run the official Fortify scan in Jenkins as the final verification.

## Exit Codes

- `0` - No issues or only Low/Medium issues found
- `1` - Issues found at or above --fail-on threshold
- `2` - Critical issues found (when not using --fail-on)

## Tips

1. **Run frequently** - Scan after every significant code change
2. **Fix iteratively** - Start with Critical issues, then High, then Medium
3. **Test your fixes** - Re-run the scanner to confirm issues are resolved
4. **Don't disable warnings** - If flagged, investigate even if you think it's safe
5. **Use with real Fortify** - This is a supplement, not a replacement

## Support

For issues or questions about the real Fortify scanner, contact your DevOps team.
For issues with this mock scanner, check the script's inline comments or modify as needed.

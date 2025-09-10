

## Your Specific Use Case - URL in JSON to Lambda

The linter detects this pattern:

```python
# This would trigger a "URL_IN_JSON_PAYLOAD" violation
payload = {
    "response_url": request.args.get('url'),  # User-controlled URL
    "callback_url": "https://external-api.com/webhook"
}
lambda_client.invoke(FunctionName='handler', Payload=json.dumps(payload))
```

**Detection Logic**: The `_check_url_security()` function identifies when URLs are embedded in JSON structures being
sent to AWS Lambda or other services, flagging potential SSRF (Server-Side Request Forgery) vulnerabilities.

## Extended Features and Integration## Complete Security Linting Solution

Now you have a comprehensive security linter with these additional capabilities:

### **CI/CD Integration**

```bash
# GitHub Actions integration
python security_linter.py --package . --format json | python -c "
import json, sys
data = json.load(sys.stdin)
print(f'::set-output name=violations::{len(data)}')
if data: sys.exit(1)
"

# Pre-commit hook setup
python -c "from security_linter import create_precommit_hook; create_precommit_hook()"
```

### **Configuration File Support**

Create a `.security-lint.json` file:

```json
{
  "exclude_patterns": [
    "*/tests/*",
    "*/venv/*"
  ],
  "severity_levels": {
    "HIGH": true,
    "MEDIUM": true,
    "LOW": false
  },
  "integrations": {
    "aws": true,
    "snowflake": true,
    "vault": true,
    "kubernetes": false
  }
}
```

### **Your URL-in-JSON Use Case**

The linter specifically catches patterns like:

```python
# DETECTED: URL_IN_JSON_PAYLOAD violation
payload = {
    "response_url": request.form.get('callback'),  # User input → SSRF risk
    "webhook_url": f"https://{user_domain}/hook"  # Domain injection
}
lambda_client.invoke(FunctionName='processor', Payload=json.dumps(payload))
```

**Suggested Fix**:

```python
# SECURE: Validate URLs against allowlist
ALLOWED_DOMAINS = ['trusted-api.com', 'internal.company.com']


def validate_callback_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return (parsed.netloc in ALLOWED_DOMAINS and
            parsed.scheme == 'https')


# Only include validated URLs
if validate_callback_url(callback_url):
    payload = {"response_url": callback_url}
```

### **Integration with Other Tools**

The linter works alongside popular tools:

1. **Bandit** (OWASP standard): `pip install bandit`
2. **Safety** (dependency scanner): `pip install safety`
3. **Semgrep** (advanced patterns): `pip install semgrep`
4. **Pre-commit hooks**: Automatic scanning before commits

### **Real-World Example**

For your specific scenario with Lambda and JSON payloads:

```bash
# Scan your Lambda handlers
python security_linter.py --package ./lambda_functions/ --severity HIGH --fix

# Generate CI/CD report
python security_linter.py --package . --format sarif --output security-results.sarif

# Focus on URL/SSRF issues only
python security_linter.py --file handler.py | grep "URL_IN_JSON_PAYLOAD\|SSRF"
```

The linter provides detailed suggestions for each violation type, making it easy to understand and fix security issues
across your AWS, Snowflake, HashiCorp Vault, and other cloud service integrations.
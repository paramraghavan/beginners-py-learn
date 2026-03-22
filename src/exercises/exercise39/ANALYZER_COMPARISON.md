# AWS Permission Analyzers Comparison

Two flavors of permission analyzers are available. Choose based on your use case.

## 1. Static Analysis (`permission_analyzer.py`)

**How it works:** Parses Python code using regex to find boto3 calls, then maps them to required IAM permissions.

### Pros ✅
- **Fast** - No code execution needed
- **Safe** - Doesn't actually call AWS (no side effects)
- **Good for review** - See what code intends to do
- **Easy debugging** - Can inspect the regex matching
- **Works offline** - No AWS credentials needed

### Cons ❌
- **Limited accuracy** - Only catches explicit boto3 calls in code
- **Misses dynamic code** - Won't detect runtime-determined permissions
- **False positives** - May suggest permissions for code paths not executed
- **Partial patterns** - Won't catch complex variable patterns
- **Guesses permissions** - Based on method names, not actual errors

### Best For
```python
# ✓ Simple, straightforward boto3 code
s3 = boto3.client('s3')
s3.put_object(Bucket='bucket', Key='key', Body=data)

# ✓ Code review and planning
# ✓ Quick permission audits
# ✓ Offline analysis
```

### Usage
```bash
python permission_analyzer.py --code-file your_app.py
```

---

## 2. Runtime Analysis (`permission_analyzer_runtime.py`)

**How it works:** Executes your code, intercepts AWS permission exceptions, suppresses them, and tracks what permissions failed.

### Pros ✅
- **Highly accurate** - Catches real permission errors
- **Dynamic code** - Works with any boto3 pattern
- **No guessing** - Reports actual errors, not predictions
- **Complex logic** - Handles conditional code, loops, etc.
- **Real errors** - Catches exactly what AWS returns

### Cons ❌
- **Requires execution** - Needs AWS credentials and some setup
- **Side effects possible** - May make partial changes (use test account!)
- **Slower** - Makes actual AWS API calls
- **Complex setup** - Must prepare test environment
- **Non-permission errors** - May hit other issues first

### Best For
```python
# ✓ Complex application logic
if user.is_admin:
    s3.delete_bucket(Bucket=bucket)
else:
    s3.list_objects(Bucket=bucket)

# ✓ Dynamic resource names
for bucket in buckets_to_access:
    s3.put_object(Bucket=bucket, Key=key, Body=data)

# ✓ Verifying actual permissions in CI/CD
# ✓ Finding minimum required permissions
```

### Usage
```python
from permission_analyzer_runtime import PermissionTracker
import boto3

with PermissionTracker(verbose=True) as tracker:
    # Your actual AWS code
    s3 = boto3.client('s3')
    s3.put_object(Bucket='bucket', Key='file', Body=b'data')
    s3.get_object(Bucket='bucket', Key='file')

tracker.report()
```

---

## Quick Comparison Table

| Feature | Static | Runtime |
|---------|--------|---------|
| **Execution** | No code run | Executes code |
| **AWS Credentials** | Not needed | Required |
| **Speed** | Very fast | Slower (API calls) |
| **Accuracy** | ~60-70% | ~95-99% |
| **Dynamic code** | Limited | Full support |
| **Side effects** | None | Possible (use test account) |
| **Offline use** | ✅ Yes | ❌ No |
| **Complex logic** | Partial | Full |
| **Setup effort** | Minimal | Moderate |

---

## Common Scenarios

### Scenario 1: Quick Code Review
```
Use: Static Analysis ✓
Reason: Fast, no side effects, good for reviews
```

### Scenario 2: Deploying to Production
```
Use: Runtime Analysis ✓
Reason: Verify actual permissions needed, exact IAM policies
```

### Scenario 3: CI/CD Pipeline
```
Use: Runtime Analysis ✓
Reason: Catch permission issues before production
```

### Scenario 4: Learning AWS Permissions
```
Use: Static Analysis ✓
Reason: See mapping between code and permissions, no setup needed
```

### Scenario 5: Complex Application
```
Use: Runtime Analysis ✓
Reason: Handles conditional logic, dynamic names, real paths
```

### Scenario 6: Offline Development
```
Use: Static Analysis ✓
Reason: No internet or AWS access needed
```

---

## How to Use Both Together

For best results, use **both analyzers**:

```python
# Step 1: Quick static analysis to understand the code
python permission_analyzer.py --code-file app.py

# Step 2: Runtime analysis to verify actual requirements
from permission_analyzer_runtime import PermissionTracker
with PermissionTracker() as tracker:
    # Run your app
    from app import main
    main()
tracker.report()

# Step 3: Compare results and refine IAM policies
# Static: Suggested permissions
# Runtime: Required permissions
# Difference: Code paths not executed in test
```

---

## Technical Details

### Static Analysis
- **Pattern matching** with regex
- **No execution** - safe to run on untrusted code
- **Supported patterns:**
  - `s3 = boto3.client('s3')` then `s3.method()`
  - `boto3.client('s3').method()`
  - Basic variable tracking

### Runtime Analysis
- **Monkey-patches** botocore BaseClient
- **Intercepts** all boto3 client calls
- **Catches exceptions** before they propagate
- **Returns mock responses** to allow execution to continue
- **Tracks everything** including:
  - Actual permission errors
  - Service and operation names
  - Error codes and messages

---

## Permission Error Detection

### What Runtime Analyzer Catches
- `AccessDenied`
- `UnauthorizedOperation`
- `AccessDeniedException`
- `UnauthorizedException`
- `ForbiddenException`
- Service-specific permission errors

### What It Doesn't Catch
- Validation errors (invalid parameters)
- Network errors
- Rate limiting
- Resource not found errors
- Other non-permission exceptions

---

## Setting Up Runtime Analysis Safely

```python
# Option 1: Use a test AWS account
import os
os.environ['AWS_PROFILE'] = 'test-account'

# Option 2: Use a sandbox role with no real resources
# Ensure your test account has:
# - Empty S3 buckets (for testing)
# - Test EC2 instances (or none)
# - Test databases (or none)

# Option 3: Use LocalStack (local AWS emulator)
# Then run: localstack start
# Then use: boto3 with LocalStack endpoint
```

---

## Tips

### For Static Analysis
- Use for code reviews and documentation
- Include output in pull requests
- Use as starting point for IAM policies
- Fast way to understand permission requirements

### For Runtime Analysis
- Always use a test/dev environment
- Set resource quotas to prevent accidents
- Document what code paths were executed
- Use in CI/CD for final verification
- Compare with static analysis results

---

## Example: Full Workflow

```python
# 1. Static analysis during development
# python permission_analyzer.py --code-file myapp.py
# Output: Suggested permissions based on code inspection

# 2. Runtime analysis before deployment
from permission_analyzer_runtime import PermissionTracker
import myapp

with PermissionTracker() as tracker:
    myapp.run()

tracker.report()
# Output: Actual permissions needed from real execution

# 3. Generate minimal IAM policy
# Use the more restrictive set of required permissions
```

---

## Which Should I Use?

| Question | Answer |
|----------|--------|
| **Need quick analysis?** | Static |
| **In production/CI-CD?** | Runtime |
| **No AWS access?** | Static |
| **Have test AWS account?** | Runtime |
| **Code is simple/straightforward?** | Static |
| **Code is complex/dynamic?** | Runtime |
| **Want guaranteed accuracy?** | Runtime |
| **Want speed?** | Static |
| **Learning/documentation?** | Static then Runtime |

---

Choose **Static** for speed and safety. Choose **Runtime** for accuracy and completeness. Use **both** for comprehensive results! 🎯

# 🔒 Security Best Practices

> **Build Secure Python Applications**
>
> Complete guide to security fundamentals, vulnerabilities, authentication, and production-ready security practices.

---

## Table of Contents

1. [Security Fundamentals](#security-fundamentals)
2. [Input Validation & Sanitization](#input-validation--sanitization)
3. [SQL Injection Prevention](#sql-injection-prevention)
4. [Cross-Site Scripting (XSS) Prevention](#cross-site-scripting-xss-prevention)
5. [Cross-Site Request Forgery (CSRF)](#cross-site-request-forgery-csrf)
6. [Password Security](#password-security)
7. [Authentication & Sessions](#authentication--sessions)
8. [Authorization & Access Control](#authorization--access-control)
9. [Secure API Design](#secure-api-design)
10. [File Upload Security](#file-upload-security)
11. [Secrets & Environment Variables](#secrets--environment-variables)
12. [Dependency Security](#dependency-security)
13. [OWASP Top 10](#owasp-top-10)
14. [Security Checklist](#security-checklist)

---

## Security Fundamentals

### Security Principles

1. **Principle of Least Privilege** - Users get minimum permissions needed
2. **Defense in Depth** - Multiple layers of security
3. **Fail Securely** - Errors don't expose sensitive data
4. **Secure by Default** - Default configuration is secure
5. **Trust Nothing** - Validate everything
6. **Keep It Simple** - Complexity = more bugs
7. **Fix Security Issues** - Don't ignore warnings

### Attack Surface

An attack surface is all the ways an attacker can interact with your application:

```
User Input → Validation → Processing → Output
     ↓           ↓            ↓         ↓
  Forms      Validate      Query    Display
  APIs       Sanitize      Cache    Headers
  Files      Encode        File     Logs
  Params     Type-check    System
```

### Types of Attacks

| Attack | Mechanism | Impact | Prevention |
|--------|-----------|--------|-----------|
| **SQL Injection** | Malicious SQL in inputs | Data breach | Parameterized queries |
| **XSS** | Malicious JavaScript | Session hijacking | Input validation, encoding |
| **CSRF** | Forged requests | Unauthorized actions | CSRF tokens |
| **Brute Force** | Multiple login attempts | Account takeover | Rate limiting, MFA |
| **DDoS** | Flood with requests | Service unavailable | Rate limiting, WAF |
| **Man-in-Middle** | Intercept traffic | Data exposure | HTTPS, encryption |
| **Phishing** | Trick users | Credential theft | User education |

---

## Input Validation & Sanitization

### Validation vs Sanitization

**Validation** - Check if input is correct format
**Sanitization** - Clean input to remove harmful content

### Basic Validation

```python
from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v < 13:
            raise ValueError('User must be at least 13 years old')
        return v

# Usage
try:
    user = UserSignup(
        username='alice123',
        email='alice@example.com',
        password='SecurePass123',
        age=25
    )
except ValueError as e:
    print(f"Validation error: {e}")
```

### Type Checking

```python
# ✅ GOOD - Type hints help catch errors
from typing import Optional, List

def process_user(user_id: int, roles: List[str]) -> Optional[dict]:
    if not isinstance(user_id, int):
        raise TypeError("user_id must be integer")
    if not isinstance(roles, list):
        raise TypeError("roles must be list")
    return {"id": user_id, "roles": roles}

# ❌ BAD - No type hints, harder to validate
def process_user(user_id, roles):
    return {"id": user_id, "roles": roles}
```

### List Validation

```python
ALLOWED_ROLES = {'admin', 'user', 'guest'}

def validate_roles(roles: List[str]) -> List[str]:
    """Validate roles against whitelist"""
    validated = []
    for role in roles:
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role: {role}")
        validated.append(role)
    return validated

# Safe
safe_roles = validate_roles(['admin', 'user'])

# Will raise error
invalid_roles = validate_roles(['admin', 'superadmin'])  # ❌
```

---

## SQL Injection Prevention

### What is SQL Injection?

```python
# ❌ VULNERABLE - User input directly in SQL
user_input = "admin' --"
query = f"SELECT * FROM users WHERE username = '{user_input}'"
# Becomes: SELECT * FROM users WHERE username = 'admin' --'
# (Comment removes password check)
```

### Prevention: Parameterized Queries

```python
import sqlite3

# ✅ GOOD - Parameterized query
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

username = "admin' --"  # Malicious input
password = "anypassword"

# SQL injection prevented - input treated as data, not code
cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
)
result = cursor.fetchone()
conn.close()
```

### SQLAlchemy ORM (Prevents SQL Injection)

```python
from sqlalchemy.orm import Session
from sqlalchemy import text

# ✅ GOOD - ORM uses parameterized queries
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# ✅ GOOD - Raw SQL with parameters
user = db.execute(
    text("SELECT * FROM users WHERE username = :username"),
    {"username": username}
).fetchone()

# ❌ BAD - Don't do this
user = db.execute(text(f"SELECT * FROM users WHERE username = '{username}'"))
```

### Raw SQL Best Practices

```python
# ✅ GOOD - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ✅ GOOD - Use named parameters
cursor.execute(
    "SELECT * FROM users WHERE id = :id AND status = :status",
    {"id": user_id, "status": "active"}
)

# ❌ AVOID - String formatting
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ❌ AVOID - String concatenation
query = "SELECT * FROM users WHERE id = " + str(user_id)
cursor.execute(query)
```

---

## Cross-Site Scripting (XSS) Prevention

### What is XSS?

```python
# ❌ VULNERABLE - User input rendered in HTML
user_comment = "<script>alert('hacked')</script>"
html = f"<p>{user_comment}</p>"  # Script executes in browser!
```

### Prevention: HTML Encoding

```python
from html import escape

# ✅ GOOD - Escape HTML special characters
user_comment = "<script>alert('hacked')</script>"
safe_comment = escape(user_comment)
# Result: &lt;script&gt;alert(&#x27;hacked&#x27;)&lt;/script&gt;

html = f"<p>{safe_comment}</p>"
```

### In Templates

```html
<!-- ❌ VULNERABLE - Jinja2 without escaping -->
<p>{{ user_comment }}</p>

<!-- ✅ GOOD - Auto-escaping enabled (default) -->
<p>{{ user_comment | escape }}</p>

<!-- ✅ GOOD - If explicitly needed -->
<p>{{ user_comment | safe }}</p>  <!-- Only for trusted content -->
```

### Content Security Policy (CSP)

```python
from fastapi import FastAPI
from fastapi.middleware import CORSMiddleware

app = FastAPI()

# Add CSP header
@app.middleware("http")
async def add_csp_header(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://trusted-cdn.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self';"
    )
    return response
```

---

## Cross-Site Request Forgery (CSRF)

### What is CSRF?

Attacker tricks user into making unwanted requests while authenticated.

### Prevention: CSRF Tokens

```python
from fastapi import FastAPI, Form
from fastapi_csrf_protect import CsrfProtect
import secrets

app = FastAPI()

# Generate CSRF token
def generate_csrf_token():
    return secrets.token_urlsafe()

@app.get("/form")
async def get_form():
    csrf_token = generate_csrf_token()
    return {
        "html": f'<form method="post"><input type="hidden" name="csrf_token" value="{csrf_token}"><input type="submit"></form>'
    }

@app.post("/submit")
async def submit_form(csrf_token: str = Form(...)):
    # Validate CSRF token
    if not validate_csrf_token(csrf_token):
        raise ValueError("Invalid CSRF token")
    # Process form...
    return {"status": "ok"}
```

### SameSite Cookies

```python
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.post("/login")
async def login(username: str):
    response = Response("Logged in")
    response.set_cookie(
        "session",
        value="session_token_here",
        httponly=True,  # Not accessible via JavaScript
        secure=True,    # Only sent over HTTPS
        samesite="Strict"  # Only sent with same-site requests
    )
    return response
```

---

## Password Security

### Password Requirements

```python
import re
from typing import Tuple

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""

    if len(password) < 12:
        return False, "Password must be at least 12 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain digit"

    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain special character"

    return True, "Password is strong"

# Test
is_valid, message = validate_password("WeakPassword")
print(message)  # "Password must be at least 12 characters"
```

### Password Hashing

```python
import bcrypt
from typing import Tuple

class UserAuth:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Usage
user_password = "SecurePass123!"
hashed = UserAuth.hash_password(user_password)

# Later, verify
if UserAuth.verify_password("SecurePass123!", hashed):
    print("Password correct")
else:
    print("Password incorrect")
```

### Never Store Plaintext Passwords

```python
# ❌ VULNERABLE - Storing plaintext
class User(Base):
    __tablename__ = "users"
    password = Column(String(100))  # NEVER EVER!

# ✅ GOOD - Store hashed password
class User(Base):
    __tablename__ = "users"
    password_hash = Column(String(255))

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
```

---

## Authentication & Sessions

### JWT Tokens

```python
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Usage
@app.post("/login")
async def login(username: str, password: str):
    # Verify username/password
    token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(hours=1)
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
    return {"user_id": token.get("sub")}
```

### Secure Session Management

```python
# ✅ GOOD - Secure session configuration
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-secret-key",
    session_cookie="session",
    max_age=3600,  # 1 hour
    same_site="lax",
    https_only=True  # HTTPS only
)

@app.post("/login")
async def login(request: Request):
    request.session["user_id"] = user_id
    request.session["logged_in"] = True
```

---

## Authorization & Access Control

### Role-Based Access Control (RBAC)

```python
from enum import Enum
from typing import List

class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

def require_role(required_roles: List[UserRole]):
    """Dependency to check user role"""
    async def check_role(token: str = Depends(verify_token)):
        user_role = token.get("role")
        if user_role not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return token
    return check_role

# Usage
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user = Depends(require_role([UserRole.ADMIN]))
):
    # Only admins can delete users
    return {"deleted": user_id}
```

### Attribute-Based Access Control (ABAC)

```python
from typing import Callable

def check_permission(permission: str) -> Callable:
    """Check if user has specific permission"""
    async def check(token: str = Depends(verify_token)):
        user_permissions = token.get("permissions", [])
        if permission not in user_permissions:
            raise HTTPException(status_code=403, detail="Permission denied")
        return token
    return check

# Usage
@app.put("/posts/{post_id}")
async def update_post(
    post_id: int,
    data: dict,
    current_user = Depends(check_permission("post:write"))
):
    return {"updated": post_id}
```

---

## Secure API Design

### API Key Management

```python
from fastapi import Header, HTTPException

# ✅ GOOD - API key in header
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.get("/api/data")
async def get_data(api_key: str = Depends(verify_api_key)):
    return {"data": "sensitive"}

# ❌ BAD - API key in URL
@app.get("/api/data?api_key=secret")  # Will be logged!
```

### HTTPS Only

```python
from fastapi import HTTPException
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Redirect HTTP to HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Or check protocol
@app.middleware("http")
async def https_redirect(request, call_next):
    if request.url.scheme != "https" and not request.url.hostname == "localhost":
        return RedirectResponse(
            url=request.url.replace(scheme="https"),
            status_code=301
        )
    return await call_next(request)
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

# Limit to 10 requests per minute
@app.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, username: str, password: str):
    # Brute force protection
    return {"token": "..."}

# Limit to 100 requests per hour
@app.get("/api/data")
@limiter.limit("100/hour")
async def get_data(request: Request):
    return {"data": "..."}
```

---

## File Upload Security

### Validate File Uploads

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
import mimetypes
import magic

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check file extension
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # Check MIME type (not just extension)
    mime = magic.from_buffer(content, mime=True)
    allowed_mimes = {'application/pdf', 'image/jpeg', 'image/png', 'text/plain'}
    if mime not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Scan for malware (optional)
    # await scan_with_clamav(content)

    # Store securely
    filename = secure_filename(f"{uuid4()}_{file.filename}")
    with open(f"uploads/{filename}", "wb") as f:
        f.write(content)

    return {"filename": filename}
```

### Store Files Outside Web Root

```python
# ❌ BAD - Uploaded files in web-accessible directory
uploads_dir = "/app/static/uploads"

# ✅ GOOD - Store outside web root
uploads_dir = "/app/uploads"  # Outside static/public directories
```

---

## Secrets & Environment Variables

### Secure Configuration

```python
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    # Secrets (shouldn't be logged)
    database_password: SecretStr
    api_key: SecretStr
    jwt_secret: SecretStr

    # Non-secrets
    database_url: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

# Accessing secrets
password = settings.database_password.get_secret_value()  # Only when needed

# Don't do this - could leak in logs
print(settings.api_key)  # Won't print actual value ✓
```

### .env File Security

```
# .env (NEVER COMMIT to Git)
DATABASE_PASSWORD=super_secret_password_123
API_KEY=sk-proj-1234567890abcdef
JWT_SECRET=very-secret-jwt-key

# Add to .gitignore
echo ".env" >> .gitignore
```

### AWS Secrets Manager

```python
import boto3
import json

def get_secret(secret_name: str):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        raise ValueError(f"Error retrieving secret: {e}")

# Usage
db_credentials = get_secret('prod/database')
password = db_credentials['password']
```

---

## Dependency Security

### Scan for Vulnerabilities

```bash
# Check requirements.txt for known vulnerabilities
pip install safety
safety check

# Or with poetry
poetry check

# Scan with bandit (security linting)
pip install bandit
bandit -r src/
```

### Keep Dependencies Updated

```bash
# Show outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package_name

# Update all packages
pip install --upgrade -r requirements.txt
```

### Dependency Scanning in CI/CD

```yaml
# GitHub Actions
- name: Scan dependencies
  run: |
    pip install safety
    safety check --json

- name: Run bandit
  run: |
    pip install bandit
    bandit -r src/ -f json -o bandit.json
```

---

## OWASP Top 10

### A01: Broken Access Control

**Prevention:**
- Implement role-based access control (RBAC)
- Check permissions on every request
- Use principle of least privilege

### A02: Cryptographic Failures

**Prevention:**
- Use HTTPS for all traffic
- Encrypt sensitive data at rest
- Use strong algorithms (bcrypt, SHA-256)

### A03: Injection

**Prevention:**
- Use parameterized queries
- Input validation
- Object-Relational Mapping (ORM)

### A04: Insecure Design

**Prevention:**
- Security requirements in design phase
- Threat modeling
- Secure by default

### A05: Security Misconfiguration

**Prevention:**
- Remove unnecessary features
- Use security headers
- Keep dependencies updated

### A06: Vulnerable and Outdated Components

**Prevention:**
- Regular dependency updates
- Vulnerability scanning
- Use SCA tools

### A07: Authentication Failures

**Prevention:**
- Strong password requirements
- Multi-factor authentication (MFA)
- Rate limiting on login

### A08: Software and Data Integrity Failures

**Prevention:**
- Use signed packages
- Verify source code integrity
- Secure CI/CD pipeline

### A09: Logging and Monitoring Failures

**Prevention:**
- Log security events
- Monitor for suspicious activity
- Alert on anomalies

### A10: Server-Side Request Forgery (SSRF)

**Prevention:**
- Validate URLs
- Whitelist allowed hosts
- Disable unused protocols (FTP, Gopher)

---

## Security Checklist

### Development

- [ ] Input validation on all user inputs
- [ ] Parameterized queries for database
- [ ] Password hashing (bcrypt/Argon2)
- [ ] SQL injection prevention
- [ ] XSS prevention (HTML encoding)
- [ ] CSRF tokens on state-changing requests
- [ ] Rate limiting on sensitive endpoints
- [ ] Secure session configuration
- [ ] HTTPS only
- [ ] Security headers (CSP, X-Frame-Options, etc.)

### Secrets & Configuration

- [ ] No hardcoded secrets
- [ ] .env files in .gitignore
- [ ] Environment variables for secrets
- [ ] Secrets manager for production
- [ ] Different secrets per environment
- [ ] Rotate secrets regularly
- [ ] Audit secret access

### Authentication & Authorization

- [ ] Strong password requirements
- [ ] Multi-factor authentication (MFA)
- [ ] JWT tokens with expiration
- [ ] Secure token storage
- [ ] Role-based access control
- [ ] Permission checks on every request
- [ ] Principle of least privilege
- [ ] Session timeout

### API Security

- [ ] API key validation
- [ ] Rate limiting
- [ ] CORS properly configured
- [ ] Request validation
- [ ] Error messages don't leak info
- [ ] Log security events
- [ ] API versioning
- [ ] Deprecation warnings

### Dependency & Updates

- [ ] Regular dependency updates
- [ ] Vulnerability scanning (Safety, Bandit)
- [ ] Security patch process
- [ ] Dependency pinning versions
- [ ] Automated security updates
- [ ] Monitor for known vulnerabilities

### Deployment & Operations

- [ ] HTTPS with valid certificate
- [ ] Security headers configured
- [ ] WAF (Web Application Firewall)
- [ ] DDoS protection
- [ ] Intrusion detection
- [ ] Regular security audits
- [ ] Penetration testing
- [ ] Incident response plan

### Monitoring & Logging

- [ ] Security event logging
- [ ] Failed login tracking
- [ ] Suspicious activity alerts
- [ ] Log aggregation
- [ ] Regular log review
- [ ] Audit trail for sensitive operations
- [ ] PII not in logs
- [ ] Log retention policy

---

## Security Resources

- **OWASP Top 10** - owasp.org/www-project-top-ten
- **OWASP Cheat Sheet Series** - cheatsheetseries.owasp.org
- **CWE Top 25** - cwe.mitre.org/top25
- **Python Security** - python-guide.org/writing-great-code/security
- **FastAPI Security** - fastapi.tiangolo.com/tutorial/security
- **Cryptography Library** - cryptography.io

---

**Last Updated:** May 2026 | **Version:** 1.0

Related resources:
- [Database Operations Guide](database-operations-guide.md) - Secure database practices
- [Cloud & DevOps Guide](cloud-devops-guide.md) - Infrastructure security
- [Quick Reference Cards](quick-reference-cards.md) - Security commands

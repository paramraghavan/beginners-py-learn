# 🌐 Web Development Guide

> **Build Modern Web Applications with Python**
>
> Complete guide to web frameworks, REST APIs, WebSockets, authentication, and building production-ready web applications.

---

## Table of Contents

1. [Web Development Fundamentals](#web-development-fundamentals)
2. [HTTP & REST Principles](#http--rest-principles)
3. [FastAPI Basics](#fastapi-basics)
4. [FastAPI Advanced](#fastapi-advanced)
5. [Request & Response Handling](#request--response-handling)
6. [Authentication & JWT](#authentication--jwt)
7. [Database Integration](#database-integration)
8. [Error Handling](#error-handling)
9. [Testing APIs](#testing-apis)
10. [Flask Basics](#flask-basics)
11. [WebSockets & Real-time](#websockets--real-time)
12. [API Documentation](#api-documentation)
13. [Performance & Optimization](#performance--optimization)
14. [Real-World Examples](#real-world-examples)

---

## Web Development Fundamentals

### Client-Server Architecture

```
┌─────────────┐         HTTP Request         ┌──────────────┐
│  Browser    ├────────────────────────────→ │   Server     │
│  (Client)   │                              │  (Backend)   │
└─────────────┘ ← ──────────────────────────┘──────────────┘
                     HTTP Response
```

### Web Stack

```
Frontend (Client-side)
├── HTML - Structure
├── CSS - Styling
├── JavaScript - Interactivity
└── Frameworks: React, Vue, Angular

Backend (Server-side)
├── Python - Our focus
├── Frameworks: FastAPI, Flask, Django
├── Databases: PostgreSQL, MongoDB, Redis
└── APIs: REST, GraphQL

DevOps
├── Deployment: Docker, Kubernetes
├── Cloud: AWS, GCP, Azure
└── CI/CD: GitHub Actions, GitLab CI
```

---

## HTTP & REST Principles

### HTTP Methods

| Method | Purpose | Safe | Idempotent |
|--------|---------|------|-----------|
| **GET** | Retrieve data | ✅ Yes | ✅ Yes |
| **POST** | Create resource | ❌ No | ❌ No |
| **PUT** | Replace resource | ❌ No | ✅ Yes |
| **PATCH** | Partial update | ❌ No | ❌ No |
| **DELETE** | Remove resource | ❌ No | ✅ Yes |
| **HEAD** | Like GET, no body | ✅ Yes | ✅ Yes |
| **OPTIONS** | Describe options | ✅ Yes | ✅ Yes |

### REST API Design

```
Resource-based URLs (not action-based):

✅ GOOD:
GET /api/users                    # List all users
GET /api/users/123                # Get user 123
POST /api/users                   # Create user
PUT /api/users/123                # Replace user 123
PATCH /api/users/123              # Update user 123
DELETE /api/users/123             # Delete user 123

❌ BAD:
GET /api/getUsers
GET /api/getUserById?id=123
POST /api/createUser
POST /api/updateUser
GET /api/deleteUser?id=123
```

### HTTP Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| **200** | OK | Successful request |
| **201** | Created | Resource created |
| **204** | No Content | Success, no body |
| **400** | Bad Request | Invalid input |
| **401** | Unauthorized | Authentication required |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Request conflicts with state |
| **500** | Server Error | Server error |
| **503** | Service Unavailable | Temporary unavailable |

---

## FastAPI Basics

### Installation & Setup

```bash
pip install fastapi uvicorn
```

### Hello World

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Run: uvicorn main:app --reload
```

### Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# GET /users/123 → {"user_id": 123}

@app.get("/posts/{post_id}/comments/{comment_id}")
def get_comment(post_id: int, comment_id: int):
    return {"post_id": post_id, "comment_id": comment_id}
```

### Query Parameters

```python
@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}

# GET /search?q=python&limit=5

@app.get("/products")
def list_products(skip: int = 0, limit: int = 10, category: str = None):
    return {"skip": skip, "limit": limit, "category": category}
```

### Request Body

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
def create_user(user: User):
    return {"message": f"User {user.name} created"}

# POST /users with JSON body:
# {"name": "Alice", "email": "alice@example.com", "age": 30}
```

### Response Models

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    # Only fields in UserResponse are returned
    return {
        "id": user_id,
        "name": "Alice",
        "email": "alice@example.com",
        "is_active": True,
        "password_hash": "should_not_appear"  # Excluded
    }
```

---

## FastAPI Advanced

### Dependency Injection

```python
from fastapi import Depends, HTTPException

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user from token"""
    if token != "valid_token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": 1, "username": "alice"}

@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}"}

# Reuse dependencies across routes
@app.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return current_user
```

### Middleware

```python
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import time
import logging

logger = logging.getLogger(__name__)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(f"{request.method} {request.url.path} - {duration:.3f}s")
    response.headers["X-Process-Time"] = str(duration)

    return response
```

### Background Tasks

```python
from fastapi import BackgroundTasks
import time

def send_email_background(email: str):
    """Send email in background"""
    time.sleep(5)  # Simulate long operation
    print(f"Email sent to {email}")

@app.post("/send-email")
async def send_email(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_background, email)
    return {"message": "Email sending in background"}
```

### WebSockets

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except:
        pass
    finally:
        await websocket.close()
```

---

## Request & Response Handling

### File Upload

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    # Save file
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename, "size": len(contents)}

# Upload multiple files
@app.post("/upload-multiple")
async def upload_files(files: List[UploadFile] = File(...)):
    return [{"filename": f.filename} for f in files]
```

### File Download

```python
from fastapi.responses import FileResponse

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    return FileResponse(
        path=f"uploads/{file_name}",
        filename=file_name
    )
```

### Custom Response

```python
from fastapi.responses import JSONResponse, HTMLResponse

@app.get("/json")
async def get_json():
    return JSONResponse({"key": "value"})

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return """
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """
```

### Headers

```python
from fastapi import Header

@app.get("/headers")
async def read_headers(x_token: str = Header(...)):
    return {"x_token": x_token}

# Response headers
@app.get("/custom-headers")
async def custom_headers():
    return {
        "message": "Hello",
        "X-Custom-Header": "CustomValue"
    }
```

---

## Authentication & JWT

### JWT Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)
    return username

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verify username/password
    if form_data.username != "alice" or form_data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
```

---

## Database Integration

### SQLAlchemy with FastAPI

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://user:pass@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

# API endpoint
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

---

## Error Handling

### Custom Exceptions

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id < 1:
        raise HTTPException(
            status_code=400,
            detail="user_id must be positive"
        )
    # Get user...
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user
```

### Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Custom error: {exc.name}"}
    )

@app.get("/test")
async def test_error():
    raise CustomException(name="test_error")
```

---

## Testing APIs

### pytest with FastAPI

```python
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_user(client):
    response = client.post("/users", json={
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"

def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200

def test_get_nonexistent_user(client):
    response = client.get("/users/999")
    assert response.status_code == 404
```

---

## Flask Basics

### Hello World

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify({"user_id": user_id})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    return jsonify({"message": f"User {data['name']} created"}), 201

if __name__ == "__main__":
    app.run(debug=True)
```

### Flask vs FastAPI

| Feature | Flask | FastAPI |
|---------|-------|---------|
| **Speed** | Moderate | Very fast |
| **Async** | Limited | Native |
| **Validation** | Manual | Auto (Pydantic) |
| **Docs** | Manual | Auto (OpenAPI) |
| **Learning** | Easier | Steeper |
| **Maturity** | Very mature | Modern |

---

## WebSockets & Real-time

### Chat Application Example

```python
from fastapi import WebSocket
from typing import List
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User {user_id}: {data}")
    except:
        manager.disconnect(websocket)
```

---

## API Documentation

### Auto-Generated Documentation

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A simple API",
    version="1.0.0"
)

# Swagger UI: /docs
# ReDoc: /redoc
```

### Custom Documentation

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

    class Config:
        example = {
            "name": "Product",
            "description": "A product",
            "price": 9.99,
            "tax": 0.99
        }

@app.post("/items")
def create_item(item: Item):
    """
    Create a new item.

    - **name**: Item name
    - **price**: Item price
    """
    return item
```

---

## Performance & Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n: int):
    # Expensive computation
    return sum(range(n))

@app.get("/calculate/{n}")
def calculate(n: int):
    return {"result": expensive_function(n)}
```

### Database Query Optimization

```python
# ❌ N+1 problem
users = db.query(User).all()
for user in users:
    posts = db.query(Post).filter(Post.user_id == user.id).all()

# ✅ Use join
users = db.query(User).options(joinedload(User.posts)).all()
```

### Pagination

```python
@app.get("/users")
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    total = db.query(User).count()
    return {
        "items": users,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

---

## Real-World Examples

### Todo API

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class Todo(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/todos", response_model=List[Todo])
def list_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404)
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404)
    db.delete(db_todo)
    db.commit()
    return {"deleted": True}
```

---

## Best Practices

### Project Structure

```
api-project/
├── main.py                 # App entry point
├── requirements.txt
├── config.py              # Configuration
├── database.py            # Database setup
├── routers/               # API routes
│   ├── users.py
│   ├── posts.py
│   └── comments.py
├── models/                # SQLAlchemy models
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── schemas/               # Pydantic schemas
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── dependencies.py        # Common dependencies
└── tests/                 # Tests
    ├── test_users.py
    └── test_posts.py
```

### Code Quality

✅ Use type hints
✅ Document APIs
✅ Write tests
✅ Use dependency injection
✅ Handle errors properly
✅ Validate inputs
✅ Log appropriately

---

**Last Updated:** May 2026 | **Version:** 1.0

Related resources:
- [Cloud & DevOps Guide](cloud-devops-guide.md) - Deployment and scaling
- [Database Operations Guide](database-operations-guide.md) - Database integration
- [Security Best Practices](security-best-practices.md) - API security

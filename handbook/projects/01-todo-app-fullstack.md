# 01 - Full-Stack Todo App

## Project Overview

Build a production-ready Todo application with a modern web framework, database, authentication, and deployment. This capstone integrates web development, databases, testing, and DevOps.

**Duration:** 3-4 weeks
**Difficulty:** Intermediate
**Best For:** Software Engineers
**Key Technologies:** FastAPI, PostgreSQL, Docker, React (optional), GitHub Actions, AWS

---

## Learning Objectives

By completing this project, you'll learn:
- Build REST APIs with FastAPI and Pydantic
- Design relational database schemas
- Implement JWT authentication
- Write comprehensive tests with pytest
- Containerize applications with Docker
- Deploy to cloud (AWS or similar)
- Set up CI/CD pipelines
- Monitor production applications

---

## Project Requirements

### Functional Requirements

**User Management:**
- User registration with email validation
- User login with JWT tokens
- Password hashing with bcrypt
- User profile management

**Todo Management:**
- Create, read, update, delete (CRUD) todos
- Mark todos as complete/incomplete
- Filter todos by status
- Assign due dates
- Add descriptions

**Sharing (Optional):**
- Share todos with other users
- Set permissions (view-only, edit, delete)

### Non-Functional Requirements

- API responses in < 200ms
- 95% test coverage
- Database normalized (3NF)
- Secure password handling
- CORS enabled for frontend
- Rate limiting on endpoints
- Comprehensive error handling
- API documentation (Swagger)

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│         Frontend (React/Vue/Plain JS)        │
├─────────────────────────────────────────────┤
│              FastAPI REST API                 │
│  (Authentication, Validation, Business Logic) │
├─────────────────────────────────────────────┤
│         PostgreSQL Database                   │
│  (Users, Todos, Audit Logs)                  │
├─────────────────────────────────────────────┤
│  Redis Cache (Optional - for sessions)       │
└─────────────────────────────────────────────┘

Deployment:
├─ Docker containers (API, DB)
├─ Docker Compose (local development)
├─ GitHub Actions (CI/CD)
└─ AWS EC2 or ECS (production)
```

---

## Week-by-Week Implementation

### Week 1: Backend Setup & Authentication

**Goals:**
- FastAPI project structure
- JWT authentication
- User model and registration
- Database setup with SQLAlchemy

**Deliverables:**
- User registration endpoint (POST /auth/register)
- User login endpoint (POST /auth/login)
- Protected endpoint example (GET /users/me)
- Integration tests for auth

**Key Code Snippets:**

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Todo API")
security = HTTPBearer()

# Database setup
DATABASE_URL = "postgresql://user:password@db:5432/todos"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# User model
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# Authentication logic
from datetime import timedelta
import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(user_id: int) -> str:
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Endpoints
@app.post("/auth/register", response_model=UserResponse)
def register(user: UserRegister, db = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login")
def login(email: str, password: str, db = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
```

**Tests:**
```python
# test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app, engine, Base

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

---

### Week 2: Todo CRUD & Database Relationships

**Goals:**
- Todo model with relationships
- CRUD endpoints
- Filtering and pagination
- Input validation

**Deliverables:**
- POST /todos (create)
- GET /todos (list with filters)
- GET /todos/{id} (get one)
- PATCH /todos/{id} (update)
- DELETE /todos/{id} (delete)
- Full test coverage

**Key Code:**

```python
# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="todos")

# schemas.py
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# endpoints.py
def get_current_user(token: HTTPAuthCredentials = Depends(security), db = Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, user = Depends(get_current_user), db = Depends(get_db)):
    db_todo = Todo(**todo.dict(), user_id=user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=List[TodoResponse])
def list_todos(
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    query = db.query(Todo).filter(Todo.user_id == user.id)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    return query.offset(skip).limit(limit).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, user = Depends(get_current_user), db = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    user = Depends(get_current_user),
    db = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, user = Depends(get_current_user), db = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "Todo deleted"}
```

---

### Week 3: Testing, Security & Documentation

**Goals:**
- Comprehensive test coverage (80%+)
- Security hardening
- API documentation
- Rate limiting

**Deliverables:**
- 50+ unit and integration tests
- Security audit completed
- Swagger documentation
- Rate limiting middleware

**Testing Strategy:**

```python
# test_todos.py
class TestTodoCRUD:
    def test_create_todo(self, authenticated_client):
        response = authenticated_client.post("/todos", json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Buy groceries"

    def test_list_todos_pagination(self, authenticated_client):
        # Create 15 todos
        for i in range(15):
            authenticated_client.post("/todos", json={"title": f"Todo {i}"})

        # Test pagination
        response = authenticated_client.get("/todos?skip=0&limit=10")
        assert len(response.json()) == 10

        response = authenticated_client.get("/todos?skip=10&limit=10")
        assert len(response.json()) == 5

    def test_filter_completed(self, authenticated_client):
        # Create and complete some todos
        response = authenticated_client.post("/todos", json={"title": "Test"})
        todo_id = response.json()["id"]
        authenticated_client.patch(f"/todos/{todo_id}", json={"completed": True})

        # Filter completed
        response = authenticated_client.get("/todos?completed=true")
        assert all(t["completed"] for t in response.json())
```

**Security Additions:**

```python
# security.py
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/login")
@limiter.limit("5/minute")
def login(...):
    # Rate limited to 5 attempts per minute
    pass

# Input validation with Pydantic already handles SQL injection
# Password hashing prevents plaintext storage
# JWT tokens instead of sessions
# CORS restricts cross-origin requests
```

---

### Week 4: Containerization & Deployment

**Goals:**
- Docker containerization
- Docker Compose for local dev
- GitHub Actions CI/CD
- AWS deployment

**Deliverables:**
- Dockerfile for API
- docker-compose.yml
- GitHub Actions workflow
- Deployed on AWS

**Dockerfile:**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/todos
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: todos
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

**GitHub Actions Workflow:**

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: pytest --cov=./ --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v2

    - name: Deploy to AWS
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      run: |
        # Deploy script here
        aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

---

## Project Completion Checklist

### Core Features
- [ ] User registration and login
- [ ] JWT authentication
- [ ] Todo CRUD operations
- [ ] Input validation
- [ ] Error handling

### Testing
- [ ] Unit tests for models
- [ ] Integration tests for endpoints
- [ ] Authentication tests
- [ ] Edge case tests
- [ ] 80%+ code coverage

### Security
- [ ] Passwords hashed with bcrypt
- [ ] SQL injection prevention
- [ ] CORS configured
- [ ] Rate limiting
- [ ] Input validation

### Documentation
- [ ] Swagger/OpenAPI docs
- [ ] README with setup instructions
- [ ] Code comments and docstrings
- [ ] Architecture documentation

### Deployment
- [ ] Dockerfile created
- [ ] docker-compose.yml working
- [ ] GitHub Actions workflow passing
- [ ] Application deployed to cloud

### Interview Readiness
- [ ] Can explain database schema
- [ ] Can discuss authentication approach
- [ ] Can explain testing strategy
- [ ] Can discuss deployment architecture

---

## Interview Questions

1. **How would you scale this application to handle 1 million users?**
   - Database indexing on user_id and created_at
   - Cache frequently accessed todos in Redis
   - Load balancing with multiple API instances
   - Database replication and read replicas

2. **How do you handle concurrent updates to the same todo?**
   - Optimistic locking with version numbers
   - Last-write-wins strategy
   - Conflict resolution in frontend
   - Audit trail for changes

3. **What security vulnerabilities did you address?**
   - SQL injection (SQLAlchemy parameterized queries)
   - Password storage (bcrypt hashing)
   - XSS (JSON responses, not HTML)
   - CSRF (JWT instead of cookies)
   - Authentication (JWT tokens)

4. **How would you add real-time updates?**
   - WebSocket endpoint for live updates
   - Publish/Subscribe with Redis
   - Server-Sent Events (SSE) alternative
   - Client polling as fallback

5. **How do you monitor the production application?**
   - CloudWatch for logs and metrics
   - Prometheus for application metrics
   - Alerts for error rates and latency
   - Health check endpoints
   - Database query monitoring

---

## Resources

- [Web Development Guide](../web-development-guide.md) - FastAPI deep dive
- [Database Operations Guide](../database-operations-guide.md) - SQLAlchemy and schema design
- [Security Best Practices](../security-best-practices.md) - Authentication and validation
- [Cloud & DevOps Guide](../cloud-devops-guide.md) - Docker and AWS deployment

---

## Time Estimate

- **Week 1:** 12-15 hours (Setup, auth, database)
- **Week 2:** 15-18 hours (CRUD, relationships, filtering)
- **Week 3:** 12-15 hours (Tests, security, documentation)
- **Week 4:** 10-12 hours (Docker, CI/CD, deployment)

**Total: 50-60 hours** (Can be parallelized over 4 weeks at 12-15 hours/week)

---

## Next Steps

After completing this project:
1. Add email notifications (Celery + SendGrid)
2. Implement sharing features (permissions model)
3. Add collaborative editing (WebSockets)
4. Build a React/Vue frontend
5. Add analytics dashboard
6. Implement soft deletes and archiving
7. Add task templates and recurring todos

**This project is portfolio-ready!** Showcase it on GitHub with clear documentation.

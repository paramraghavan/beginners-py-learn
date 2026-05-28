# 🗄️ Database Operations Guide

> **From SQL to Production Databases**
>
> Complete guide to working with databases in Python: SQL fundamentals, SQLAlchemy ORM, connection management, and real-world patterns.

---

## Table of Contents

1. [Database Fundamentals](#database-fundamentals)
2. [SQL Basics](#sql-basics)
3. [SQLAlchemy Core & ORM](#sqlalchemy-core--orm)
4. [Models & Relationships](#models--relationships)
5. [Querying Data](#querying-data)
6. [Transactions & ACID](#transactions--acid)
7. [Connection Management](#connection-management)
8. [Database Migrations with Alembic](#database-migrations-with-alembic)
9. [Raw SQL vs ORM](#raw-sql-vs-orm)
10. [Real-World Patterns](#real-world-patterns)
11. [Common Pitfalls](#common-pitfalls)
12. [PostgreSQL Specifics](#postgresql-specifics)
13. [MongoDB with PyMongo](#mongodb-with-pymongo)
14. [Redis for Caching](#redis-for-caching)

---

## Database Fundamentals

### Relational vs NoSQL

| Aspect | Relational (SQL) | NoSQL (Document) |
|--------|------------------|------------------|
| **Structure** | Fixed schema, tables | Flexible, JSON-like |
| **Examples** | PostgreSQL, MySQL | MongoDB, CouchDB |
| **Best for** | Structured data, ACID | Flexible, scalable |
| **Query** | SQL | Query language varies |
| **Transactions** | ACID guarantees | Limited/eventual consistency |
| **Scaling** | Vertical | Horizontal |

### ACID Properties

- **Atomicity** - Transaction completes fully or not at all
- **Consistency** - Data remains valid before & after
- **Isolation** - Transactions don't interfere
- **Durability** - Committed data persists

### Key-Value Store (Redis)
- **In-memory** database for caching
- **Fast** access (microseconds)
- **Data types**: strings, lists, sets, hashes, sorted sets
- **Best for**: sessions, caching, real-time analytics

---

## SQL Basics

### Database & Table Creation

```python
# Using raw SQL
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER CHECK (age >= 0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
```

### CRUD Operations

```python
# Create (Insert)
cursor.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Alice", "alice@example.com", 30)
)

# Read (Select)
cursor.execute("SELECT * FROM users WHERE age > ?", (25,))
rows = cursor.fetchall()

# Update
cursor.execute(
    "UPDATE users SET age = ? WHERE email = ?",
    (31, "alice@example.com")
)

# Delete
cursor.execute("DELETE FROM users WHERE id = ?", (1,))

conn.commit()
```

---

## SQLAlchemy Core & ORM

### Installation

```bash
pip install sqlalchemy psycopg2-binary  # PostgreSQL
pip install sqlalchemy pymysql          # MySQL
pip install sqlalchemy pyodbc           # SQL Server
```

### Connection Strings

```python
# SQLite
sqlite:///database.db

# PostgreSQL
postgresql://user:password@localhost:5432/dbname

# MySQL
mysql+pymysql://user:password@localhost:3306/dbname

# SQL Server
mssql+pyodbc://user:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server
```

### Create Engine

```python
from sqlalchemy import create_engine

# Basic engine
engine = create_engine('postgresql://user:password@localhost/dbname')

# With connection pooling
from sqlalchemy.pool import QueuePool
engine = create_engine(
    'postgresql://user:password@localhost/dbname',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)

# Echo SQL (for debugging)
engine = create_engine('...', echo=True)
```

### Session Management

```python
from sqlalchemy.orm import sessionmaker, Session

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use session
session = SessionLocal()
try:
    # database operations
    pass
finally:
    session.close()

# Better: use context manager
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage
with get_db() as db:
    # database operations
    pass
```

---

## Models & Relationships

### Define Base Model

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
```

### Create Tables

```python
# Create all tables
Base.metadata.create_all(bind=engine)

# Drop all tables
Base.metadata.drop_all(bind=engine)
```

### One-to-Many Relationship

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Relationship
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relationship
    author = relationship("Author", back_populates="books")
```

### Many-to-Many Relationship

```python
from sqlalchemy import Table

# Association table
user_role_association = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    roles = relationship("Role", secondary=user_role_association)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
```

### Self-Referential Relationship

```python
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Self-referential relationship
    parent = relationship("Category", remote_side=[id], backref="children")
```

---

## Querying Data

### Basic Queries

```python
from sqlalchemy.orm import Session

session = SessionLocal()

# Get all records
users = session.query(User).all()

# Get one record
user = session.query(User).first()
user = session.query(User).filter_by(id=1).first()
user = session.query(User).filter(User.id == 1).first()

# Get by primary key
user = session.query(User).get(1)

# Count
count = session.query(User).count()

# Check existence
exists = session.query(User).filter(User.id == 1).first() is not None
# Better way:
exists = session.query(User).filter(User.id == 1).scalar() is not None
```

### Filtering

```python
# Single condition
users = session.query(User).filter(User.age > 25).all()

# Multiple conditions (AND)
users = session.query(User).filter(
    User.age > 25,
    User.is_active == True
).all()

# OR conditions
from sqlalchemy import or_
users = session.query(User).filter(
    or_(User.age > 25, User.is_active == False)
).all()

# IN operator
users = session.query(User).filter(User.id.in_([1, 2, 3])).all()

# LIKE (string matching)
users = session.query(User).filter(User.name.like('%Alice%')).all()

# BETWEEN
users = session.query(User).filter(User.age.between(25, 35)).all()

# NOT NULL
users = session.query(User).filter(User.email != None).all()
```

### Ordering & Limiting

```python
# Order by
users = session.query(User).order_by(User.age).all()  # ascending
users = session.query(User).order_by(User.age.desc()).all()  # descending

# Multiple order by
users = session.query(User).order_by(
    User.age.desc(),
    User.name.asc()
).all()

# Limit & Offset (pagination)
page = 1
per_page = 10
offset = (page - 1) * per_page

users = session.query(User).limit(per_page).offset(offset).all()
```

### Aggregation

```python
from sqlalchemy import func

# Count
count = session.query(func.count(User.id)).scalar()

# Average
avg_age = session.query(func.avg(User.age)).scalar()

# Sum
total = session.query(func.sum(Order.amount)).scalar()

# Min/Max
min_age = session.query(func.min(User.age)).scalar()
max_age = session.query(func.max(User.age)).scalar()

# Group by
from sqlalchemy import group_by
results = session.query(
    User.city,
    func.count(User.id).label('count')
).group_by(User.city).all()
```

### Relationships & Joins

```python
# Accessing related data (lazy loading)
author = session.query(Author).filter_by(id=1).first()
books = author.books  # triggers database query

# Join
books = session.query(Book).join(Author).filter(
    Author.name == "George Orwell"
).all()

# Left join (include authors with no books)
results = session.query(Author).outerjoin(Book).all()

# Multiple joins
results = session.query(Book).join(Author).join(Publisher).filter(
    Publisher.name == "Penguin"
).all()

# Eager loading (prevent N+1 queries)
from sqlalchemy.orm import joinedload
authors = session.query(Author).options(
    joinedload(Author.books)
).all()
```

---

## Transactions & ACID

### Basic Transaction

```python
try:
    session.add(new_user)
    session.commit()
except Exception as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()
```

### Savepoints

```python
try:
    # Do something
    session.add(user1)
    session.flush()

    # Create savepoint
    savepoint = session.begin_nested()

    try:
        session.add(user2)
        session.commit()
    except:
        savepoint.rollback()
        session.add(user3)
        session.commit()

except:
    session.rollback()
finally:
    session.close()
```

### Isolation Levels

```python
from sqlalchemy import event, pool

# Set isolation level
@event.listens_for(pool.Pool, "connect")
def set_isolation_level(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    # PostgreSQL
    cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
    cursor.close()
```

### Bulk Operations

```python
# Bulk insert (faster than adding individually)
users = [
    User(username=f"user{i}", email=f"user{i}@example.com")
    for i in range(1000)
]
session.bulk_insert_mappings(User, users)
session.commit()

# Bulk update
session.query(User).filter(User.is_active == False).update(
    {"is_active": True},
    synchronize_session=False
)
session.commit()

# Bulk delete
session.query(User).filter(User.age < 18).delete()
session.commit()
```

---

## Connection Management

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool, StaticPool

# Default pool (QueuePool)
engine = create_engine(
    'postgresql://...',
    pool_size=10,           # number of connections to keep
    max_overflow=20,        # max additional connections
    pool_recycle=3600,      # recycle connections after 1 hour
    pool_pre_ping=True      # test connection before using
)

# Disable pooling (useful for testing)
engine = create_engine('sqlite:///:memory:', poolclass=StaticPool)

# NullPool (create new connection each time)
engine = create_engine('postgresql://...', poolclass=NullPool)
```

### Connection Events

```python
from sqlalchemy import event

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    # Called when a new connection is created
    print("New connection created")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_conn, connection_record):
    # Called when connection returned to pool
    print("Connection returned to pool")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    # Called when connection taken from pool
    print("Connection taken from pool")
```

### Disposing Connections

```python
# Close all connections in pool
engine.dispose()

# Reconnect after dispose
session = SessionLocal()
```

---

## Database Migrations with Alembic

### Initialize Alembic

```bash
pip install alembic
alembic init alembic
```

### Configure alembic.ini

```ini
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

### Create Migration

```bash
# Auto-generate migration
alembic revision --autogenerate -m "Create users table"

# Manual migration
alembic revision -m "Add email column to users"
```

### Migration File Example

```python
# alembic/versions/xxxxx_create_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
```

### Apply Migrations

```bash
# Apply next migration
alembic upgrade head

# Apply specific migration
alembic upgrade abc123

# Rollback last migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base

# View migration history
alembic history
```

---

## Raw SQL vs ORM

### When to Use ORM

```python
# Good for: business logic, type safety, relationships

# Create user
user = User(username="alice", email="alice@example.com")
session.add(user)
session.commit()

# Update related data
author = session.query(Author).get(1)
author.books.append(Book(title="New Book"))
session.commit()
```

**Advantages:**
- Type safety
- Relationship management
- Query builder is flexible
- Database agnostic
- Prevents SQL injection

**Disadvantages:**
- Slower than raw SQL
- Complex queries are verbose
- N+1 query problems
- Learning curve

### When to Use Raw SQL

```python
# Good for: complex queries, performance-critical, reporting

from sqlalchemy import text

# Raw SQL query
result = session.execute(text("""
    SELECT u.username, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
    HAVING COUNT(o.id) > 10
    ORDER BY order_count DESC
""")).fetchall()
```

**Advantages:**
- Full control over query
- Better performance
- Complex queries easier
- Familiar if coming from SQL

**Disadvantages:**
- SQL injection risk
- Database specific
- Need to handle types manually
- Less maintainable

### Hybrid Approach

```python
# Combine ORM with raw SQL
from sqlalchemy import and_, or_
from sqlalchemy.orm import Query

# Complex ORM query
query = session.query(User).filter(
    and_(
        User.age > 25,
        or_(User.is_active == True, User.premium == True)
    )
).order_by(User.created_at.desc())

# Convert to raw SQL if needed
sql = str(query.statement.compile())
print(sql)
```

---

## Real-World Patterns

### User Authentication

```python
from datetime import datetime, timedelta
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

# Usage
user = User(username="alice", email="alice@example.com")
user.set_password("secure_password")
session.add(user)
session.commit()

# Verify password
if user.verify_password("secure_password"):
    print("Password correct")
```

### Soft Deletes

```python
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    deleted_at = Column(DateTime, nullable=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self):
        """Mark as deleted without removing from database"""
        self.deleted_at = datetime.utcnow()
        session.commit()

    def restore(self):
        """Restore soft-deleted record"""
        self.deleted_at = None
        session.commit()

# Queries automatically exclude deleted records
class UserRepository:
    @staticmethod
    def get_active_users():
        return session.query(User).filter(User.deleted_at == None).all()
```

### Pagination

```python
class Paginator:
    def __init__(self, query, page: int = 1, per_page: int = 10):
        self.query = query
        self.page = max(page, 1)
        self.per_page = per_page
        self.total = query.count()

    @property
    def pages(self) -> int:
        return (self.total + self.per_page - 1) // self.per_page

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    def items(self):
        offset = (self.page - 1) * self.per_page
        return self.query.limit(self.per_page).offset(offset).all()

# Usage
query = session.query(User)
paginator = Paginator(query, page=1, per_page=20)
users = paginator.items()
```

### N+1 Query Problem & Solution

```python
# BAD: N+1 query problem
authors = session.query(Author).all()
for author in authors:
    print(author.books)  # triggers new query for each author

# GOOD: Use eager loading
from sqlalchemy.orm import joinedload, selectinload

# Option 1: joinedload (single query with left join)
authors = session.query(Author).options(
    joinedload(Author.books)
).all()

# Option 2: selectinload (two queries with IN clause)
authors = session.query(Author).options(
    selectinload(Author.books)
).all()

# Option 3: contains_eager
from sqlalchemy.orm import contains_eager
authors = session.query(Author).outerjoin(Book).options(
    contains_eager(Author.books)
).all()
```

### Audit Trail

```python
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    action = Column(String(20))  # CREATE, UPDATE, DELETE
    old_values = Column(String)  # JSON
    new_values = Column(String)  # JSON
    changed_by = Column(String(50))
    changed_at = Column(DateTime, default=datetime.utcnow)

def log_change(session, entity, action, old_values, new_values, user_id):
    """Log database change"""
    import json
    log = AuditLog(
        entity_type=entity.__class__.__name__,
        entity_id=entity.id,
        action=action,
        old_values=json.dumps(old_values),
        new_values=json.dumps(new_values),
        changed_by=user_id
    )
    session.add(log)
    session.commit()
```

---

## Common Pitfalls

### 1. N+1 Query Problem

```python
# ❌ BAD
users = session.query(User).all()
for user in users:
    print(user.profile.bio)  # New query each iteration

# ✅ GOOD
users = session.query(User).options(
    joinedload(User.profile)
).all()
```

### 2. Mutable Default Arguments

```python
# ❌ BAD
def create_user(roles=[]):
    user = User(roles=roles)
    return user

# ✅ GOOD
def create_user(roles=None):
    if roles is None:
        roles = []
    user = User(roles=roles)
    return user
```

### 3. Session Management Issues

```python
# ❌ BAD - Session not closed
session = SessionLocal()
user = session.query(User).get(1)
print(user.created_at)  # Might fail if lazy-loaded outside session

# ✅ GOOD - Use context manager
with get_db() as session:
    user = session.query(User).get(1)
    print(user.created_at)
```

### 4. Expired Objects

```python
# ❌ BAD
user = session.query(User).get(1)
session.commit()  # Expires objects
print(user.username)  # Detached instance warning

# ✅ GOOD
user = session.query(User).get(1)
username = user.username  # Access before commit
session.commit()
```

### 5. Circular Import

```python
# models.py
from sqlalchemy.orm import relationship
from posts import Post

class User(Base):
    posts = relationship("Post", back_populates="author")

# posts.py
from users import User

class Post(Base):
    author = relationship("User", back_populates="posts")

# ✅ GOOD - Use string references
class User(Base):
    posts = relationship("Post", back_populates="author")

class Post(Base):
    author = relationship("User", back_populates="posts")
```

---

## PostgreSQL Specifics

### UUID Type

```python
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50))
```

### Array Type

```python
from sqlalchemy.dialects.postgresql import ARRAY

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tags = Column(ARRAY(String))
    scores = Column(ARRAY(Integer))

# Usage
user = User(tags=["python", "web"])
session.add(user)
session.commit()
```

### JSON Type

```python
from sqlalchemy import JSON

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    metadata = Column(JSON)

# Usage
user = User(metadata={"theme": "dark", "notifications": True})
session.add(user)
session.commit()

# Query JSON
users = session.query(User).filter(
    User.metadata['theme'].astext == 'dark'
).all()
```

### ENUM Type

```python
import enum
from sqlalchemy import Enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
```

### Full-Text Search

```python
from sqlalchemy import func, text

# Raw SQL full-text search
results = session.execute(text("""
    SELECT * FROM posts
    WHERE to_tsvector('english', title || ' ' || content)
    @@ plainto_tsquery('english', :query)
"""), {"query": "python database"}).fetchall()
```

---

## MongoDB with PyMongo

### Installation & Connection

```bash
pip install pymongo
```

```python
from pymongo import MongoClient

# Connect
client = MongoClient('mongodb://localhost:27017/')
db = client['myapp_db']
users = db['users']
```

### CRUD Operations

```python
# Create (Insert)
user_data = {
    'username': 'alice',
    'email': 'alice@example.com',
    'age': 30,
    'roles': ['admin', 'user']
}
result = users.insert_one(user_data)
print(result.inserted_id)

# Insert multiple
users.insert_many([...])

# Read
user = users.find_one({'username': 'alice'})
users_list = list(users.find({'age': {'$gt': 25}}))

# Update
users.update_one(
    {'username': 'alice'},
    {'$set': {'age': 31}}
)

# Delete
users.delete_one({'username': 'alice'})
```

### Indexing

```python
# Create index
users.create_index([('email', 1)])  # 1 for ascending
users.create_index([('email', 1)], unique=True)

# Compound index
users.create_index([('username', 1), ('email', 1)])

# List indexes
users.list_indexes()
```

### Aggregation Pipeline

```python
pipeline = [
    {'$match': {'age': {'$gt': 25}}},
    {'$group': {
        '_id': '$role',
        'count': {'$sum': 1},
        'avg_age': {'$avg': '$age'}
    }},
    {'$sort': {'count': -1}}
]

results = list(users.aggregate(pipeline))
```

---

## Redis for Caching

### Installation

```bash
pip install redis
```

### Basic Operations

```python
import redis

# Connect
r = redis.Redis(host='localhost', port=6379, db=0)

# String operations
r.set('key', 'value')
value = r.get('key')
r.delete('key')

# Expiration
r.setex('session_token', 3600, 'token_value')  # expires in 1 hour

# Increment
r.incr('counter')
r.incrby('counter', 5)

# Decrement
r.decr('counter')
r.decrby('counter', 3)

# Exists
r.exists('key')

# Check type
r.type('key')
```

### Data Structures

```python
import json

# Lists
r.lpush('queue', 'job1', 'job2')      # push to left
r.rpush('queue', 'job3')              # push to right
r.lpop('queue')                        # pop from left
r.lrange('queue', 0, -1)              # get all items

# Sets
r.sadd('tags', 'python', 'database')  # add members
r.smembers('tags')                    # get all
r.scard('tags')                        # count
r.sismember('tags', 'python')         # is member

# Hashes
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@example.com'
})
r.hget('user:1', 'name')
r.hgetall('user:1')

# Sorted sets
r.zadd('leaderboard', {'alice': 100, 'bob': 85})
r.zrange('leaderboard', 0, -1, withscores=True)  # by score ascending
r.zrevrange('leaderboard', 0, -1)                # by score descending
```

### Caching Pattern

```python
def get_user_with_cache(user_id):
    # Try cache first
    cached = r.get(f'user:{user_id}')
    if cached:
        return json.loads(cached)

    # Query database
    user = session.query(User).get(user_id)
    if user:
        # Cache for 1 hour
        r.setex(
            f'user:{user_id}',
            3600,
            json.dumps({
                'id': user.id,
                'username': user.username,
                'email': user.email
            })
        )
        return user

    return None

# Invalidate cache after update
def update_user(user_id, **kwargs):
    user = session.query(User).get(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.commit()

    # Clear cache
    r.delete(f'user:{user_id}')
```

---

## Best Practices

### 1. Use Connection Pooling
```python
engine = create_engine(
    'postgresql://...',
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### 2. Use Alembic for Schema Changes
```bash
alembic upgrade head
```

### 3. Always Use Transactions
```python
try:
    session.add(obj)
    session.commit()
except:
    session.rollback()
finally:
    session.close()
```

### 4. Use Indexes for Frequently Queried Fields
```python
class User(Base):
    __tablename__ = "users"
    email = Column(String(100), index=True, unique=True)
```

### 5. Batch Operations for Performance
```python
session.bulk_insert_mappings(User, users)
```

### 6. Use Eager Loading to Prevent N+1
```python
users = session.query(User).options(joinedload(User.posts)).all()
```

### 7. Monitor Slow Queries
```python
engine = create_engine('...', echo=True)
```

### 8. Use Query Objects for Reusability
```python
class UserRepository:
    @staticmethod
    def get_active_users():
        return session.query(User).filter(User.is_active == True)

    @staticmethod
    def get_by_email(email: str):
        return session.query(User).filter(User.email == email).first()
```

---

## Common Database Designs

### E-commerce Database

```python
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Float)
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
```

### Blog Database

```python
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MongoDB Python Guide](https://pymongo.readthedocs.io/)
- [Redis Python Client](https://redis-py.readthedocs.io/)

---

**Last Updated:** May 2026 | **Version:** 1.0

For more on Python development, see the [Python Handbook](PYTHON_HANDBOOK.md)

# 04 - Real-Time Chat Application

## Project Overview

Build a real-time chat application with WebSockets, message persistence, and user management. This integrates web development, databases, and real-time communication.

**Duration:** 2-3 weeks
**Difficulty:** Intermediate
**Best For:** Software Engineers, Full-Stack Developers
**Key Technologies:** FastAPI, WebSockets, PostgreSQL, Redis, React, Docker

---

## Learning Objectives

By completing this project, you'll learn:
- Implement WebSocket communication
- Build real-time message systems
- Manage connection state
- Design chat data models
- Implement user authentication
- Message persistence
- Redis for caching
- Frontend-backend integration

---

## Project Features

**Core Features:**
- User registration and login
- Create and join chat rooms
- Real-time messaging
- User online/offline status
- Message history
- Typing indicators (optional)
- Private messaging (optional)

**Technical Requirements:**
- < 100ms message latency
- Support 100+ concurrent connections
- Message persistence
- User authentication via JWT
- API rate limiting

---

## System Architecture

```
┌─────────────────────────────┐
│   React Frontend            │
│  (User Interface)           │
└──────────┬──────────────────┘
           │ WebSocket
           │ HTTP REST
           ↓
┌─────────────────────────────┐
│   FastAPI Backend           │
│  • Connection Management    │
│  • Message Routing          │
│  • Business Logic           │
└──────────┬──────────────────┘
           │
     ┌─────┴─────┐
     ↓           ↓
┌─────────┐  ┌──────────┐
│PostgreSQL  │  Redis   │
│Messages    │  Cache   │
│Users       │ Sessions │
│Rooms       │          │
└───────────┘  └────────┘
```

---

## Week-by-Week Implementation

### Week 1: Backend Setup & WebSocket Implementation

**Goals:**
- FastAPI project structure
- User model and authentication
- Chat room model
- WebSocket connection handling

**Deliverables:**
- User registration and login endpoints
- Chat room CRUD endpoints
- WebSocket connection handling
- Message broadcasting

**Key Code:**

```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    rooms = relationship("ChatRoom", secondary="room_members", back_populates="members")
    messages = relationship("Message", back_populates="author")

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_private = Column(Boolean, default=False)

    creator = relationship("User")
    members = relationship("User", secondary="room_members", back_populates="rooms")
    messages = relationship("Message", back_populates="room", cascade="all, delete-orphan")

class RoomMember(Base):
    __tablename__ = "room_members"

    room_id = Column(Integer, ForeignKey("chat_rooms.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("ChatRoom", back_populates="messages")
    author = relationship("User", back_populates="messages")


# websocket_manager.py
from typing import List, Dict
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        # room_id -> list of (websocket, user_id)
        self.active_connections: Dict[int, List[tuple]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        """Accept WebSocket connection"""
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = []

        self.active_connections[room_id].append((websocket, user_id))
        logger.info(f"User {user_id} connected to room {room_id}")

        # Notify others
        await self.broadcast(
            room_id,
            {
                "type": "user_joined",
                "user_id": user_id,
                "user_count": len(self.active_connections[room_id])
            },
            exclude_user=user_id
        )

    def disconnect(self, room_id: int, user_id: int):
        """Remove connection"""
        if room_id in self.active_connections:
            self.active_connections[room_id] = [
                (ws, uid) for ws, uid in self.active_connections[room_id]
                if uid != user_id
            ]
            logger.info(f"User {user_id} disconnected from room {room_id}")

    async def broadcast(self, room_id: int, data: dict, exclude_user: int = None):
        """Broadcast message to all users in room"""
        if room_id not in self.active_connections:
            return

        disconnected = []

        for websocket, user_id in self.active_connections[room_id]:
            if exclude_user and user_id == exclude_user:
                continue

            try:
                await websocket.send_json(data)
            except Exception as e:
                logger.error(f"Error sending to user {user_id}: {e}")
                disconnected.append((websocket, user_id))

        # Clean up disconnected
        for ws, uid in disconnected:
            self.disconnect(room_id, uid)

    async def send_personal(self, websocket: WebSocket, data: dict):
        """Send message to specific user"""
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.error(f"Error in personal message: {e}")

    def get_room_user_count(self, room_id: int) -> int:
        """Get active user count in room"""
        return len(self.active_connections.get(room_id, []))


# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import jwt

app = FastAPI(title="Chat API")
manager = ConnectionManager()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
SECRET_KEY = "your-secret-key"

def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)

# REST Endpoints
@app.post("/rooms")
def create_room(name: str, description: str = None, user_id: int = Depends(get_current_user), db = Depends(get_db)):
    """Create chat room"""
    room = ChatRoom(
        name=name,
        description=description,
        creator_id=user_id
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@app.get("/rooms")
def list_rooms(db = Depends(get_db)):
    """List all public rooms"""
    rooms = db.query(ChatRoom).filter(ChatRoom.is_private == False).all()
    return rooms

@app.post("/rooms/{room_id}/join")
def join_room(room_id: int, user_id: int = Depends(get_current_user), db = Depends(get_db)):
    """Join chat room"""
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404)

    user = db.query(User).filter(User.id == user_id).first()
    if user not in room.members:
        room.members.append(user)
        db.commit()

    return {"status": "joined"}

@app.get("/rooms/{room_id}/messages")
def get_messages(room_id: int, skip: int = 0, limit: int = 50, db = Depends(get_db)):
    """Get message history"""
    messages = db.query(Message).filter(
        Message.room_id == room_id
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()

    return messages

# WebSocket
@app.websocket("/ws/rooms/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    token: str,
    db = Depends(get_db)
):
    """WebSocket connection for real-time messaging"""

    # Verify user
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except jwt.InvalidTokenError:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    # Check room access
    room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if not room:
        await websocket.close(code=4004, reason="Room not found")
        return

    # Connect
    await manager.connect(websocket, room_id, user_id)

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Save to database
            message = Message(
                room_id=room_id,
                author_id=user_id,
                content=message_data.get("content")
            )
            db.add(message)
            db.commit()

            # Broadcast
            await manager.broadcast(
                room_id,
                {
                    "type": "message",
                    "user_id": user_id,
                    "username": db.query(User).get(user_id).username,
                    "content": message_data.get("content"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        await manager.broadcast(
            room_id,
            {
                "type": "user_left",
                "user_id": user_id,
                "user_count": manager.get_room_user_count(room_id)
            }
        )
```

---

### Week 2: Frontend & User Experience

**Goals:**
- React frontend setup
- Chat UI components
- WebSocket client
- User authentication
- Real-time message display

**Deliverables:**
- Chat room list
- Message display
- Message input
- User presence indicators
- Responsive design

**Key Code (React):**

```jsx
// src/hooks/useChat.js
import { useEffect, useState, useCallback } from 'react';

export function useChat(roomId, token) {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState(0);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!roomId || !token) return;

    // Connect to WebSocket
    const websocket = new WebSocket(
      `ws://localhost:8000/ws/rooms/${roomId}?token=${token}`
    );

    websocket.onopen = () => {
      console.log('Connected');
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'message') {
        setMessages(prev => [...prev, {
          id: prev.length,
          username: data.username,
          content: data.content,
          timestamp: data.timestamp
        }]);
      } else if (data.type === 'user_joined') {
        setUsers(data.user_count);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [roomId, token]);

  const sendMessage = useCallback((content) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ content }));
    }
  }, [ws]);

  return { messages, users, sendMessage };
}

// src/components/ChatRoom.jsx
import { useChat } from '../hooks/useChat';
import { useState } from 'react';

export function ChatRoom({ roomId, token, roomName }) {
  const { messages, users, sendMessage } = useChat(roomId, token);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-room">
      <h2>{roomName}</h2>
      <p>Users online: {users}</p>

      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className="message">
            <strong>{msg.username}</strong>
            <p>{msg.content}</p>
            <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type a message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
```

---

### Week 3: Optimization, Testing & Deployment

**Goals:**
- Add Redis caching
- Performance optimization
- Comprehensive testing
- Docker deployment
- CI/CD setup

**Deliverables:**
- Redis integration for session management
- Load testing results
- Test suite (API + WebSocket)
- Docker Compose setup
- GitHub Actions workflow

**Key Code:**

```python
# redis_manager.py
import redis
import json

class RedisManager:
    """Manage Redis for sessions and caching"""

    def __init__(self, host='localhost', port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def set_user_session(self, user_id: int, token: str, expires: int = 86400):
        """Store user session"""
        self.redis.setex(f"session:{user_id}", expires, token)

    def get_user_session(self, user_id: int) -> str:
        """Get user session"""
        return self.redis.get(f"session:{user_id}")

    def set_room_status(self, room_id: int, status: dict):
        """Store room status (user count, etc)"""
        self.redis.setex(f"room:{room_id}", 3600, json.dumps(status))

    def get_active_users(self, room_id: int) -> list:
        """Get active users in room"""
        return self.redis.lrange(f"room:{room_id}:users", 0, -1)


# tests/test_websocket.py
import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_websocket_connection(client):
    """Test WebSocket connection"""
    with client.websocket_connect("/ws/rooms/1?token=valid_token") as websocket:
        # Send message
        websocket.send_json({"content": "Hello"})

        # Receive message
        data = websocket.receive_json()
        assert data["type"] == "message"
        assert data["content"] == "Hello"

def test_websocket_broadcast(client):
    """Test message broadcasting"""
    with client.websocket_connect("/ws/rooms/1?token=token1") as ws1:
        with client.websocket_connect("/ws/rooms/1?token=token2") as ws2:
            # User 1 sends message
            ws1.send_json({"content": "Hello everyone"})

            # User 2 receives
            data = ws2.receive_json()
            assert data["content"] == "Hello everyone"

def test_message_persistence(client, db):
    """Test messages are saved to database"""
    with client.websocket_connect("/ws/rooms/1?token=token") as ws:
        ws.send_json({"content": "Persistent message"})

    # Verify in database
    messages = db.query(Message).filter(Message.content == "Persistent message").all()
    assert len(messages) == 1
```

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
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
      DATABASE_URL: postgresql://user:password@db:5432/chat
      REDIS_URL: redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: chat
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - api

volumes:
  postgres_data:
```

---

## Project Completion Checklist

### Backend
- [ ] User authentication (JWT)
- [ ] Chat room CRUD
- [ ] WebSocket message handling
- [ ] Message persistence
- [ ] User online/offline status
- [ ] API rate limiting

### Frontend
- [ ] Chat room list UI
- [ ] Message display area
- [ ] Message input
- [ ] Real-time updates
- [ ] User presence indicators
- [ ] Responsive design

### Performance
- [ ] < 100ms message latency
- [ ] Support 100+ concurrent connections
- [ ] Redis caching
- [ ] Database query optimization

### Testing
- [ ] Unit tests (API)
- [ ] WebSocket tests
- [ ] Integration tests
- [ ] Load tests (50+ users)
- [ ] 80%+ coverage

### Deployment
- [ ] Dockerfile created
- [ ] docker-compose.yml
- [ ] GitHub Actions workflow
- [ ] Deployed

---

## Interview Questions

1. **How would you scale this to support millions of concurrent users?**
   - Load balancing
   - Multiple WebSocket servers
   - Redis pub/sub for inter-server messaging
   - Database scaling

2. **How do you handle message ordering?**
   - Timestamps with microsecond precision
   - Database sequence numbers
   - Client-side sorting
   - Idempotent message IDs

3. **What happens if WebSocket connection drops?**
   - Client reconnection with backoff
   - Message queue in Redis
   - Undelivered messages stored
   - Sync on reconnect

4. **How do you prevent spam?**
   - Rate limiting per user
   - Redis counters
   - Message validation
   - User moderation tools

5. **How do you ensure message delivery?**
   - Acknowledgment mechanism
   - Message queue
   - Retry logic
   - Delivery status tracking

---

## Time Estimate

- **Week 1:** 15-18 hours (Backend, WebSockets)
- **Week 2:** 15-18 hours (Frontend, UI/UX)
- **Week 3:** 12-15 hours (Testing, optimization, deployment)

**Total: 42-51 hours**

---

## Next Steps

After completing:
1. Add typing indicators
2. Implement private messaging
3. Add message reactions/emojis
4. User profiles
5. Admin moderation tools
6. Message search
7. File/image sharing

**This is a production-ready chat application!** Portfolio-impressive and interview-worthy.

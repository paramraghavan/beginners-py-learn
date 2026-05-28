# 05 - E-Commerce Backend

## Project Overview

Build a complete e-commerce backend with product catalog, shopping cart, orders, payments, and inventory management. This is a comprehensive full-stack project integrating all major concepts.

**Duration:** 4-5 weeks
**Difficulty:** Advanced
**Best For:** Full-Stack/Backend Engineers
**Key Technologies:** FastAPI, PostgreSQL, Stripe, Redis, Celery, AWS, Docker

---

## Learning Objectives

By completing this project, you'll learn:
- Complex database relationships
- Payment processing (Stripe)
- Inventory management
- Order workflow and state machines
- Asynchronous tasks (Celery)
- Email notifications
- Search and filtering
- Analytics and reporting
- Production-grade error handling
- Advanced API design

---

## Project Scope

**Core Features:**
- Product catalog with categories and search
- User authentication and profiles
- Shopping cart management
- Order placement and tracking
- Payment processing (Stripe)
- Inventory management
- Admin dashboard
- Email notifications
- Wishlist functionality

**Business Requirements:**
- Support 10,000+ concurrent users
- Process 1000 orders/day
- < 200ms API response time
- 99.9% uptime
- Secure payment handling (PCI DSS compliant)
- Audit trail for all transactions

---

## System Architecture

```
┌────────────────────────────────────────────────────┐
│            Frontend (React/Vue)                     │
│  (Product Browse, Cart, Checkout, User Profile)   │
└────────────────┬─────────────────────────────────┘
                 │ REST API / WebSocket
┌────────────────────────────────────────────────────┐
│           FastAPI Backend                          │
│  ┌──────────────────────────────────────────────┐ │
│  │ API Layer                                    │ │
│  │  • Product endpoints                         │ │
│  │  • Cart endpoints                            │ │
│  │  • Order endpoints                           │ │
│  │  • Payment endpoints                         │ │
│  │  • User endpoints                            │ │
│  └──────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────┐ │
│  │ Business Logic                               │ │
│  │  • Inventory management                      │ │
│  │  • Order processing                          │ │
│  │  • Payment handling                          │ │
│  │  • User management                           │ │
│  └──────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────┐ │
│  │ Services                                     │ │
│  │  • Stripe payment service                    │ │
│  │  • Email notification service                │ │
│  │  • Search service (Elasticsearch)            │ │
│  └──────────────────────────────────────────────┘ │
└────────────────┬─────────────────────────────────┘
     ┌───────────┼───────────┬────────────────┐
     ↓           ↓           ↓                ↓
┌─────────┐  ┌────────┐  ┌──────┐      ┌──────────┐
│PostgreSQL  │  Redis   │Stripe │      │Celery    │
│           │  Cache   │API    │      │Tasks     │
└─────────┘  └────────┘  └──────┘      └──────────┘
```

---

## Week-by-Week Implementation

### Week 1: Data Models & Core APIs

**Goals:**
- Design comprehensive database schema
- Implement user and product management
- Create shopping cart system
- Build core REST endpoints

**Deliverables:**
- Database schema (users, products, orders, cart items)
- User registration/authentication
- Product CRUD with filtering
- Shopping cart endpoints
- 80%+ test coverage

**Key Code:**

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    wishlist_items = relationship("WishlistItem", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=False)
    country = Column(String(50), nullable=False)
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    slug = Column(String(50), unique=True)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    sku = Column(String(50), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float)  # For profit calculation
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    wishlist_items = relationship("WishlistItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_number = Column(String(20), unique=True, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0)
    shipping = Column(Float, default=0)
    total = Column(Float, nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"))
    payment_status = Column(String(20))  # paid, pending, failed
    stripe_payment_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    shipping_address = relationship("Address")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of purchase
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")


# endpoints.py - Product endpoints
from fastapi import FastAPI, Query, HTTPException
from sqlalchemy.orm import Session

app = FastAPI(title="E-Commerce API")

@app.get("/products")
def list_products(
    skip: int = 0,
    limit: int = 20,
    category: str = None,
    search: str = None,
    sort_by: str = "name",
    db: Session = Depends(get_db)
):
    """List products with filtering and search"""
    query = db.query(Product).filter(Product.is_active == True)

    # Filter by category
    if category:
        query = query.join(Category).filter(Category.slug == category)

    # Search by name or description
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) |
            (Product.description.ilike(search_term))
        )

    # Sort
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())

    return query.offset(skip).limit(limit).all()

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product details"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Cart endpoints
@app.post("/cart/items")
def add_to_cart(
    product_id: int,
    quantity: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)

    db.commit()
    return {"status": "added", "quantity": cart_item.quantity}

@app.get("/cart")
def get_cart(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's cart"""
    items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    total = sum(item.product.price * item.quantity for item in items)

    return {
        "items": items,
        "item_count": len(items),
        "total": total
    }

@app.delete("/cart/items/{item_id}")
def remove_from_cart(item_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Remove item from cart"""
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404)

    db.delete(cart_item)
    db.commit()
    return {"status": "removed"}
```

---

### Week 2: Order Processing & Payment Integration

**Goals:**
- Implement order creation workflow
- Integrate Stripe payment processing
- Handle order status transitions
- Transaction management

**Deliverables:**
- Order checkout endpoint
- Stripe payment integration
- Order confirmation
- Payment error handling
- Webhook handling for payment updates

**Key Code:**

```python
# payment_service.py
import stripe
from typing import Optional

stripe.api_key = "sk_test_..."

class PaymentService:
    """Handle payment processing"""

    @staticmethod
    def create_payment_intent(order_id: int, amount: float, email: str):
        """Create Stripe PaymentIntent"""
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Amount in cents
            currency="usd",
            receipt_email=email,
            metadata={"order_id": order_id}
        )
        return intent

    @staticmethod
    def confirm_payment(payment_intent_id: str) -> bool:
        """Confirm payment was successful"""
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent.status == "succeeded"

    @staticmethod
    def refund_payment(payment_intent_id: str, amount: Optional[int] = None) -> bool:
        """Refund a payment"""
        try:
            stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount  # None = full refund
            )
            return True
        except stripe.error.StripeError as e:
            print(f"Refund failed: {e}")
            return False


# order_service.py
from datetime import datetime, timedelta
import uuid

class OrderService:
    """Handle order operations"""

    @staticmethod
    def create_order(user_id: int, shipping_address_id: int, db: Session) -> Order:
        """Create order from cart"""

        # Get cart items
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Calculate totals
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        tax = subtotal * 0.1  # 10% tax
        shipping = 10.0 if subtotal < 100 else 0  # Free shipping over $100
        total = subtotal + tax + shipping

        # Create order
        order = Order(
            user_id=user_id,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=total,
            shipping_address_id=shipping_address_id,
            status=OrderStatus.PENDING
        )

        # Create order items and reduce stock
        for cart_item in cart_items:
            order_item = OrderItem(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                subtotal=cart_item.product.price * cart_item.quantity
            )
            order.items.append(order_item)

            # Update stock (reserve)
            product = cart_item.product
            product.stock_quantity -= cart_item.quantity

        db.add(order)
        db.commit()
        db.refresh(order)

        # Clear cart
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()

        return order

    @staticmethod
    def process_payment(order_id: int, payment_intent_id: str, db: Session) -> bool:
        """Process payment for order"""

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404)

        # Verify payment
        if not PaymentService.confirm_payment(payment_intent_id):
            # Revert stock
            for item in order.items:
                item.product.stock_quantity += item.quantity
            db.commit()
            return False

        # Update order
        order.stripe_payment_id = payment_intent_id
        order.payment_status = "paid"
        order.status = OrderStatus.CONFIRMED
        db.commit()

        # Send confirmation email (task)
        send_order_confirmation.delay(order_id)

        return True

    @staticmethod
    def cancel_order(order_id: int, db: Session) -> bool:
        """Cancel order"""

        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404)

        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise HTTPException(status_code=400, detail="Cannot cancel shipped order")

        # Restore stock
        for item in order.items:
            item.product.stock_quantity += item.quantity

        # Refund payment
        if order.stripe_payment_id:
            PaymentService.refund_payment(order.stripe_payment_id)

        order.status = OrderStatus.CANCELLED
        db.commit()

        return True


# checkout endpoints
@app.post("/checkout")
def checkout(
    shipping_address_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate checkout"""

    # Create order
    order = OrderService.create_order(user_id, shipping_address_id, db)

    # Create payment intent
    user = db.query(User).get(user_id)
    intent = PaymentService.create_payment_intent(
        order.id,
        order.total,
        user.email
    )

    return {
        "order_id": order.id,
        "client_secret": intent.client_secret,
        "amount": order.total
    }

@app.post("/payment/confirm")
def confirm_payment(
    order_id: int,
    payment_intent_id: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Confirm payment"""

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(status_code=404)

    if OrderService.process_payment(order_id, payment_intent_id, db):
        return {"status": "success", "order_id": order_id}
    else:
        raise HTTPException(status_code=400, detail="Payment failed")

# Stripe webhook
@app.post("/webhooks/stripe")
def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, "whsec_..."
        )
    except stripe.error.SignatureVerificationError:
        return {"error": "Invalid signature"}, 400

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata']['order_id']
        # Mark order as paid
        # ...

    return {"status": "received"}
```

---

### Week 3: Asynchronous Tasks & Notifications

**Goals:**
- Set up Celery for async tasks
- Implement email notifications
- Background job processing
- Task monitoring

**Deliverables:**
- Celery task setup
- Email service integration
- Order confirmation emails
- Admin notification system
- Task monitoring dashboard

**Key Code:**

```python
# celery_app.py
from celery import Celery
from email.mime.text import MIMEText
import smtplib

app = Celery(
    'ecommerce',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@app.task
def send_order_confirmation(order_id: int):
    """Send order confirmation email"""
    db = SessionLocal()
    order = db.query(Order).get(order_id)

    email_body = f"""
    Thank you for your order!

    Order Number: {order.order_number}
    Total: ${order.total}
    Status: {order.status}

    Items:
    {chr(10).join(f'- {item.product.name} x{item.quantity}' for item in order.items)}

    Tracking information will be sent when order ships.
    """

    send_email(
        to=order.user.email,
        subject=f"Order Confirmation #{order.order_number}",
        body=email_body
    )
    db.close()

@app.task
def update_order_status(order_id: int, new_status: str):
    """Update order status and notify user"""
    db = SessionLocal()
    order = db.query(Order).get(order_id)
    order.status = new_status
    db.commit()

    send_email(
        to=order.user.email,
        subject=f"Order {order.order_number} - {new_status.upper()}",
        body=f"Your order is now {new_status}."
    )
    db.close()

@app.task
def process_inventory_restock(product_id: int, quantity: int):
    """Update inventory and notify if low stock"""
    db = SessionLocal()
    product = db.query(Product).get(product_id)
    product.stock_quantity += quantity
    db.commit()

    if product.stock_quantity < 10:
        send_admin_alert(f"Low stock for {product.name}: {product.stock_quantity} remaining")
    db.close()

def send_email(to: str, subject: str, body: str):
    """Send email"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "noreply@ecommerce.com"
    msg['To'] = to

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your-email@gmail.com", "your-password")
        server.send_message(msg)
```

---

### Week 4: Admin Dashboard & Analytics

**Goals:**
- Create admin endpoints
- Build analytics
- Inventory management
- Reporting

**Deliverables:**
- Admin endpoints for order/product management
- Sales analytics and reporting
- Inventory dashboard
- Revenue metrics
- Performance monitoring

**Key Code:**

```python
# admin_endpoints.py
from fastapi import APIRouter, Depends
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

# Admin authorization
def get_admin(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user.is_admin:  # Add is_admin to User model
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user

@router.get("/orders")
def get_orders(
    skip: int = 0,
    limit: int = 50,
    status: str = None,
    admin: User = Depends(get_admin),
    db: Session = Depends(get_db)
):
    """Get all orders"""
    query = db.query(Order)

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    total = db.query(func.count(Order.id)).scalar()

    return {
        "orders": orders,
        "total": total,
        "page": skip // limit + 1
    }

@router.post("/orders/{order_id}/update-status")
def update_order_status(
    order_id: int,
    new_status: str,
    admin: User = Depends(get_admin),
    db: Session = Depends(get_db)
):
    """Update order status"""
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404)

    order.status = new_status
    db.commit()

    # Send notification
    update_order_status.delay(order_id, new_status)

    return {"status": "updated"}

@router.get("/analytics/sales")
def get_sales_analytics(
    days: int = 30,
    admin: User = Depends(get_admin),
    db: Session = Depends(get_db)
):
    """Get sales analytics"""
    start_date = datetime.utcnow() - timedelta(days=days)

    # Total revenue
    total_revenue = db.query(func.sum(Order.total)).filter(
        Order.created_at >= start_date,
        Order.status != OrderStatus.CANCELLED
    ).scalar() or 0

    # Order count
    order_count = db.query(func.count(Order.id)).filter(
        Order.created_at >= start_date
    ).scalar()

    # Average order value
    avg_order_value = total_revenue / order_count if order_count > 0 else 0

    # Top products
    top_products = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).join(Order).filter(
        Order.created_at >= start_date
    ).group_by(Product.id).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(10).all()

    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "avg_order_value": avg_order_value,
        "top_products": top_products
    }

@router.get("/inventory")
def get_inventory(
    admin: User = Depends(get_admin),
    db: Session = Depends(get_db)
):
    """Get inventory status"""
    products = db.query(Product).all()

    low_stock = [p for p in products if p.stock_quantity < 10]

    return {
        "total_products": len(products),
        "total_stock_value": sum(p.stock_quantity * p.price for p in products),
        "low_stock_items": low_stock
    }
```

---

### Week 5: Testing, Documentation & Deployment

**Goals:**
- Comprehensive test suite
- API documentation
- Performance optimization
- Deployment to production

**Deliverables:**
- 100+ test cases
- API documentation
- Load testing results
- Docker containerization
- Production deployment

**Key Code:**

```python
# test_checkout.py
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_checkout_flow(client, db):
    """Test complete checkout flow"""
    # 1. Add to cart
    response = client.post(
        "/cart/items",
        json={"product_id": 1, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # 2. Get cart
    response = client.get(
        "/cart",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    cart = response.json()
    assert len(cart["items"]) == 1

    # 3. Initiate checkout
    response = client.post(
        "/checkout",
        json={"shipping_address_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    checkout = response.json()
    assert "client_secret" in checkout

    # 4. Confirm payment
    response = client.post(
        "/payment/confirm",
        json={
            "order_id": checkout["order_id"],
            "payment_intent_id": "pi_test_123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_inventory_reduction(client, db):
    """Test inventory is reduced on order"""
    product = db.query(Product).first()
    original_stock = product.stock_quantity

    # Create order
    # ...

    db.refresh(product)
    assert product.stock_quantity == original_stock - 2

def test_order_cancellation(client, db):
    """Test order can be cancelled"""
    # Create order...

    response = client.post(
        f"/orders/{order_id}/cancel",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Verify stock restored
    # ...
```

---

## Project Completion Checklist

### Core Features
- [ ] Product catalog with search and filtering
- [ ] User registration and profiles
- [ ] Shopping cart management
- [ ] Order placement workflow
- [ ] Payment processing (Stripe)
- [ ] Order tracking and status updates

### Business Logic
- [ ] Inventory management
- [ ] Tax calculation
- [ ] Shipping cost calculation
- [ ] Order cancellation/refunds
- [ ] Wishlist functionality

### Integration
- [ ] Stripe payment integration
- [ ] Email notifications (Celery)
- [ ] Webhook handling
- [ ] Admin dashboard
- [ ] Analytics and reporting

### Quality
- [ ] 80%+ test coverage
- [ ] API documentation
- [ ] Error handling
- [ ] Logging and monitoring
- [ ] Performance optimization

### Deployment
- [ ] Dockerfile and docker-compose
- [ ] GitHub Actions CI/CD
- [ ] Deployed to AWS/production
- [ ] Monitoring and alerting setup

---

## Interview Questions

1. **How would you handle a flash sale with limited inventory?**
   - Optimistic locking to prevent overselling
   - Redis for real-time stock counters
   - Order queue for fairness
   - Inventory reservation with timeout

2. **How do you ensure payment security?**
   - PCI DSS compliance
   - Never store full card numbers
   - Use Stripe for payments
   - HTTPS everywhere
   - Rate limiting on payment endpoints

3. **How would you scale to 100,000 orders/day?**
   - Database sharding
   - Read replicas for queries
   - Caching with Redis
   - Async processing with Celery
   - CDN for static content

4. **How do you handle concurrent order modifications?**
   - Optimistic locking with version numbers
   - Database transactions
   - Idempotent operations
   - Conflict resolution strategy

5. **What would you implement for high availability?**
   - Load balancing
   - Database replication
   - Multiple availability zones
   - Health checks and auto-scaling
   - Graceful degradation

---

## Time Estimate

- **Week 1:** 18-20 hours (Models, core APIs)
- **Week 2:** 18-20 hours (Order processing, payments)
- **Week 3:** 15-18 hours (Async tasks, notifications)
- **Week 4:** 12-15 hours (Admin, analytics)
- **Week 5:** 15-18 hours (Testing, documentation, deployment)

**Total: 78-91 hours**

---

## Next Steps

After completing:
1. Add multi-currency support
2. Implement loyalty/reward points
3. Add inventory pre-orders
4. Build mobile app
5. Add recommendation engine
6. Implement marketplace features (3rd party sellers)
7. Advanced analytics and BI

**This is a production-ready e-commerce platform!** Portfolio-grade project that demonstrates full-stack expertise.

"""
Demo: Visual Python Tracer
==========================

HOW TO RUN:
    1. Terminal 1 - Start the server:
       python visual_tracer.py
    
    2. Open browser: http://localhost:5050
    
    3. Terminal 2 - Run this demo:
       python demo_visual_tracer.py
    
    4. Watch the visualization in your browser!
"""

# ============================================================================
# SINGLE LINE TO ENABLE TRACING
# ============================================================================
from visual_tracer import trace; trace()
# ============================================================================

import time


def fetch_user(user_id: int) -> dict:
    """Simulate fetching a user from database"""
    time.sleep(0.05)  # Simulate DB call
    return {"id": user_id, "name": f"User_{user_id}", "email": f"user{user_id}@example.com"}


def validate_email(email: str) -> bool:
    """Validate email format"""
    time.sleep(0.01)
    return "@" in email and "." in email


def validate_user(user: dict) -> bool:
    """Validate user data"""
    if not user.get("id"):
        return False
    return validate_email(user.get("email", ""))


def fetch_orders(user_id: int) -> list:
    """Simulate fetching orders from database"""
    time.sleep(0.08)  # Simulate slower DB call
    return [
        {"order_id": 1001, "amount": 99.99, "status": "completed"},
        {"order_id": 1002, "amount": 249.50, "status": "pending"},
        {"order_id": 1003, "amount": 75.00, "status": "completed"},
    ]


def filter_completed_orders(orders: list) -> list:
    """Filter only completed orders"""
    return [o for o in orders if o["status"] == "completed"]


def calculate_total(orders: list) -> float:
    """Calculate total order amount"""
    return sum(o["amount"] for o in orders)


def apply_discount(total: float, discount_pct: float = 10) -> float:
    """Apply percentage discount"""
    discount = total * (discount_pct / 100)
    return round(total - discount, 2)


def generate_invoice(user: dict, orders: list, total: float) -> dict:
    """Generate invoice document"""
    time.sleep(0.02)
    return {
        "invoice_id": f"INV-{user['id']}-{int(time.time())}",
        "customer": user["name"],
        "items": len(orders),
        "total": total
    }


def send_notification(user: dict, message: str) -> bool:
    """Simulate sending notification"""
    time.sleep(0.03)
    print(f"   📧 Notification sent to {user['email']}: {message}")
    return True


def process_user(user_id: int) -> dict:
    """Process a single user - main workflow"""
    # Fetch user
    user = fetch_user(user_id)
    
    # Validate
    if not validate_user(user):
        return {"error": "Invalid user", "user_id": user_id}
    
    # Get orders
    orders = fetch_orders(user_id)
    completed = filter_completed_orders(orders)
    
    # Calculate totals
    subtotal = calculate_total(completed)
    final_total = apply_discount(subtotal, discount_pct=15)
    
    # Generate invoice
    invoice = generate_invoice(user, completed, final_total)
    
    # Notify user
    send_notification(user, f"Invoice {invoice['invoice_id']} generated!")
    
    return {
        "user": user["name"],
        "order_count": len(completed),
        "total": final_total,
        "invoice": invoice["invoice_id"]
    }


def process_batch(user_ids: list) -> list:
    """Process multiple users"""
    results = []
    for uid in user_ids:
        print(f"\n👤 Processing user {uid}...")
        result = process_user(uid)
        results.append(result)
    return results


def main():
    """Main entry point"""
    print("\n" + "=" * 50)
    print("🚀 Starting Visual Tracer Demo")
    print("=" * 50)
    print("\n📺 Open http://localhost:5050 to see visualization!\n")
    
    # Process a batch of users
    user_ids = [101, 102, 103]
    results = process_batch(user_ids)
    
    print("\n" + "=" * 50)
    print("📊 Results:")
    print("=" * 50)
    for r in results:
        print(f"   {r}")
    
    return results


if __name__ == "__main__":
    main()

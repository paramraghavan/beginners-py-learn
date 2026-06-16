"""Order Management Module"""

from typing import Dict, List
from enum import Enum


class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Item:
    """Shopping cart item"""

    def __init__(self, item_id: int, name: str, price: float, quantity: int = 1):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def total(self) -> float:
        """Calculate total for this item"""
        return self.price * self.quantity


class Order:
    """Order model"""

    def __init__(self, order_id: int, user_id: int, items: List[Item]):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.status = OrderStatus.PENDING
        self.total_amount = sum(item.total for item in items)
        self.payment_method = None
        self.shipping_address = None

    def add_item(self, item: Item) -> None:
        """Add item to order"""
        # Check if item already exists
        for existing_item in self.items:
            if existing_item.item_id == item.item_id:
                existing_item.quantity += item.quantity
                self.total_amount += item.total
                return

        self.items.append(item)
        self.total_amount += item.total

    def remove_item(self, item_id: int) -> None:
        """Remove item from order"""
        for item in self.items:
            if item.item_id == item_id:
                self.total_amount -= item.total
                self.items.remove(item)
                break

    def apply_discount(self, discount_percent: float) -> None:
        """Apply discount to order

        Args:
            discount_percent: Discount percentage (0-100)

        Raises:
            ValueError: If discount is invalid
        """
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")

        discount_amount = self.total_amount * (discount_percent / 100)
        self.total_amount -= discount_amount


class OrderService:
    """Service for managing orders"""

    def __init__(self):
        self.orders: Dict[int, Order] = {}
        self._next_id = 1

    def create_order(self, user_id: int, items: List[Item]) -> Order:
        """Create new order

        Args:
            user_id: User ID
            items: List of items

        Returns:
            Order object

        Raises:
            ValueError: If items list is empty
        """
        if not items:
            raise ValueError("Order must contain at least one item")

        order = Order(self._next_id, user_id, items)
        self.orders[self._next_id] = order
        self._next_id += 1

        return order

    def get_order(self, order_id: int) -> Order:
        """Get order by ID

        Args:
            order_id: Order ID

        Returns:
            Order object

        Raises:
            ValueError: If order not found
        """
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")
        return self.orders[order_id]

    def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for a user

        Args:
            user_id: User ID

        Returns:
            List of orders
        """
        return [order for order in self.orders.values() if order.user_id == user_id]

    def confirm_order(self, order_id: int, payment_method: str, address: str) -> Order:
        """Confirm order with payment and shipping details

        Args:
            order_id: Order ID
            payment_method: Payment method (credit_card, paypal, etc.)
            address: Shipping address

        Returns:
            Confirmed order

        Raises:
            ValueError: If order not found or invalid details
        """
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")

        if not payment_method:
            raise ValueError("Payment method required")

        if not address:
            raise ValueError("Shipping address required")

        order = self.orders[order_id]

        if order.status != OrderStatus.PENDING:
            raise ValueError("Only pending orders can be confirmed")

        order.payment_method = payment_method
        order.shipping_address = address
        order.status = OrderStatus.CONFIRMED

        return order

    def ship_order(self, order_id: int) -> Order:
        """Ship confirmed order

        Args:
            order_id: Order ID

        Returns:
            Shipped order

        Raises:
            ValueError: If order not found or not confirmed
        """
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")

        order = self.orders[order_id]

        if order.status != OrderStatus.CONFIRMED:
            raise ValueError("Only confirmed orders can be shipped")

        order.status = OrderStatus.SHIPPED
        return order

    def deliver_order(self, order_id: int) -> Order:
        """Deliver order

        Args:
            order_id: Order ID

        Returns:
            Delivered order

        Raises:
            ValueError: If order not found or not shipped
        """
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")

        order = self.orders[order_id]

        if order.status != OrderStatus.SHIPPED:
            raise ValueError("Only shipped orders can be delivered")

        order.status = OrderStatus.DELIVERED
        return order

    def cancel_order(self, order_id: int) -> Order:
        """Cancel order

        Args:
            order_id: Order ID

        Returns:
            Cancelled order

        Raises:
            ValueError: If order not found or cannot be cancelled
        """
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")

        order = self.orders[order_id]

        if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise ValueError(f"Cannot cancel order in {order.status.value} status")

        order.status = OrderStatus.CANCELLED
        return order


# Global instance
order_service = OrderService()

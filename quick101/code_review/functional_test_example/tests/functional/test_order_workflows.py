"""Functional Tests for Order Management Workflows"""

import pytest
from src.order import OrderService, Item, OrderStatus
from src.user import UserService


@pytest.fixture
def order_service():
    """Fresh order service for each test"""
    return OrderService()


@pytest.fixture
def user_service():
    """Fresh user service for each test"""
    return UserService()


@pytest.fixture
def logged_in_user(user_service):
    """Create and login a user"""
    user = user_service.register(
        email="customer@example.com",
        name="John Customer",
        password="SecurePass123"
    )
    return user_service.login("customer@example.com", "SecurePass123")


class TestSimpleCheckoutWorkflow:
    """FUNCTIONAL TEST: User adds item to cart and checks out"""

    def test_complete_checkout_workflow(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. User is logged in
        2. User creates order with items
        3. User confirms order with payment details
        4. Order is ready to ship
        """
        user_id = logged_in_user.user_id

        # Step 1: User adds items to order
        items = [
            Item(item_id=1, name="Laptop", price=999.99, quantity=1),
            Item(item_id=2, name="Mouse", price=29.99, quantity=2)
        ]

        # Step 2: User creates order
        order = order_service.create_order(user_id, items)

        assert order.user_id == user_id
        assert len(order.items) == 2
        assert order.total_amount == 999.99 + (29.99 * 2)
        assert order.status == OrderStatus.PENDING

        # Step 3: User provides payment and shipping details
        confirmed_order = order_service.confirm_order(
            order_id=order.order_id,
            payment_method="credit_card",
            address="123 Main St, City, State 12345"
        )

        assert confirmed_order.status == OrderStatus.CONFIRMED
        assert confirmed_order.payment_method == "credit_card"
        assert confirmed_order.shipping_address == "123 Main St, City, State 12345"

    def test_checkout_fails_without_payment_details(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. User creates order
        2. User tries to confirm without payment details
        3. System rejects order
        """
        items = [Item(item_id=1, name="Product", price=49.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)

        # Try to confirm without payment method
        with pytest.raises(ValueError, match="Payment method required"):
            order_service.confirm_order(
                order_id=order.order_id,
                payment_method="",
                address="123 Main St"
            )

    def test_checkout_fails_without_shipping_address(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. User creates order
        2. User tries to confirm without shipping address
        3. System rejects order
        """
        items = [Item(item_id=1, name="Product", price=49.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)

        # Try to confirm without address
        with pytest.raises(ValueError, match="Shipping address required"):
            order_service.confirm_order(
                order_id=order.order_id,
                payment_method="credit_card",
                address=""
            )


class TestOrderFulfillmentWorkflow:
    """FUNCTIONAL TEST: Complete order fulfillment process"""

    def test_order_lifecycle_from_pending_to_delivered(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is created (PENDING)
        2. Customer confirms order (CONFIRMED)
        3. Order is shipped (SHIPPED)
        4. Order is delivered (DELIVERED)
        """
        user_id = logged_in_user.user_id

        # Step 1: Create order
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(user_id, items)
        assert order.status == OrderStatus.PENDING

        # Step 2: Confirm order
        order = order_service.confirm_order(
            order.order_id,
            payment_method="credit_card",
            address="123 Main St"
        )
        assert order.status == OrderStatus.CONFIRMED

        # Step 3: Ship order
        order = order_service.ship_order(order.order_id)
        assert order.status == OrderStatus.SHIPPED

        # Step 4: Deliver order
        order = order_service.deliver_order(order.order_id)
        assert order.status == OrderStatus.DELIVERED

        # Verify final order state
        final_order = order_service.get_order(order.order_id)
        assert final_order.status == OrderStatus.DELIVERED
        assert final_order.user_id == user_id

    def test_cannot_ship_unconfirmed_order(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is created (PENDING)
        2. Warehouse tries to ship without confirmation
        3. System denies shipment
        """
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)

        # Try to ship without confirming
        with pytest.raises(ValueError, match="Only confirmed orders can be shipped"):
            order_service.ship_order(order.order_id)

    def test_cannot_deliver_unshipped_order(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is created and confirmed
        2. Delivery person tries to deliver without shipping
        3. System denies delivery
        """
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)
        order_service.confirm_order(order.order_id, "credit_card", "123 Main St")

        # Try to deliver without shipping
        with pytest.raises(ValueError, match="Only shipped orders can be delivered"):
            order_service.deliver_order(order.order_id)


class TestOrderCancellationWorkflow:
    """FUNCTIONAL TEST: Order cancellation scenarios"""

    def test_cancel_pending_order(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is created (PENDING)
        2. Customer changes mind
        3. Customer cancels order
        4. Order is cancelled
        """
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)

        # Customer cancels
        cancelled_order = order_service.cancel_order(order.order_id)
        assert cancelled_order.status == OrderStatus.CANCELLED

    def test_cancel_confirmed_order(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is confirmed
        2. Customer wants to cancel
        3. System allows cancellation
        """
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)
        order_service.confirm_order(order.order_id, "credit_card", "123 Main St")

        # Customer cancels confirmed order
        cancelled_order = order_service.cancel_order(order.order_id)
        assert cancelled_order.status == OrderStatus.CANCELLED

    def test_cannot_cancel_shipped_order(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is confirmed and shipped
        2. Customer tries to cancel
        3. System denies cancellation
        """
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)
        order_service.confirm_order(order.order_id, "credit_card", "123 Main St")
        order_service.ship_order(order.order_id)

        # Try to cancel shipped order
        with pytest.raises(ValueError, match="Cannot cancel order"):
            order_service.cancel_order(order.order_id)

    def test_cannot_cancel_delivered_order(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Order is delivered
        2. Customer tries to cancel
        3. System denies cancellation
        """
        items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order = order_service.create_order(logged_in_user.user_id, items)
        order_service.confirm_order(order.order_id, "credit_card", "123 Main St")
        order_service.ship_order(order.order_id)
        order_service.deliver_order(order.order_id)

        # Try to cancel delivered order
        with pytest.raises(ValueError, match="Cannot cancel order"):
            order_service.cancel_order(order.order_id)


class TestMultipleOrdersWorkflow:
    """FUNCTIONAL TEST: Customer with multiple orders"""

    def test_customer_can_place_multiple_orders(self, order_service, logged_in_user):
        """
        WORKFLOW:
        1. Customer places first order
        2. Customer places second order
        3. Both orders are separate
        4. System tracks all orders for customer
        """
        user_id = logged_in_user.user_id

        # First order
        order1_items = [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        order1 = order_service.create_order(user_id, order1_items)

        # Second order
        order2_items = [Item(item_id=2, name="Pen", price=5.99, quantity=3)]
        order2 = order_service.create_order(user_id, order2_items)

        # Verify both orders exist
        assert order1.order_id != order2.order_id
        assert order1.total_amount == 19.99
        assert order2.total_amount == 5.99 * 3

        # Verify both orders belong to user
        user_orders = order_service.get_user_orders(user_id)
        assert len(user_orders) == 2
        assert order1.order_id in [o.order_id for o in user_orders]
        assert order2.order_id in [o.order_id for o in user_orders]

    def test_multiple_customers_can_have_orders(self, order_service, user_service):
        """
        WORKFLOW:
        1. Customer A places order
        2. Customer B places order
        3. Orders are kept separate
        4. Each customer only sees their orders
        """
        # Create two customers
        user_a = user_service.register("alice@example.com", "Alice", "Pass123")
        user_b = user_service.register("bob@example.com", "Bob", "Pass123")

        # Both place orders
        order_a = order_service.create_order(
            user_a.user_id,
            [Item(item_id=1, name="Book", price=19.99, quantity=1)]
        )
        order_b = order_service.create_order(
            user_b.user_id,
            [Item(item_id=2, name="Pen", price=5.99, quantity=1)]
        )

        # Verify orders are separate
        assert order_a.user_id == user_a.user_id
        assert order_b.user_id == user_b.user_id

        # Verify each customer only sees their order
        alice_orders = order_service.get_user_orders(user_a.user_id)
        bob_orders = order_service.get_user_orders(user_b.user_id)

        assert len(alice_orders) == 1
        assert len(bob_orders) == 1
        assert alice_orders[0].order_id == order_a.order_id
        assert bob_orders[0].order_id == order_b.order_id

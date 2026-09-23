# db_tools.py
# Purpose: A FAKE database of orders (just a Python dict for now).
# Later this can be swapped for real SQLite/Postgres without changing
# how the rest of the app calls these functions.

from typing import Optional, TypedDict


class Order(TypedDict):
    order_id: str
    customer_name: str
    status: str          # shipped, processing, delivered, cancelled
    refund_eligible: bool


FAKE_ORDERS_DB: dict[str, Order] = {
    "1234": {
        "order_id": "1234",
        "customer_name": "Ali",
        "status": "shipped",
        "refund_eligible": True,
    },
    "2345": {
        "order_id": "2345",
        "customer_name": "Sara",
        "status": "processing",
        "refund_eligible": True,
    },
    "3456": {
        "order_id": "3456",
        "customer_name": "Ahmed",
        "status": "delivered",
        "refund_eligible": True,
    },
    "4567": {
        "order_id": "4567",
        "customer_name": "Ayesha",
        "status": "delivered",
        "refund_eligible": False,
    },
    "5678": {
        "order_id": "5678",
        "customer_name": "Hamza",
        "status": "cancelled",
        "refund_eligible": False,
    },
    "6789": {
        "order_id": "6789",
        "customer_name": "Fatima",
        "status": "shipped",
        "refund_eligible": False,
    },
    "7890": {
        "order_id": "7890",
        "customer_name": "Usman",
        "status": "processing",
        "refund_eligible": True,
    },
    "8901": {
        "order_id": "8901",
        "customer_name": "Hina",
        "status": "delivered",
        "refund_eligible": False,
    },
    "9012": {
        "order_id": "9012",
        "customer_name": "Bilal",
        "status": "shipped",
        "refund_eligible": True,
    },
    "0123": {
        "order_id": "0123",
        "customer_name": "Zainab",
        "status": "cancelled",
        "refund_eligible": False,
    },
}


def get_order(order_id: str) -> Optional[Order]:
    """Look up an order by ID. Returns None if not found."""
    return FAKE_ORDERS_DB.get(order_id)


def check_refund_eligibility(order_id: str) -> bool:
    """Check if a given order can be refunded."""
    order = get_order(order_id)

    if order is None:
        return False

    return order["refund_eligible"]
from enum import Enum


class OrderStatus(Enum):
    """Статусы заказа"""
    NEW = "new"
    PAID = "paid"
    CANCELLED = "cancelled"
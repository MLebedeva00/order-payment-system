from typing import Dict, Optional
from domain.entities.order import Order
from interfaces.repositories import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory реализация репозитория заказов"""

    def __init__(self):
        self._orders: Dict[str, Order] = {}

    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Получить заказ по ID"""
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        """Сохранить заказ"""
        self._orders[order.id] = order

    def clear(self) -> None:
        """Очистить хранилище (для тестов)"""
        self._orders.clear()
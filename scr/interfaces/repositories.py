from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.order import Order


class OrderRepository(ABC):
    """Интерфейс репозитория заказов"""

    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Получить заказ по ID"""
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        """Сохранить заказ"""
        pass
from abc import ABC, abstractmethod
from domain.value_objects.money import Money


class PaymentGateway(ABC):
    """Интерфейс платежного шлюза"""

    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> bool:
        """Выполнить платеж"""
        pass
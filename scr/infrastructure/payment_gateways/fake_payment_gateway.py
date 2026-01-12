from typing import Dict
from domain.value_objects.money import Money
from interfaces.payment_gateways import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Fake реализация платежного шлюза"""

    def __init__(self, always_succeed: bool = True):
        self.always_succeed = always_succeed
        self.payments: Dict[str, Money] = {}

    def charge(self, order_id: str, amount: Money) -> bool:
        """Выполнить платеж"""
        if self.always_succeed:
            self.payments[order_id] = amount
            return True
        return False

    def get_payment(self, order_id: str) -> Optional[Money]:
        """Получить информацию о платеже"""
        return self.payments.get(order_id)
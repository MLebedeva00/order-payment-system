from dataclasses import dataclass
from domain.value_objects.money import Money


@dataclass
class PaymentResult:
    """Результат оплаты"""
    success: bool
    order_id: str
    amount: Money
    message: str = ""
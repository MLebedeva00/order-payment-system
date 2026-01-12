from decimal import Decimal
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Money:
    """Value Object для представления денежных сумм"""
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))
        if self.amount < Decimal('0'):
            raise ValueError("Сумма не может быть отрицательной")

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Нельзя складывать деньги разных валют")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, multiplier: Decimal) -> 'Money':
        return Money(self.amount * multiplier, self.currency)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from decimal import Decimal

from domain.entities.order_line import OrderLine
from domain.value_objects.money import Money
from domain.enums.order_status import OrderStatus
from domain.exceptions import DomainException


@dataclass
class Order:
    """Агрегат Order - корневая сущность"""
    _id: str = field(default_factory=lambda: str(uuid4()))
    _lines: List[OrderLine] = field(default_factory=list)
    _status: OrderStatus = field(default=OrderStatus.NEW)
    _created_at: datetime = field(default_factory=datetime.now)
    _updated_at: datetime = field(default_factory=datetime.now)

    @property
    def id(self) -> str:
        return self._id

    @property
    def lines(self) -> List[OrderLine]:
        return self._lines.copy()

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def total(self) -> Money:
        """Итоговая сумма заказа"""
        if not self._lines:
            return Money(Decimal('0'))

        total_amount = Money(Decimal('0'), self._lines[0].price.currency)
        for line in self._lines:
            if line.price.currency != total_amount.currency:
                raise ValueError("Все строки заказа должны быть в одной валюте")
            total_amount = total_amount + line.total
        return total_amount

    def add_line(self, product_id: str, quantity: int, price: Money) -> None:
        """Добавить строку в заказ"""
        if self._status == OrderStatus.PAID:
            raise DomainException("Нельзя изменить оплаченный заказ")

        # Проверяем валюту
        if self._lines and price.currency != self._lines[0].price.currency:
            raise ValueError("Все товары должны быть в одной валюте")

        new_line = OrderLine(
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        self._lines.append(new_line)
        self._updated_at = datetime.now()

    def remove_line(self, line_id: str) -> None:
        """Удалить строку из заказа"""
        if self._status == OrderStatus.PAID:
            raise DomainException("Нельзя изменить оплаченный заказ")

        self._lines = [line for line in self._lines if line.id != line_id]
        self._updated_at = datetime.now()

    def pay(self) -> None:
        """Оплатить заказ"""
        if self._status == OrderStatus.PAID:
            raise DomainException("Заказ уже оплачен")

        if not self._lines:
            raise DomainException("Нельзя оплатить пустой заказ")

        self._status = OrderStatus.PAID
        self._updated_at = datetime.now()

    def cancel(self) -> None:
        """Отменить заказ"""
        if self._status == OrderStatus.PAID:
            raise DomainException("Нельзя отменить оплаченный заказ")

        self._status = OrderStatus.CANCELLED
        self._updated_at = datetime.now()
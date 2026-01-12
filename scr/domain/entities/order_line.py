from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from domain.value_objects.money import Money


@dataclass
class OrderLine:
    """Строка заказа - часть агрегата Order"""
    product_id: str
    quantity: int
    price: Money
    _id: Optional[str] = None

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def total(self) -> Money:
        """Общая стоимость строки"""
        return self.price * Decimal(self.quantity)

    def change_quantity(self, new_quantity: int) -> None:
        """Изменить количество товара"""
        if new_quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self.quantity = new_quantity
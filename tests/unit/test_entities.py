import pytest
from decimal import Decimal
from domain.entities.order import Order
from domain.entities.order_line import OrderLine
from domain.value_objects.money import Money
from domain.enums.order_status import OrderStatus
from domain.exceptions import DomainException


class TestMoney:
    """Тесты value object Money"""

    def test_create_money(self):
        money = Money(Decimal("100.50"), "USD")
        assert money.amount == Decimal("100.50")
        assert money.currency == "USD"

    def test_money_addition(self):
        money1 = Money(Decimal("100"), "USD")
        money2 = Money(Decimal("50"), "USD")
        result = money1 + money2
        assert result.amount == Decimal("150")

    def test_money_addition_different_currencies(self):
        money1 = Money(Decimal("100"), "USD")
        money2 = Money(Decimal("50"), "EUR")
        with pytest.raises(ValueError):
            money1 + money2

    def test_money_multiplication(self):
        money = Money(Decimal("100"), "USD")
        result = money * Decimal("2")
        assert result.amount == Decimal("200")


class TestOrder:
    """Тесты агрегата Order"""

    def test_create_order(self):
        order = Order()
        assert order.status == OrderStatus.NEW
        assert len(order.lines) == 0

    def test_add_line_to_order(self):
        order = Order()
        price = Money(Decimal("100"), "USD")
        order.add_line("prod_1", 2, price)

        assert len(order.lines) == 1
        assert order.total.amount == Decimal("200")

    def test_cannot_add_line_to_paid_order(self):
        order = Order()
        price = Money(Decimal("100"), "USD")
        order.add_line("prod_1", 2, price)
        order.pay()

        with pytest.raises(DomainException):
            order.add_line("prod_2", 1, price)

    def test_cannot_pay_empty_order(self):
        order = Order()

        with pytest.raises(DomainException) as exc:
            order.pay()

        assert "Нельзя оплатить пустой заказ" in str(exc.value)

    def test_cannot_pay_already_paid_order(self):
        order = Order()
        price = Money(Decimal("100"), "USD")
        order.add_line("prod_1", 1, price)
        order.pay()

        with pytest.raises(DomainException) as exc:
            order.pay()

        assert "Заказ уже оплачен" in str(exc.value)

    def test_order_total_calculation(self):
        order = Order()
        price1 = Money(Decimal("100"), "USD")
        price2 = Money(Decimal("50"), "USD")

        order.add_line("prod_1", 2, price1)  # 200
        order.add_line("prod_2", 3, price2)  # 150

        assert order.total.amount == Decimal("350")

    def test_lines_immutable_after_payment(self):
        order = Order()
        price = Money(Decimal("100"), "USD")
        order.add_line("prod_1", 2, price)

        line_id = order.lines[0].id
        order.pay()

        # Нельзя удалить строку после оплаты
        with pytest.raises(DomainException):
            order.remove_line(line_id)


class TestOrderLine:
    """Тесты строки заказа"""

    def test_order_line_total(self):
        line = OrderLine(
            product_id="prod_1",
            quantity=3,
            price=Money(Decimal("100"), "USD")
        )
        assert line.total.amount == Decimal("300")

    def test_change_quantity(self):
        line = OrderLine(
            product_id="prod_1",
            quantity=3,
            price=Money(Decimal("100"), "USD")
        )
        line.change_quantity(5)
        assert line.quantity == 5
        assert line.total.amount == Decimal("500")
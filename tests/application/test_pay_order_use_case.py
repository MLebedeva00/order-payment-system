import pytest
from decimal import Decimal
from domain.entities.order import Order
from domain.value_objects.money import Money
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.payment_gateways.fake_payment_gateway import FakePaymentGateway
from application.use_cases.pay_order_use_case import PayOrderUseCase


class TestPayOrderUseCase:
    """Тесты use case оплаты заказа"""

    def setup_method(self):
        self.order_repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway(always_succeed=True)
        self.use_case = PayOrderUseCase(
            order_repository=self.order_repository,
            payment_gateway=self.payment_gateway
        )

    def test_successful_payment(self):
        """Успешная оплата корректного заказа"""
        # Создаем заказ
        order = Order()
        order.add_line("prod_1", 2, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        # Выполняем оплату
        result = self.use_case.execute(order.id)

        # Проверяем результат
        assert result.success is True
        assert result.amount.amount == Decimal("200")
        assert result.message == "Оплата прошла успешно"

        # Проверяем, что заказ сохранен с правильным статусом
        saved_order = self.order_repository.get_by_id(order.id)
        assert saved_order.status.value == "paid"

        # Проверяем, что платеж записан в шлюз
        assert self.payment_gateway.get_payment(order.id).amount == Decimal("200")

    def test_payment_empty_order_fails(self):
        """Ошибка при оплате пустого заказа"""
        # Создаем пустой заказ
        order = Order()
        self.order_repository.save(order)

        # Пытаемся оплатить
        result = self.use_case.execute(order.id)

        # Проверяем, что оплата не прошла
        assert result.success is False
        assert "Нельзя оплатить пустой заказ" in result.message

    def test_double_payment_fails(self):
        """Ошибка при повторной оплате"""
        # Создаем и оплачиваем заказ
        order = Order()
        order.add_line("prod_1", 1, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        # Первая оплата - успешная
        result1 = self.use_case.execute(order.id)
        assert result1.success is True

        # Вторая оплата - должна завершиться ошибкой
        result2 = self.use_case.execute(order.id)
        assert result2.success is False
        assert "Заказ уже оплачен" in result2.message

    def test_cannot_modify_order_after_payment(self):
        """Невозможность изменения заказа после оплаты"""
        # Создаем и оплачиваем заказ
        order = Order()
        order.add_line("prod_1", 1, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        self.use_case.execute(order.id)

        # Пытаемся изменить оплаченный заказ
        saved_order = self.order_repository.get_by_id(order.id)

        with pytest.raises(Exception) as exc:
            saved_order.add_line("prod_2", 1, Money(Decimal("50"), "USD"))

        assert "Нельзя изменить оплаченный заказ" in str(exc.value)

    def test_correct_total_calculation(self):
        """Корректный расчет итоговой суммы"""
        # Создаем заказ с несколькими строками
        order = Order()
        order.add_line("prod_1", 2, Money(Decimal("100"), "USD"))  # 200
        order.add_line("prod_2", 3, Money(Decimal("50"), "USD"))  # 150
        order.add_line("prod_3", 1, Money(Decimal("75"), "USD"))  # 75
        self.order_repository.save(order)

        # Оплачиваем
        result = self.use_case.execute(order.id)

        # Проверяем корректность суммы
        assert result.amount.amount == Decimal("425")  # 200 + 150 + 75
        assert result.success is True

    def test_payment_gateway_failure(self):
        """Ошибка при сбое платежного шлюза"""
        # Создаем шлюз, который всегда возвращает ошибку
        failing_gateway = FakePaymentGateway(always_succeed=False)
        use_case = PayOrderUseCase(
            order_repository=self.order_repository,
            payment_gateway=failing_gateway
        )

        # Создаем заказ
        order = Order()
        order.add_line("prod_1", 1, Money(Decimal("100"), "USD"))
        self.order_repository.save(order)

        # Пытаемся оплатить
        result = use_case.execute(order.id)

        # Проверяем, что оплата не прошла
        assert result.success is False
        assert "Платеж не прошел" in result.message
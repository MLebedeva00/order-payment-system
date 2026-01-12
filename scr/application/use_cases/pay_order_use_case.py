from typing import Optional
from domain.entities.order import Order
from domain.value_objects.money import Money
from interfaces.repositories import OrderRepository
from interfaces.payment_gateways import PaymentGateway
from application.dto.payment_result import PaymentResult
from domain.exceptions import DomainException


class PayOrderUseCase:
    """Use Case для оплаты заказа"""

    def __init__(
            self,
            order_repository: OrderRepository,
            payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, order_id: str) -> PaymentResult:
        """Выполнить оплату заказа"""

        # 1. Загрузить заказ
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return PaymentResult(
                success=False,
                order_id=order_id,
                amount=Money(0),
                message="Заказ не найден"
            )

        try:
            # 2. Выполнить доменную операцию оплаты
            order.pay()

            # 3. Вызвать платежный шлюз
            payment_success = self.payment_gateway.charge(order_id, order.total)

            if not payment_success:
                raise DomainException("Платеж не прошел")

            # 4. Сохранить заказ
            self.order_repository.save(order)

            return PaymentResult(
                success=True,
                order_id=order_id,
                amount=order.total,
                message="Оплата прошла успешно"
            )

        except DomainException as e:
            return PaymentResult(
                success=False,
                order_id=order_id,
                amount=order.total,
                message=str(e)
            )
class DomainException(Exception):
    """Базовое исключение доменного слоя"""
    pass


class PaymentException(DomainException):
    """Исключение при оплате"""
    pass


class OrderValidationException(DomainException):
    """Исключение валидации заказа"""
    pass
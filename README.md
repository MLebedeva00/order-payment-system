# Система оплаты заказа

Лабораторная работа №7: Архитектура, слои и DDD-lite

## Цель проекта
Реализовать систему оплаты заказов, применяя слоистую архитектуру и принципы DDD.

## Архитектура проекта

### Слои:
1. **Domain** - доменная модель и бизнес-правила
   - Агрегат Order (корневая сущность)
   - OrderLine (часть агрегата)
   - Money (value object)
   - OrderStatus (enum)

2. **Application** - use cases
   - PayOrderUseCase

3. **Infrastructure** - реализации интерфейсов
   - InMemoryOrderRepository
   - FakePaymentGateway

4. **Interfaces** - абстракции
   - OrderRepository
   - PaymentGateway

## Бизнес-правила (инварианты)

1. Нельзя оплатить пустой заказ
2. Нельзя оплатить заказ повторно
3. После оплаты нельзя менять строки заказа
4. Итоговая сумма заказа равна сумме строк

## Запуск тестов

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest tests/

# Запуск тестов use case
pytest tests/application/

# Запуск unit-тестов
pytest tests/unit/

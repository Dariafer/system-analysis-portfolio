# Варианты использования / Use Cases

## UC-01 Создание платежа / Create Payment

### Цель / Goal

Создать новый платеж в системе.

Create a new payment in the system.

### Основной актор / Primary Actor

Merchant / Мерчант

### Предусловия / Preconditions

- Мерчант зарегистрирован в системе.
- Merchant is registered in the system.

### Основной сценарий / Main Flow

1. Мерчант отправляет запрос на создание платежа.
2. Система проверяет данные.
3. Система создает платеж.
4. Система возвращает идентификатор платежа.

1. Merchant sends payment creation request.
2. System validates data.
3. System creates payment.
4. System returns payment identifier.

### Результат / Postconditions

Платеж создан со статусом CREATED.

Payment is created with CREATED status.

# Проектирование API / API Design

## Назначение

API платежного шлюза предназначен для взаимодействия мерчанта с системой обработки платежей.

The payment gateway API is designed for interaction between the merchant and the payment processing system.

## Основные endpoints / Main Endpoints

| Метод | Endpoint                               | Назначение                                         |
| ----- | -------------------------------------- | -------------------------------------------------- |
| POST  | `/api/v1/payments`                     | Создание платежа                                   |
| GET   | `/api/v1/payments/{payment_id}`        | Получение информации о платеже                     |
| POST  | `/api/v1/payments/{payment_id}/cancel` | Отмена платежа до обработки                        |
| POST  | `/api/v1/acquiring/callback`           | Получение результата оплаты от mock acquiring bank |
| POST  | `/api/v1/webhooks/test-receiver`       | Тестовый endpoint для приема webhook               |

## Обязательные заголовки / Required Headers

| Header                           | Назначение                                             |
| -------------------------------- | ------------------------------------------------------ |
| `Idempotency-Key`                | Защита от повторного создания одного и того же платежа |
| `Content-Type: application/json` | Формат тела запроса                                    |

## Пример создания платежа / Create Payment Example

```http
POST /api/v1/payments
Content-Type: application/json
Idempotency-Key: order-1001-payment-1
```

```json
{
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "description": "Оплата заказа order-1001"
}
```

## Пример ответа / Response Example

```json
{
  "payment_id": "pay_001",
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "status": "CREATED"
}

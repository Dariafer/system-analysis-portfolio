# Проектирование API / API Design

## Назначение документа / Document Purpose

Документ описывает API платежного шлюза в рамках MVP: создание платежа, получение статуса платежа, отмену платежа до обработки и прием результата оплаты от заглушки банка-эквайера.

The document describes the payment gateway API within the MVP scope: payment creation, payment status retrieval, payment cancellation before processing, and payment result processing from the mock acquiring bank.

## Общие принципы API / API Principles

| Принцип         | Описание                                                                 |
| --------------- | ------------------------------------------------------------------------ |
| REST API        | Взаимодействие выполняется через HTTP endpoints                          |
| JSON            | Формат входных и выходных данных — JSON                                  |
| Idempotency-Key | Создание платежа защищено от повторной обработки                         |
| Статусы платежа | Статус платежа изменяется только по разрешенным переходам                |
| Webhook         | После финального статуса платежа система отправляет уведомление мерчанту |

## Main API Principles

| Principle        | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| REST API         | Interaction is performed through HTTP endpoints                                      |
| JSON             | Request and response payloads use JSON format                                        |
| Idempotency-Key  | Payment creation is protected from duplicate processing                              |
| Payment statuses | Payment status changes only through allowed transitions                              |
| Webhook          | After a final payment status is set, the system sends a notification to the merchant |

## Основные endpoints / Main Endpoints

| Метод | Endpoint                               | Назначение                                         |
| ----- | -------------------------------------- | -------------------------------------------------- |
| POST  | `/api/v1/payments`                     | Создание платежа                                   |
| GET   | `/api/v1/payments/{payment_id}`        | Получение информации о платеже                     |
| POST  | `/api/v1/payments/{payment_id}/cancel` | Отмена платежа до отправки в обработку             |
| POST  | `/api/v1/acquiring/callback`           | Прием результата оплаты от заглушки банка-эквайера |

## Обязательные заголовки / Required Headers

| Header                           | Где используется        | Назначение                                               |
| -------------------------------- | ----------------------- | -------------------------------------------------------- |
| `Content-Type: application/json` | Все POST-запросы        | Указывает JSON-формат тела запроса                       |
| `Idempotency-Key`                | `POST /api/v1/payments` | Защищает от повторного создания одного и того же платежа |
| `X-API-Key`                      | Запросы мерчанта        | Идентифицирует мерчанта в системе                        |

## Создание платежа / Create Payment

### Endpoint

```http
POST /api/v1/payments
```

### Request Headers

```http
Content-Type: application/json
X-API-Key: merchant-api-key
Idempotency-Key: order-1001-payment-1
```

### Request Body

```json
{
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "description": "Оплата заказа order-1001"
}
```

### Success Response

```http
201 Created
```

```json
{
  "payment_id": "b3c4f7a0-7d7a-4e2d-9c21-9d9817d64b10",
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "status": "CREATED"
}
```

### Possible Errors

| Код   | Причина                            |
| ----- | ---------------------------------- |
| `400` | Некорректные параметры запроса     |
| `401` | Не передан или неверен `X-API-Key` |
| `409` | Конфликт ключа идемпотентности     |

## Получение информации о платеже / Get Payment

### Endpoint

```http
GET /api/v1/payments/{payment_id}
```

### Request Headers

```http
X-API-Key: merchant-api-key
```

### Success Response

```http
200 OK
```

```json
{
  "payment_id": "b3c4f7a0-7d7a-4e2d-9c21-9d9817d64b10",
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "status": "SUCCEEDED"
}
```

### Possible Errors

| Код   | Причина                            |
| ----- | ---------------------------------- |
| `401` | Не передан или неверен `X-API-Key` |
| `404` | Платеж не найден                   |

## Отмена платежа / Cancel Payment

### Endpoint

```http
POST /api/v1/payments/{payment_id}/cancel
```

### Request Headers

```http
Content-Type: application/json
X-API-Key: merchant-api-key
```

### Success Response

```http
200 OK
```

```json
{
  "payment_id": "b3c4f7a0-7d7a-4e2d-9c21-9d9817d64b10",
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "status": "CANCELLED"
}
```

### Business Rule

Платеж может быть отменен только до отправки в обработку банку-эквайеру.

The payment can be cancelled only before it is sent to the acquiring bank for processing.

### Possible Errors

| Код   | Причина                                  |
| ----- | ---------------------------------------- |
| `401` | Не передан или неверен `X-API-Key`       |
| `404` | Платеж не найден                         |
| `409` | Платеж нельзя отменить в текущем статусе |

## Callback от банка-эквайера / Acquiring Bank Callback

### Endpoint

```http
POST /api/v1/acquiring/callback
```

### Request Body

```json
{
  "acquiring_request_id": "acq-req-1001",
  "status": "SUCCEEDED",
  "error_code": null,
  "error_message": null
}
```

### Failed Payment Example

```json
{
  "acquiring_request_id": "acq-req-1002",
  "status": "FAILED",
  "error_code": "BANK_DECLINED",
  "error_message": "Payment was declined by acquiring bank"
}
```

### Success Response

```http
200 OK
```

```json
{
  "result": "processed"
}
```

### Business Rule

Callback используется для изменения статуса платежа из `PROCESSING` в финальный статус `SUCCEEDED` или `FAILED`.

Callback is used to change the payment status from `PROCESSING` to the final status `SUCCEEDED` or `FAILED`.

## Исходящий webhook мерчанту / Outgoing Merchant Webhook

Webhook не является входящим endpoint платежного шлюза. Это исходящий HTTP-запрос, который Payment Gateway отправляет на `webhook_url`, указанный в настройках мерчанта.

Webhook is not an incoming payment gateway endpoint. It is an outgoing HTTP request sent by Payment Gateway to the merchant `webhook_url`.

### Webhook URL Example

```http
POST https://merchant.example.com/webhooks/payments
```

### Webhook Payload

```json
{
  "event_id": "evt-1001",
  "event_type": "payment.succeeded",
  "payment_id": "b3c4f7a0-7d7a-4e2d-9c21-9d9817d64b10",
  "merchant_order_id": "order-1001",
  "amount_minor": 150000,
  "currency": "RUB",
  "status": "SUCCEEDED",
  "created_at": "2026-06-20T12:00:00Z"
}
```

### Webhook Events

| Событие             | Когда отправляется                     |
| ------------------- | -------------------------------------- |
| `payment.succeeded` | Платеж успешно завершен                |
| `payment.failed`    | Платеж отклонен или завершился ошибкой |
| `payment.cancelled` | Платеж отменен до обработки            |

## Статусы платежа / Payment Statuses

| Статус       | Описание                               |
| ------------ | -------------------------------------- |
| `CREATED`    | Платеж создан                          |
| `PROCESSING` | Платеж отправлен в обработку           |
| `SUCCEEDED`  | Платеж успешно завершен                |
| `FAILED`     | Платеж отклонен или завершился ошибкой |
| `CANCELLED`  | Платеж отменен до обработки            |

## Связанный файл OpenAPI / Related OpenAPI File

Полная OpenAPI-спецификация находится в файле:

```text
openapi/payment-gateway.yaml
```

The full OpenAPI specification is stored in:

```text
openapi/payment-gateway.yaml

# Backend MVP / Payment Gateway

Backend MVP реализует учебную систему обработки платежей на основе подготовленных аналитических артефактов.

The backend MVP implements a training payment processing system based on the prepared system analysis artifacts.

## Stack

* Python
* FastAPI
* Pydantic
* Pytest
* HTTPX
* Uvicorn

## Implemented Endpoints

| Method | Endpoint                               | Description                               |
| ------ | -------------------------------------- | ----------------------------------------- |
| `GET`  | `/health`                              | Проверка работоспособности API            |
| `POST` | `/api/v1/payments`                     | Создание платежа                          |
| `GET`  | `/api/v1/payments/{payment_id}`        | Получение платежа и его статуса           |
| `POST` | `/api/v1/payments/{payment_id}/cancel` | Отмена платежа                            |
| `POST` | `/api/v1/acquiring/callback`           | Обработка callback от mock acquiring bank |

## Current Implementation

На текущем этапе backend использует in-memory хранилище.

At the current stage, the backend uses in-memory storage.

Это означает, что данные платежей хранятся только во время работы приложения и сбрасываются после перезапуска сервера.

This means that payment data is stored only while the application is running and is reset after server restart.

## Install Dependencies

From the `backend` directory:

```bash
pip install -r requirements.txt
```

## Run Application

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

## Run Tests

From the `backend` directory:

```bash
pytest
```

## Example: Create Payment

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/payments" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -H "Idempotency-Key: idem-example-1" \
  -d '{
    "merchant_order_id": "order_10001",
    "amount_minor": 125000,
    "currency": "RUB",
    "description": "Payment for order order_10001"
  }'
```

## MVP Limitations

* Реальный эквайринг не подключается / Real acquiring is not connected.
* Банковские карты не обрабатываются / Bank cards are not processed.
* PCI DSS не входит в рамки MVP / PCI DSS compliance is out of MVP scope.
* Refund-сценарии не реализованы / Refund scenarios are not implemented.
* Холдирование средств не реализовано / Payment hold is not implemented.
* Антифрод не реализован / Anti-fraud is not implemented.
* PostgreSQL пока не подключен / PostgreSQL is not connected yet.

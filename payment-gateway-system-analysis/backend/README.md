# Backend MVP / Payment Gateway

Backend MVP реализует учебную систему обработки платежей на основе подготовленных аналитических артефактов.

The backend MVP implements a training payment processing system based on the prepared system analysis artifacts.

## Planned Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest
- Docker Compose

## MVP Endpoints

- `POST /api/v1/payments` — создание платежа
- `GET /api/v1/payments/{payment_id}` — получение статуса платежа
- `POST /api/v1/payments/{payment_id}/cancel` — отмена платежа
- `POST /api/v1/acquiring/callback` — обработка callback от заглушки банка-эквайера

## MVP Scope

Backend реализует только учебную бизнес-логику платежного шлюза. Реальный эквайринг, обработка банковских карт, PCI DSS, refunds, hold и antifraud не входят в рамки MVP.

# Границы MVP / MVP Scope
## Назначение проекта
Система обработки платежей предназначена для приема и обработки платежей интернет-магазинов через учебный платежный шлюз.

The payment processing system is designed to receive and process online store payments through an educational payment gateway.

## Входит в MVP / Included in MVP

- Создание платежа / Payment creation
- Получение статуса платежа / Payment status retrieval
- Обработка результата mock acquiring bank / Mock acquiring bank result processing
- Webhook-уведомление мерчанту / Webhook notification to merchant
- Идемпотентность создания платежа / Payment creation idempotency
- Хранение данных в PostgreSQL / Data storage in PostgreSQL

## Не входит в MVP / Out of Scope

- Реальная обработка банковских карт / Real bank card processing
- 3-D Secure
- PCI DSS compliance
- Личный кабинет мерчанта / Merchant personal account
- Возвраты / Refunds
- Холдирование средств / Payment hold
- Мультивалютность / Multi-currency support
- Антифрод / Anti-fraud

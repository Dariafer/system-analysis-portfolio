# Проектирование базы данных / Database Design

## Назначение

База данных хранит информацию о мерчантах, платежах, попытках оплаты, ключах идемпотентности, webhook-событиях и технических логах.

The database stores information about merchants, payments, payment attempts, idempotency keys, webhook events, and technical logs.

## Основные таблицы / Main Tables

| Таблица | Назначение |
|---|---|
| merchants | Хранит данные мерчантов |
| payments | Хранит основные данные платежей |
| payment_attempts | Хранит попытки обработки платежа |
| idempotency_keys | Хранит ключи идемпотентности для защиты от дублей |
| webhook_events | Хранит события webhook для отправки мерчанту |
| transaction_logs | Хранит технический журнал операций |

## Ключевые связи / Key Relationships

| Связь | Описание |
|---|---|
| merchants → payments | Один мерчант может создать много платежей |
| payments → payment_attempts | Один платеж может иметь одну или несколько попыток обработки |
| payments → webhook_events | По одному платежу могут быть созданы webhook-события |
| payments → transaction_logs | По платежу фиксируются технические операции |
| idempotency_keys → payments | Один ключ идемпотентности связан с результатом создания платежа |

## ERD-диаграмма / ERD Diagram

![ERD: Система обработки платежей](../diagrams/payment_gateway_erd.png)

Редактируемый файл draw.io: [payment_gateway_erd.drawio](../diagrams/payment_gateway_erd.drawio)

Диаграмма отражает основные сущности системы обработки платежей: мерчантов, платежи, попытки оплаты, ключи идемпотентности, webhook-события и технические логи.

The diagram describes the main entities of the payment processing system: merchants, payments, payment attempts, idempotency keys, webhook events, and transaction logs.

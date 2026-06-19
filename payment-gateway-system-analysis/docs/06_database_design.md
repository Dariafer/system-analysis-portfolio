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

## Комментарий

Таблица `payments` является центральной сущностью модели данных. Остальные таблицы дополняют ее: фиксируют попытки оплаты, защищают от повторного создания платежей, хранят события webhook и журналируют операции.

The `payments` table is the central entity of the data model. Other tables support it by storing payment attempts, preventing duplicate payment creation, storing webhook events, and logging operations.

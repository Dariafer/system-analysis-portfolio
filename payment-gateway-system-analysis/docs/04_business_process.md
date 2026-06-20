# Бизнес-процесс обработки платежа / Payment Processing Business Process

## Назначение документа / Document Purpose

Документ описывает основной бизнес-процесс создания и обработки платежа в рамках MVP платежного шлюза.

The document describes the main business process for payment creation and processing within the payment gateway MVP.

## Основной процесс / Main Process

1. Покупатель оформляет заказ в интернет-магазине.
2. Мерчант отправляет запрос на создание платежа в Payment Gateway.
3. Payment Gateway принимает запрос и проверяет обязательные параметры.
4. Payment Gateway проверяет ключ идемпотентности.
5. Если запрос некорректен, система возвращает ошибку `400`.
6. Если ключ идемпотентности уже использовался, система возвращает ранее созданный платеж или ошибку `409` при конфликте данных.
7. Если запрос корректен, Payment Gateway создает платеж со статусом `CREATED`.
8. Система сохраняет данные платежа в PostgreSQL.
9. Система создает запись ключа идемпотентности.
10. Система создает попытку оплаты.
11. Payment Gateway переводит платеж в статус `PROCESSING`.
12. Payment Gateway отправляет запрос на оплату в заглушку банка-эквайера.
13. Заглушка банка-эквайера обрабатывает запрос и возвращает результат оплаты.
14. Если оплата успешна, Payment Gateway устанавливает статус платежа `SUCCEEDED`.
15. Если оплата отклонена или завершилась ошибкой, Payment Gateway устанавливает статус платежа `FAILED`.
16. Payment Gateway формирует webhook-событие.
17. Webhook Service отправляет webhook-уведомление мерчанту.
18. Мерчант принимает webhook и обновляет статус заказа.

## Main Process

1. Customer places an order in the online store.
2. Merchant sends a payment creation request to Payment Gateway.
3. Payment Gateway receives the request and validates required parameters.
4. Payment Gateway checks the idempotency key.
5. If the request is invalid, the system returns a `400` error.
6. If the idempotency key has already been used, the system returns the previously created payment or a `409` error in case of a data conflict.
7. If the request is valid, Payment Gateway creates a payment with the `CREATED` status.
8. The system stores payment data in PostgreSQL.
9. The system creates an idempotency key record.
10. The system creates a payment attempt.
11. Payment Gateway changes the payment status to `PROCESSING`.
12. Payment Gateway sends a payment request to the mock acquiring bank.
13. The mock acquiring bank processes the request and returns the payment result.
14. If the payment is successful, Payment Gateway sets the payment status to `SUCCEEDED`.
15. If the payment is declined or fails, Payment Gateway sets the payment status to `FAILED`.
16. Payment Gateway creates a webhook event.
17. Webhook Service sends a webhook notification to the merchant.
18. Merchant receives the webhook and updates the order status.

## Альтернативные сценарии / Alternative Flows

| Сценарий                 | Описание                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------- |
| Некорректный запрос      | Если обязательные параметры отсутствуют или имеют неверный формат, система возвращает ошибку `400`        |
| Повторный запрос         | Если повторный запрос пришел с тем же `Idempotency-Key`, система не создает новый платеж                  |
| Конфликт идемпотентности | Если тот же `Idempotency-Key` используется с другими параметрами платежа, система возвращает ошибку `409` |
| Ошибка банка-эквайера    | Если банк-эквайер возвращает отказ или ошибку, платеж переходит в статус `FAILED`                         |
| Ошибка доставки webhook  | Если мерчант недоступен, webhook-событие сохраняется для последующей повторной отправки                   |

## Alternative Flows

| Flow                   | Description                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------- |
| Invalid request        | If required parameters are missing or have an invalid format, the system returns a `400` error            |
| Repeated request       | If a repeated request is sent with the same `Idempotency-Key`, the system does not create a new payment   |
| Idempotency conflict   | If the same `Idempotency-Key` is used with different payment parameters, the system returns a `409` error |
| Acquiring bank error   | If the acquiring bank returns a decline or error, the payment status changes to `FAILED`                  |
| Webhook delivery error | If the merchant is unavailable, the webhook event is stored for later retry                               |

## Диаграмма процесса / Process Diagram

### Детальная схема обработки платежа / Detailed Payment Processing Flow

![Детальная схема обработки платежа](../diagrams/bpmn_payment_process_detailed.png)

Редактируемый файл draw.io: [bpmn_payment_process_detailed.drawio](../diagrams/bpmn_payment_process_detailed.drawio)

Диаграмма показывает детальный процесс создания и обработки платежа: оформление заказа покупателем, создание платежа мерчантом, проверку запроса и ключа идемпотентности, создание записей в системе, обращение к заглушке банка-эквайера, получение результата оплаты, обновление статуса платежа и отправку webhook-уведомления мерчанту.

The diagram shows the detailed payment creation and processing flow: customer order placement, payment creation by the merchant, request and idempotency key validation, system record creation, interaction with the mock acquiring bank, payment result processing, payment status update, and webhook notification delivery to the merchant.

## Условные обозначения / Notation

Цельные стрелки показывают последовательность операций внутри одного участника процесса.

Пунктирные стрелки показывают обмен сообщениями между участниками системы: API-запросы, ответы, callback и webhook.

Solid arrows show the sequence of operations within one process participant.

Dashed arrows show message exchange between system participants: API requests, responses, callbacks, and webhooks.

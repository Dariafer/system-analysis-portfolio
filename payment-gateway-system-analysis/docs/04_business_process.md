# Бизнес-процесс обработки платежа / Payment Processing Business Process

## Основной процесс / Main Process

1. Покупатель оформляет заказ в интернет-магазине.
2. Мерчант отправляет запрос на создание платежа в Payment Gateway.
3. Payment Gateway проверяет корректность запроса.
4. Payment Gateway создает платеж со статусом CREATED.
5. Payment Gateway переводит платеж в статус PROCESSING.
6. Payment Gateway отправляет запрос в Mock Acquiring Bank.
7. Mock Acquiring Bank возвращает результат оплаты.
8. Payment Gateway обновляет статус платежа на SUCCEEDED или FAILED.
9. Payment Gateway формирует webhook-событие.
10. Payment Gateway отправляет webhook мерчанту.
11. Мерчант обновляет статус заказа.

## Main Process

1. Customer places an order in the online store.
2. Merchant sends a payment creation request to Payment Gateway.
3. Payment Gateway validates the request.
4. Payment Gateway creates a payment with CREATED status.
5. Payment Gateway changes payment status to PROCESSING.
6. Payment Gateway sends a request to Mock Acquiring Bank.
7. Mock Acquiring Bank returns the payment result.
8. Payment Gateway updates payment status to SUCCEEDED or FAILED.
9. Payment Gateway creates a webhook event.
10. Payment Gateway sends the webhook to the merchant.
11. Merchant updates the order status.
## Диаграммы процесса / Process Diagrams

### Обзорная схема обработки платежа

Файл: `diagrams/bpmn_payment_process_overview.drawio`

Диаграмма показывает основной бизнес-процесс: оформление заказа покупателем, создание платежа мерчантом, обработку платежа платежным шлюзом, получение результата от банка-эквайера и отправку webhook-уведомления мерчанту.

### Детальная схема обработки платежа

Файл: `diagrams/bpmn_payment_process_detailed.drawio`

Диаграмма детализирует внутреннюю обработку платежа: проверку запроса, проверку ключа идемпотентности, создание записей в базе данных, создание попытки оплаты, обращение к mock acquiring bank, обновление статуса платежа и отправку webhook-события.

## Условные обозначения

Цельные стрелки показывают последовательность операций внутри одного участника процесса.

Пунктирные стрелки показывают обмен сообщениями между участниками: API-запросы, ответы, callback и webhook.

## Диаграммы процесса / Process Diagrams

### Детальная схема обработки платежа / Detailed Payment Processing Flow

![Детальная схема обработки платежа](../diagrams/bpmn_payment_process_detailed.png)

Редактируемый файл draw.io: [bpmn_payment_process_detailed.drawio](../diagrams/bpmn_payment_process_detailed.drawio)

Диаграмма показывает детальный процесс создания и обработки платежа: оформление заказа покупателем, создание платежа мерчантом, проверку запроса и ключа идемпотентности, создание записей в системе, обращение к заглушке банка-эквайера, получение результата оплаты, обновление статуса платежа и отправку webhook-уведомления мерчанту.

The diagram shows the detailed payment creation and processing flow: customer order placement, payment creation by the merchant, request and idempotency key validation, system record creation, interaction with the mock acquiring bank, payment result processing, payment status update, and webhook notification delivery to the merchant.

### Условные обозначения / Notation

Цельные стрелки показывают последовательность операций внутри одного участника процесса.

Пунктирные стрелки показывают обмен сообщениями между участниками системы: API-запросы, ответы, callback и webhook.

Solid arrows show the sequence of operations within one process participant.

Dashed arrows show message exchange between system participants: API requests, responses, callbacks, and webhooks.


# Диаграмма последовательности / Sequence Diagram

## Назначение документа / Document Purpose

Документ описывает последовательность взаимодействия участников системы при создании и обработке платежа.

The document describes the sequence of interactions between system participants during payment creation and processing.

## Сценарий / Scenario

Диаграмма отражает основной сценарий обработки платежа:

1. Мерчант отправляет запрос на создание платежа.
2. Payment Gateway API принимает запрос и передает его в Payment Service.
3. Payment Service проверяет мерчанта, ключ идемпотентности и создает платеж.
4. Payment Service сохраняет данные в PostgreSQL.
5. Payment Service отправляет запрос на оплату в заглушку банка-эквайера.
6. Заглушка банка-эквайера возвращает результат оплаты через callback.
7. Payment Service обновляет статус платежа.
8. Webhook Service отправляет уведомление в систему мерчанта.

## Участники / Participants

| Участник            | Назначение                                                              |
| ------------------- | ----------------------------------------------------------------------- |
| Merchant            | Инициирует создание платежа                                             |
| Payment Gateway API | Принимает внешние API-запросы                                           |
| Payment Service     | Выполняет бизнес-логику обработки платежа                               |
| PostgreSQL          | Хранит платежи, попытки оплаты, ключи идемпотентности и webhook-события |
| Mock Acquiring Bank | Имитирует обработку платежа банком-эквайером                            |
| Webhook Service     | Отправляет уведомление мерчанту                                         |
| Merchant System     | Принимает webhook и обновляет статус заказа                             |

## Диаграмма / Diagram

![Диаграмма последовательности создания и обработки платежа](../diagrams/sequence_payment_structure.png)

## Основная логика / Main Logic

Диаграмма показывает синхронные и асинхронные взаимодействия между компонентами системы. Создание платежа инициируется мерчантом через API, после чего Payment Service сохраняет платеж и отправляет запрос в заглушку банка-эквайера. Результат оплаты приходит через callback, затем система обновляет статус платежа и формирует webhook-событие для мерчанта.

The diagram shows synchronous and asynchronous interactions between system components. Payment creation is initiated by the merchant through the API. Payment Service stores the payment and sends a request to the mock acquiring bank. The payment result is received through a callback. Then the system updates the payment status and creates a webhook event for the merchant.

## Условные обозначения / Notation

| Тип стрелки            | Значение                                |
| ---------------------- | --------------------------------------- |
| Сплошная стрелка       | Вызов операции или передача запроса     |
| Пунктирная стрелка     | Ответ на запрос или результат обработки |
| Вертикальная линия     | Жизненная линия участника процесса      |
| Прямоугольник на линии | Период выполнения операции              |

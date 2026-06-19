# Жизненный цикл платежа / Payment State Machine

## Назначение

Документ описывает допустимые статусы платежа и правила перехода между ними.

This document describes allowed payment statuses and transition rules.

## Статусы платежа / Payment Statuses

| Статус | Описание |
|---|---|
| CREATED | Платеж создан, но еще не отправлен в банк-эквайер |
| PROCESSING | Платеж отправлен в банк-эквайер и ожидает результата |
| SUCCEEDED | Платеж успешно оплачен |
| FAILED | Платеж отклонен или завершился ошибкой |
| CANCELLED | Платеж отменен до отправки в обработку |

## Разрешенные переходы / Allowed Transitions

| Из статуса | В статус | Условие |
|---|---|---|
| CREATED | PROCESSING | Платеж отправлен в банк-эквайер |
| CREATED | CANCELLED | Мерчант отменил платеж до обработки |
| PROCESSING | SUCCEEDED | Банк-эквайер вернул успешный результат |
| PROCESSING | FAILED | Банк-эквайер вернул ошибку или отказ |

## Запрещенные переходы / Forbidden Transitions

| Переход | Причина |
|---|---|
| SUCCEEDED → FAILED | Успешный платеж не должен становиться ошибочным |
| FAILED → SUCCEEDED | Ошибочный платеж нельзя повторно сделать успешным без новой попытки оплаты |
| CANCELLED → PROCESSING | Отмененный платеж не должен отправляться в обработку |
| SUCCEEDED → CANCELLED | Успешный платеж нельзя отменить, для этого нужен refund |

## Комментарий

Возвраты не входят в MVP. Поэтому статусы REFUNDED и PARTIALLY_REFUNDED будут добавлены на следующем этапе развития системы.

Refunds are out of MVP scope. Therefore, REFUNDED and PARTIALLY_REFUNDED statuses will be added in the next project stage.
## Диаграмма жизненного цикла платежа / Payment State Machine Diagram

![Жизненный цикл платежа](../diagrams/payment_state_machine.png)

Редактируемый файл draw.io: [payment_state_machine.drawio](../diagrams/payment_state_machine.drawio)

Диаграмма показывает допустимые состояния платежа в рамках MVP: создание платежа, отправку в обработку, успешное завершение, ошибку обработки и отмену до отправки в банк-эквайер.

The diagram shows allowed payment states within the MVP scope: payment creation, processing, successful completion, processing failure, and cancellation before sending the payment to the acquiring bank.

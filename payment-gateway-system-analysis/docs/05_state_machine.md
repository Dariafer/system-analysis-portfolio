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

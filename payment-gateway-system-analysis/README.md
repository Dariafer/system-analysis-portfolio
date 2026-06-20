# Система обработки платежей / Payment Gateway System Analysis

Проект по системному анализу учебной системы обработки платежей для интернет-магазинов.

The project describes system analysis artifacts for a payment processing system used by online merchants.

## Цель проекта / Project Goal

Цель проекта — показать полный цикл работы системного аналитика: определение границ MVP, описание участников, проектирование бизнес-процесса, жизненного цикла платежа, модели данных и API.

The goal is to demonstrate the system analyst workflow: MVP scope definition, actor description, business process modeling, payment state modeling, database design, and API design.

## Состав проекта / Project Structure

| Раздел | Описание |
|---|---|
| `docs/01_scope.md` | Границы MVP |
| `docs/02_actors.md` | Участники системы |
| `docs/03_use_cases.md` | Варианты использования |
| `docs/04_business_process.md` | Бизнес-процесс обработки платежа |
| `docs/05_state_machine.md` | Жизненный цикл платежа |
| `docs/06_database_design.md` | Проектирование базы данных |
| `docs/07_api_design.md` | Проектирование API |
| `docs/08_non_functional_requirements.md` | Нефункциональные требования |
| `docs/09_risks.md` | Риски и ограничения |
| `openapi/payment-gateway.yaml` | OpenAPI-спецификация |
| `diagrams/` | BPMN, State Machine и ERD-диаграммы |

## Основные артефакты / Main Artifacts

### Детальный процесс обработки платежа

![Детальный процесс обработки платежа](diagrams/bpmn_payment_process_detailed.png)

Редактируемый файл: [`bpmn_payment_process_detailed.drawio`](diagrams/bpmn_payment_process_detailed.drawio)

### Жизненный цикл платежа

![Жизненный цикл платежа](diagrams/payment_state_machine.png)

Редактируемый файл: [`payment_state_machine.drawio`](diagrams/payment_state_machine.drawio)

### ERD-модель базы данных

![ERD: Система обработки платежей](diagrams/payment_gateway_erd.png)

Редактируемый файл: [`payment_gateway_erd.drawio`](diagrams/payment_gateway_erd.drawio)

## MVP-функции / MVP Features
- Создание платежа / Payment creation.
- Получение статуса платежа / Payment status retrieval.
- Проверка ключа идемпотентности / Idempotency key validation.
- Обработка результата от mock acquiring bank / Mock acquiring bank result processing.
- Обновление статуса платежа / Payment status update.
- Формирование webhook-события / Webhook event creation.
- Отправка webhook-уведомления мерчанту / Webhook notification delivery to merchant.
- Хранение данных в PostgreSQL / Data storage in PostgreSQL.

## Стек проектирования / Design Stack

- BPMN
- ERD
- State Machine
- OpenAPI
- PostgreSQL
- REST API
- Webhook
- Idempotency Key

## Ограничения MVP / MVP Limitations

- Реальный эквайринг не подключается / Real acquiring is not connected.
- Банковские карты не обрабатываются / Bank cards are not processed.
- PCI DSS не входит в рамки MVP / PCI DSS compliance is out of MVP scope.
- Refund-сценарии не входят в MVP / Refund scenarios are out of MVP scope.
- Антифрод не реализуется / Anti-fraud is not implemented.

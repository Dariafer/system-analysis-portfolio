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

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_payment_success() -> None:
    response = client.post(
        "/api/v1/payments",
        headers={
            "X-API-Key": "test-api-key",
            "Idempotency-Key": "idem-create-payment-success",
        },
        json={
            "merchant_order_id": "order_10001",
            "amount_minor": 125000,
            "currency": "RUB",
            "description": "Payment for order order_10001",
        },
    )

    assert response.status_code == 201
    
    def test_create_payment_rejects_invalid_api_key() -> None:
    response = client.post(
        "/api/v1/payments",
        headers={
            "X-API-Key": "wrong-api-key",
            "Idempotency-Key": "idem-invalid-api-key",
        },
        json={
            "merchant_order_id": "order_invalid_api_key",
            "amount_minor": 10000,
            "currency": "RUB",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["merchant_order_id"] == "order_10001"
    assert data["amount_minor"] == 125000
    assert data["currency"] == "RUB"
    assert data["status"] == "CREATED"
    assert data["payment_id"] is not None




def test_create_payment_requires_api_key() -> None:
    response = client.post(
        "/api/v1/payments",
        headers={
            "Idempotency-Key": "idem-without-api-key",
        },
        json={
            "merchant_order_id": "order_without_api_key",
            "amount_minor": 10000,
            "currency": "RUB",
        },
    )

    assert response.status_code == 401


def test_idempotency_returns_existing_payment() -> None:
    headers = {
        "X-API-Key": "test-api-key",
        "Idempotency-Key": "idem-repeat-payment",
    }

    payload = {
        "merchant_order_id": "order_repeat",
        "amount_minor": 50000,
        "currency": "RUB",
    }

    first_response = client.post(
        "/api/v1/payments",
        headers=headers,
        json=payload,
    )

    second_response = client.post(
        "/api/v1/payments",
        headers=headers,
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["payment_id"] == second_response.json()["payment_id"]


def test_idempotency_conflict() -> None:
    headers = {
        "X-API-Key": "test-api-key",
        "Idempotency-Key": "idem-conflict",
    }

    first_response = client.post(
        "/api/v1/payments",
        headers=headers,
        json={
            "merchant_order_id": "order_conflict",
            "amount_minor": 10000,
            "currency": "RUB",
        },
    )

    second_response = client.post(
        "/api/v1/payments",
        headers=headers,
        json={
            "merchant_order_id": "order_conflict",
            "amount_minor": 20000,
            "currency": "RUB",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_get_payment_success() -> None:
    create_response = client.post(
        "/api/v1/payments",
        headers={
            "X-API-Key": "test-api-key",
            "Idempotency-Key": "idem-get-payment",
        },
        json={
            "merchant_order_id": "order_get",
            "amount_minor": 30000,
            "currency": "RUB",
        },
    )

    payment_id = create_response.json()["payment_id"]

    get_response = client.get(
        f"/api/v1/payments/{payment_id}",
        headers={
            "X-API-Key": "test-api-key",
        },
    )

    assert get_response.status_code == 200
    assert get_response.json()["payment_id"] == payment_id
    assert get_response.json()["merchant_order_id"] == "order_get"


def test_cancel_payment_success() -> None:
    create_response = client.post(
        "/api/v1/payments",
        headers={
            "X-API-Key": "test-api-key",
            "Idempotency-Key": "idem-cancel-payment",
        },
        json={
            "merchant_order_id": "order_cancel",
            "amount_minor": 70000,
            "currency": "RUB",
        },
    )

    payment_id = create_response.json()["payment_id"]

    cancel_response = client.post(
        f"/api/v1/payments/{payment_id}/cancel",
        headers={
            "X-API-Key": "test-api-key",
        },
    )

    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "CANCELLED"


def test_acquiring_callback_success() -> None:
    create_response = client.post(
        "/api/v1/payments",
        headers={
            "X-API-Key": "test-api-key",
            "Idempotency-Key": "idem-callback-success",
        },
        json={
            "merchant_order_id": "order_callback",
            "amount_minor": 90000,
            "currency": "RUB",
        },
    )

    payment_id = create_response.json()["payment_id"]
    acquiring_request_id = f"acq_{payment_id}"

    callback_response = client.post(
        "/api/v1/acquiring/callback",
        json={
            "acquiring_request_id": acquiring_request_id,
            "payment_status": "SUCCEEDED",
            "error_code": None,
            "error_message": None,
        },
    )

    assert callback_response.status_code == 200
    assert callback_response.json() == {"result": "processed"}

    get_response = client.get(
        f"/api/v1/payments/{payment_id}",
        headers={
            "X-API-Key": "test-api-key",
        },
    )

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "SUCCEEDED"

import hashlib
import json
from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.schemas.payment import (
    AcquiringCallbackRequest,
    CallbackProcessingResponse,
    CreatePaymentRequest,
    PaymentResponse,
    PaymentStatus,
)


payments: dict[UUID, PaymentResponse] = {}
idempotency_keys: dict[str, dict[str, str]] = {}
acquiring_requests: dict[str, UUID] = {}


def _request_hash(data: CreatePaymentRequest) -> str:
    raw = json.dumps(data.model_dump(), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def create_payment(
    request: CreatePaymentRequest,
    idempotency_key: str,
) -> PaymentResponse:
    request_hash = _request_hash(request)

    if idempotency_key in idempotency_keys:
        stored = idempotency_keys[idempotency_key]

        if stored["request_hash"] != request_hash:
            raise HTTPException(
                status_code=409,
                detail={
                    "error_code": "IDEMPOTENCY_KEY_CONFLICT",
                    "message": "Idempotency-Key was already used with different request parameters.",
                },
            )

        payment_id = UUID(stored["payment_id"])
        return payments[payment_id]

    now = datetime.now(UTC)
    payment_id = uuid4()
    acquiring_request_id = f"acq_{payment_id}"

    payment = PaymentResponse(
        payment_id=payment_id,
        merchant_order_id=request.merchant_order_id,
        amount_minor=request.amount_minor,
        currency=request.currency,
        status=PaymentStatus.CREATED,
        description=request.description,
        created_at=now,
        updated_at=now,
    )

    payments[payment_id] = payment
    acquiring_requests[acquiring_request_id] = payment_id
    idempotency_keys[idempotency_key] = {
        "request_hash": request_hash,
        "payment_id": str(payment_id),
    }

    return payment


def get_payment(payment_id: UUID) -> PaymentResponse:
    payment = payments.get(payment_id)

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "PAYMENT_NOT_FOUND",
                "message": "Payment not found.",
            },
        )

    return payment


def cancel_payment(payment_id: UUID) -> PaymentResponse:
    payment = get_payment(payment_id)

    if payment.status != PaymentStatus.CREATED:
        raise HTTPException(
            status_code=409,
            detail={
                "error_code": "PAYMENT_CANNOT_BE_CANCELLED",
                "message": "Payment cannot be cancelled in the current status.",
            },
        )

    updated_payment = payment.model_copy(
        update={
            "status": PaymentStatus.CANCELLED,
            "updated_at": datetime.now(UTC),
        }
    )

    payments[payment_id] = updated_payment
    return updated_payment


def process_acquiring_callback(
    request: AcquiringCallbackRequest,
) -> CallbackProcessingResponse:
    payment_id = acquiring_requests.get(request.acquiring_request_id)

    if payment_id is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "PAYMENT_ATTEMPT_NOT_FOUND",
                "message": "Payment attempt not found.",
            },
        )

    payment = get_payment(payment_id)

    if payment.status in {
        PaymentStatus.SUCCEEDED,
        PaymentStatus.FAILED,
        PaymentStatus.CANCELLED,
    }:
        raise HTTPException(
            status_code=409,
            detail={
                "error_code": "PAYMENT_ALREADY_FINAL",
                "message": "Payment is already in a final status.",
            },
        )

    if request.payment_status not in {
        PaymentStatus.SUCCEEDED,
        PaymentStatus.FAILED,
    }:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INVALID_PAYMENT_STATUS",
                "message": "Callback payment_status must be SUCCEEDED or FAILED.",
            },
        )

    updated_payment = payment.model_copy(
        update={
            "status": request.payment_status,
            "updated_at": datetime.now(UTC),
        }
    )

    payments[payment_id] = updated_payment

    return CallbackProcessingResponse(result="processed")

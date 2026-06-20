from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, status

from app.core.config import get_settings
from app.schemas.payment import (
    AcquiringCallbackRequest,
    CallbackProcessingResponse,
    CreatePaymentRequest,
    PaymentResponse,
)
from app.services.payment_service import (
    cancel_payment,
    create_payment,
    get_payment,
    process_acquiring_callback,
)

settings = get_settings()

router = APIRouter(prefix=settings.api_v1_prefix, tags=["Payments"])


def validate_api_key(x_api_key: str | None) -> None:
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "UNAUTHORIZED",
                "message": "Missing X-API-Key header.",
            },
        )

    if x_api_key != settings.default_merchant_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "INVALID_API_KEY",
                "message": "Invalid X-API-Key header.",
            },
        )


@router.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment_endpoint(
    request: CreatePaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> PaymentResponse:
    validate_api_key(x_api_key)
    return create_payment(request, idempotency_key)


@router.get(
    "/payments/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment_endpoint(
    payment_id: UUID,
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> PaymentResponse:
    validate_api_key(x_api_key)
    return get_payment(payment_id)


@router.post(
    "/payments/{payment_id}/cancel",
    response_model=PaymentResponse,
)
def cancel_payment_endpoint(
    payment_id: UUID,
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> PaymentResponse:
    validate_api_key(x_api_key)
    return cancel_payment(payment_id)


@router.post(
    "/acquiring/callback",
    response_model=CallbackProcessingResponse,
    tags=["Acquiring"],
)
def acquiring_callback_endpoint(
    request: AcquiringCallbackRequest,
) -> CallbackProcessingResponse:
    return process_acquiring_callback(request)

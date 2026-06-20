from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class CreatePaymentRequest(BaseModel):
    merchant_order_id: str = Field(..., min_length=1)
    amount_minor: int = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    description: str | None = None


class PaymentResponse(BaseModel):
    payment_id: UUID
    merchant_order_id: str
    amount_minor: int
    currency: str
    status: PaymentStatus
    description: str | None = None
    created_at: datetime
    updated_at: datetime


class AcquiringCallbackRequest(BaseModel):
    acquiring_request_id: str = Field(..., min_length=1)
    payment_status: PaymentStatus
    error_code: str | None = None
    error_message: str | None = None


class CallbackProcessingResponse(BaseModel):
    result: str = "processed"


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict[str, Any] | None = None

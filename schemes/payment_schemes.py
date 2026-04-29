import datetime
from pydantic import BaseModel
from enums.currency import CurrencyEnum
from typing import Optional

class InputPaymentCreate(BaseModel):
    amount: int
    currency: CurrencyEnum

    description: Optional[str] = None
    meta: Optional[dict] = None
    webhook_url: Optional[str] = None

class PayloadPayment(BaseModel):
    payment_id: int
    idempotency_key: str
    amount: int
    currency: CurrencyEnum

    description: Optional[str] = None
    meta: Optional[dict] = None
    webhook_url: Optional[str] = None

class OutputPaymentCreate(BaseModel):
    payment_id: int
    status: str
    created_at: datetime.datetime
    is_new: bool = False

class PaymentRead(BaseModel):
    info_payment: dict
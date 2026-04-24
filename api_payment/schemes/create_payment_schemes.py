import datetime

from enum import Enum
from pydantic import BaseModel

class CurrencyEnum(str, Enum):
    USD = 'USD'
    EUR = 'EUR'
    RUB = 'RUB'

class PaymentCreate(BaseModel):
    amount: int = 0
    currency: CurrencyEnum = 'RUB'
    description: str = None
    meta: str = None
    webhook_url: str = None

class PaymentStatusRead(BaseModel):
    status: str
    payment_id: int
    created_at: datetime.datetime
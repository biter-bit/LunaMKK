from pydantic import BaseModel
from schemes.create_payment_schemes import CurrencyEnum

class EventCreate(BaseModel):
    payment_id: int
    amount: int = 0
    currency: CurrencyEnum = 'RUB'
    description: str = None
    meta: str = None
    webhook_url: str = None
    idempotency_key: str = None
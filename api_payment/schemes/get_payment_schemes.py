from pydantic import BaseModel

class PaymentRead(BaseModel):
    info_payment: str
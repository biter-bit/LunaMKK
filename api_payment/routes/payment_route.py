from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from schemes.create_payment_schemes import PaymentCreate, PaymentStatusRead
from schemes.get_payment_schemes import PaymentRead

payment_router = APIRouter(prefix="/payments", tags=["payment"])

@payment_router.post('/', response_model=PaymentStatusRead)
async def create_payment_route(body: PaymentCreate, idempotency_key: str = Header(..., alias='Idempotency-key')):
    payment = PaymentStatusRead(status='CREATED', payment_id=123, created_at=datetime.now())
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=jsonable_encoder(payment)
    )

@payment_router.get('/{payment_id}', response_model=PaymentRead)
async def get_payment_route(payment_id: str):
    a = payment_id
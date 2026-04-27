from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from schemes.create_payment_schemes import PaymentCreate, PaymentStatusRead
from schemes.get_payment_schemes import PaymentRead
from repositories.outbox_repository import create_task
from repositories.payment_repository import get_payment

payment_router = APIRouter(prefix="/payments", tags=["payment"])

@payment_router.post('/', response_model=PaymentStatusRead)
async def create_payment_route(body: PaymentCreate, idempotency_key: str = Header(..., alias='Idempotency-key')):
    event = await create_task(
        amount=body.amount,
        currency=body.currency,
        idempotency_key=idempotency_key,
        description=body.description,
        meta=body.meta,
        webhook_url=body.webhook_url,
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=event
    )

@payment_router.get('/{payment_id}', response_model=PaymentRead)
async def get_payment_route(payment_id: int):
    payment = await get_payment(payment_id)
    if payment:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=payment
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=None
        )
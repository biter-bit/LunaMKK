from fastapi import APIRouter, status, Depends
from schemes.payment_schemes import OutputPaymentCreate, PayloadPayment
from services.payment_logic import create_payment_logic, get_payment_logic

payment_router = APIRouter(prefix="/payments", tags=["payment"])

@payment_router.post('/', response_model=OutputPaymentCreate, status_code=status.HTTP_202_ACCEPTED)
async def create_payment_route(payment = Depends(create_payment_logic)):
    return payment

@payment_router.get('/{payment_id}', response_model=PayloadPayment)
async def get_payment_route(payment_id: str, payment: dict = Depends(get_payment_logic)):
    return payment
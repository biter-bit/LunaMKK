from schemes.payment_schemes import InputPaymentCreate, PayloadPayment, OutputPaymentCreate
from fastapi import Header, HTTPException, status
from repositories.payment_repository import get_payment, create_payment, get_by_idempotency_key
from repositories.outbox_repository import create_outbox
from core.database import async_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models.payment import Payment


async def create_task(session: AsyncSession, body: InputPaymentCreate, idempotency_key: str) -> tuple[bool, Payment]:
    is_new = True
    try:
        payment = await create_payment(
            session=session,
            amount=body.amount,
            currency=body.currency,
            idempotency_key=idempotency_key,
            description=body.description,
            meta=body.meta,
            webhook_url=body.webhook_url,
        )
        event = PayloadPayment(
            id=payment.id,
            amount=payment.amount,
            currency=payment.currency,
            description=payment.description,
            meta=payment.meta,
            webhook_url=payment.webhook_url,
            idempotency_key=idempotency_key,
        )
        payload = event.model_dump()
        await create_outbox(session=session, payment=payment, payload=payload)
    except IntegrityError:
        await session.rollback()
        payment = await get_by_idempotency_key(session, idempotency_key)
        is_new = False
    return is_new, payment

async def create_payment_logic(
        body: InputPaymentCreate,
        idempotency_key: str = Header(alias='Idempotency-Key')
) -> OutputPaymentCreate:
    async with async_session() as session:
        is_new, payment = await create_task(session=session, body=body, idempotency_key=idempotency_key)
        payment = OutputPaymentCreate.model_validate(payment)
        payment.is_new = is_new
        await session.commit()
    return payment

async def get_payment_logic(payment_id: int) -> PayloadPayment:
    async with async_session() as session:
        payment = await get_payment(session=session, payment_id=payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Payment not found')
        result_payment = PayloadPayment.model_validate(payment)
        await session.commit()
    return result_payment
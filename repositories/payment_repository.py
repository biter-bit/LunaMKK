from core.database import async_session
from models import Payment
from schemes.payment_schemes import PayloadPayment

async def get_by_idempotency_key(session, key: str) -> Payment:
    stmt = select(Payment).where(Payment.idempotency_key == key)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_payment(
        session: AsyncSession,
        amount: int,
        currency: CurrencyEnum,
        idempotency_key: str,
        description: Optional[str] = None,
        meta: Optional[dict] = None,
        webhook_url: Optional[str] = None
) -> Payment:
    payment = Payment(
        amount=amount,
        currency=currency,
        description=description,
        meta=meta,
        webhook_url=webhook_url,
        idempotency_key=idempotency_key,
        status=StatusPayment.PENDING,
    )
    session.add(payment)
    await session.flush()
    return payment

async def get_payment(session: AsyncSession, payment_id: int) -> PayloadPayment:
    payment = await session.get(Payment, payment_id)
    return payment
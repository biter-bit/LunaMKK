from core.database import async_session
from models import Payment
from enums.status import StatusTask
from schemes.get_payment_schemes import PaymentRead

async def get_payment(payment_id):
    async with async_session() as session:
        payment = await session.get(Payment, payment_id)
        payload = {
            'payment_id': payment.id,
            'status': payment.status,
        }
        response = PaymentRead(info_payment=payload)
        return response.model_dump()

# async def create_payment(amount, currency, description, meta, webhook_url, idempotency_key) -> Payment:
#     async with async_session() as session:
#         payment = Payment(
#             amount=amount,
#             currency=currency,
#             description=description,
#             meta=meta,
#             webhook_url=webhook_url,
#             idempotency_key=idempotency_key,
#             status=StatusTask.PENDING,
#         )
#         await session.add(payment)
#         return payment
from core.database import async_session
from models import Outbox, Payment
from enums.status import StatusTask, Exchange, RoutingKey
from schemes.event_schemes import EventCreate
from sqlalchemy import select
from typing import List
from schemes.outbox_schemes import OutboxScheme

async def create_task(amount, currency, description, meta, webhook_url, idempotency_key) -> dict:
    async with async_session() as session:
        payment = Payment(
            amount=amount,
            currency=currency,
            description=description,
            meta=meta,
            webhook_url=webhook_url,
            idempotency_key=idempotency_key,
            status=StatusTask.PENDING,
        )
        session.add(payment)
        await session.flush()
        event = EventCreate(
            payment_id=payment.id,
            amount=amount,
            currency=currency,
            description=description,
            meta=meta,
            webhook_url=webhook_url,
            idempotency_key=idempotency_key,
        )
        payload = event.model_dump()

        outbox = Outbox(
            event_type=Exchange.PAYMENT_EVENTS.value,
            aggregate_id=payment.id,
            payload=payload,
            routing_key=RoutingKey.PAYMENT_CREATED.value,
            status=StatusTask.PENDING,
        )

        session.add(outbox)
        await session.commit()

        return payload

async def get_events() -> List[Outbox | None]:
    async with async_session() as session:
        query = (
            select(Outbox).where(Outbox.status == StatusTask.PENDING)
        )

        result = await session.execute(query)
        events = result.scalars().all()
        return [OutboxScheme.model_validate(e).model_dump() for e in events]
from core.config import settings
from models import Outbox, Payment
from enums.status import StatusTask, StatusEvent, RoutingKey
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


async def create_outbox(session: AsyncSession, payment: Payment, payload: dict):
    outbox = Outbox(
        event_type=StatusEvent.PAYMENT_EVENTS.value,
        aggregate_id=payment.id,
        payload=payload,
        routing_key=RoutingKey.PAYMENT_CREATED.value,
        status=StatusTask.PENDING,
    )
    session.add(outbox)
    return outbox

async def get_outbox(session: AsyncSession) -> List[Outbox]:
    query = (
        select(Outbox)
        .where(Outbox.status == StatusTask.PENDING, Outbox.attempts < settings.OUTBOX_RETRIES)
        .order_by(Outbox.created_at)
        .limit(100)
        .with_for_update(skip_locked=True)
    )

    result = await session.execute(query)
    events = result.scalars().all()
    return events
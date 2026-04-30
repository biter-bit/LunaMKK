import asyncio
from datetime import datetime
from enums.status import StatusTask
from repositories.outbox_repository import get_outbox
from broker.rabbit import publish_event, setup, connect_with_retry
from core.database import async_session
from aio_pika.abc import AbstractRobustConnection, AbstractChannel
import aio_pika
from core.config import settings

from schemes.outbox_schemes import OutboxScheme


async def start_event_worker():
    connection: AbstractRobustConnection = await connect_with_retry(url=settings.RABBIT_URL)

    try:
        channel: AbstractChannel = await connection.channel()
        await setup(channel=channel)
        while True:
            async with async_session() as session:
                outboxes = await get_outbox(session=session)
                for outbox in outboxes:
                    serializer_outbox = OutboxScheme.model_validate(outbox).model_dump()
                    try:
                        await publish_event(serializer_outbox=serializer_outbox, routing_key=outbox.routing_key, channel=channel)
                        outbox.status = StatusTask.SUCCEEDED
                        outbox.published_at = datetime.now()
                    except Exception as e:
                        outbox.attempts += 1
                        if outbox.attempts >= settings.OUTBOX_RETRIES:
                            outbox.status = StatusTask.FAILED
                        outbox.error = str(e)
                await session.commit()
                await asyncio.sleep(10)
    except Exception as e:
        print(f"Exception: {e}")
        raise
    finally:
        await connection.close()
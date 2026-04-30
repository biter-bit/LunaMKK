import asyncio

import aio_pika

from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from broker.rabbit import make_read_event_handler, setup, connect_with_retry
from core.config import settings


async def main():
    connection: AbstractRobustConnection = await connect_with_retry(url=settings.RABBIT_URL)
    channel: AbstractChannel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await setup(channel)
    await queue.consume(make_read_event_handler(channel))
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        pass
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())

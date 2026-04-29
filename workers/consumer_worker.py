import asyncio

import aio_pika

from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from broker.rabbit import read_events, setup
from core.config import settings


async def main():
    connection: AbstractRobustConnection = await aio_pika.connect_robust(url=settings.RABBIT_URL)
    channel: AbstractChannel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await setup(channel)
    await queue.consume(read_events)
    
    print("Consumer started ...")


if __name__ == "__main__":
    asyncio.run(main())
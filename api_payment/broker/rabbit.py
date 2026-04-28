import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.abc import AbstractChannel
from aio_pika import Message
from aio_pika import DeliveryMode
import json
import asyncio

async def send_events(events: list):
    connection: AbstractRobustConnection = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbit:5672//"
    )
    routing_key = "test_queue"

    channel: AbstractChannel = await connection.channel()

    await channel.declare_queue("test_queue", durable=True)

    await channel.default_exchange.publish(
        Message(
            body=json.dumps(events).encode(),
            delivery_mode=DeliveryMode.PERSISTENT
        ),
        routing_key=routing_key,
    )

    await connection.close()

async def read_events():
    connection: AbstractRobustConnection = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbit:5672//"
    )
    channel = await connection.channel()
    queue = await channel.declare_queue("test_queue", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(message.body)
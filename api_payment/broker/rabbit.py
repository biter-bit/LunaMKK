import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.abc import AbstractChannel
from aio_pika import Message
import json
import asyncio

async def send_events(events: list):
    connection: AbstractRobustConnection = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbit:5672//"
    )
    routing_key = "test_queue"

    channel: AbstractChannel = await connection.channel()

    await channel.default_exchange.publish(
        Message(
            body=json.dumps(events).encode(),
        ),
        routing_key=routing_key,
    )

    await connection.close()
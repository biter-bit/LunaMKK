import aio_pika
from aio_pika.abc import AbstractRobustConnection, ExchangeType
from aio_pika.abc import AbstractChannel
from aio_pika import Message, Channel, IncomingMessage
from aio_pika import DeliveryMode
import json
from core.config import settings
from models import Outbox
from schemes.outbox_schemes import OutboxScheme
from sqlalchemy.ext import serializer
from services.emulation_payment_logic import emulation_payment

async def publish_event(serializer_outbox: dict, routing_key: str, channel: AbstractChannel):
    await channel.default_exchange.publish(
        Message(
            body=json.dumps(serializer_outbox).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            headers={
                "x-attempts": 0
            }
        ),
        routing_key=routing_key,
    )

async def setup(channel: AbstractChannel):
    dlx_exchange = await channel.declare_exchange(
        "dlx_exchange",
        ExchangeType.DIRECT,
        durable=True,
    )
    dlq_queue = await channel.declare_queue("dlq_queue", durable=True)
    await dlq_queue.bind(dlx_exchange, routing_key="dlq.create")

    main_queue = await channel.declare_queue(
        "main_queue",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "dlx_exchange",
            "x-dead-letter-routing-key": "dlq.create"
        }
    )
    return main_queue

async def read_events(message: IncomingMessage):

    headers = message.headers or {}
    attempts = headers.get("x-attempts", 0)

    try:
        await emulation_payment(message.body)
        await message.ack()
    except Exception as e:
        if attempts >= 3:
            await message.reject(requeue=False)
        else:
            new_headers = dict(headers)
            new_headers["x-attempts"] = attempts + 1

            await message.channel.default_exchange.publish(
                Message(
                    body=message.body,
                    headers=new_headers,
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=message.routing_key,
            )
            await message.ack()
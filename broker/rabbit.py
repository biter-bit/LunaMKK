from collections.abc import Awaitable, Callable
import asyncio
import json

import aio_pika
from aio_pika.abc import ExchangeType
from aio_pika.abc import AbstractChannel
from aio_pika import Message, IncomingMessage
from aio_pika import DeliveryMode
from core.database import async_session
from repositories.payment_repository import update_status_payment
from services.emulation_payment_logic import emulation_payment
from enums.status import StatusPayment
from services.notification_logic import send_notification

MAX_RETRY_ATTEMPTS = 3
ATTEMPTS_HEADER = "x-attempts"


async def connect_with_retry(url: str, retries: int = 30, delay: int = 2):
    for attempt in range(1, retries + 1):
        try:
            return await aio_pika.connect_robust(url)
        except Exception as exc:
            print(f"Rabbit not ready, retry {attempt}/{retries}: {type(exc).__name__}: {exc}")
            await asyncio.sleep(delay)
    raise RuntimeError("Cannot connect to Rabbit")


async def publish_event(serializer_outbox: dict, routing_key: str, channel: AbstractChannel):
    await channel.default_exchange.publish(
        Message(
            body=json.dumps(serializer_outbox).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            headers={
                ATTEMPTS_HEADER: 0
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
        "payments.new",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "dlx_exchange",
            "x-dead-letter-routing-key": "dlq.create"
        }
    )
    return main_queue


def make_read_event_handler(channel: AbstractChannel) -> Callable[[IncomingMessage], Awaitable[None]]:
    async def handler(message: IncomingMessage) -> None:
        await read_event(message=message, channel=channel)

    return handler


async def read_event(message: IncomingMessage, channel: AbstractChannel):
    headers = message.headers or {}
    attempts = int(headers.get(ATTEMPTS_HEADER, 0))

    try:
        data = json.loads(message.body)
        aggregate_id = data.get("aggregate_id")

        async with async_session() as session:
            await emulation_payment(data)
            payment = await update_status_payment(payment_id=aggregate_id, session=session, status=StatusPayment.SUCCEEDED)
            if not payment:
                raise ValueError(f"Payment {aggregate_id} not found")

            webhook_url = payment.webhook_url
            await session.commit()

        if webhook_url:
            await send_notification(webhook_url)

        await message.ack()
    except Exception:
        if attempts >= MAX_RETRY_ATTEMPTS:
            await message.reject(requeue=False)
        else:
            new_headers = dict(headers)
            new_headers[ATTEMPTS_HEADER] = attempts + 1

            await channel.default_exchange.publish(
                Message(
                    body=message.body,
                    headers=new_headers,
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=message.routing_key,
            )
            await message.ack()

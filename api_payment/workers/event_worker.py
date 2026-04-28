import asyncio

from repositories.outbox_repository import get_events
from broker.rabbit import send_events


async def main():
    while True:
        events = await get_events()
        if events:
            await send_events(events)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
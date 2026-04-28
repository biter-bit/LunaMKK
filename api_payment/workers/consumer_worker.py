import asyncio
from broker.rabbit import read_events

async def main():
    while True:
        await read_events()
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
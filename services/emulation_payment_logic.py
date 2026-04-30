import json
import random
import asyncio


async def emulation_payment(data: dict):
    await asyncio.sleep(random.uniform(2, 5))

    if random.random() < 0.1:
        raise Exception("fail")
    return data
import json


async def emulation_payment(body: bytes):
    data = json.loads(body)

    print(data)
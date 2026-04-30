import aiohttp

async def send_notification(webhook_url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=webhook_url) as resp:
            print("success webhook")
            response_json = await resp.json()
            return response_json
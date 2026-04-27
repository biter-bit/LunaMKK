from fastapi import APIRouter

check_router = APIRouter()

@check_router.get("/live")
async def live():
    return {"status": "alive"}
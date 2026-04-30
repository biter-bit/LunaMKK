import uvicorn
from fastapi import FastAPI, Depends
from routes.payment_route import payment_router
from routes.check_route import check_router
from security.authentication import verify_api_key
from contextlib import asynccontextmanager
from workers.event_worker import start_event_worker
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_event_worker())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(payment_router, prefix="/api/v1")
app.include_router(check_router, prefix="/health")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
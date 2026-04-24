from fastapi import FastAPI
from routes.payment_route import payment_router

app = FastAPI()
app.include_router(payment_router, prefix="/api/v1")
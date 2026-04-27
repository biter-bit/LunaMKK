from fastapi import FastAPI
from routes.payment_route import payment_router
from routes.check_route import check_router

app = FastAPI()
app.include_router(payment_router, prefix="/api/v1")
app.include_router(check_router, prefix="/health")
from fastapi import FastAPI, Depends
from routes.payment_route import payment_router
from routes.check_route import check_router
from security.authentication import verify_api_key

app = FastAPI(dependencies=[Depends(verify_api_key)])
app.include_router(payment_router, prefix="/api/v1")
app.include_router(check_router, prefix="/health")
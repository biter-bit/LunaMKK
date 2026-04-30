from datetime import datetime

from enums.status import StatusTask
from pydantic import BaseModel, field_serializer
from schemes.payment_schemes import PayloadPayment


class OutboxScheme(BaseModel):
    id: int
    event_type: str
    aggregate_id: int
    payload: PayloadPayment

    status: StatusTask
    routing_key: str
    attempts: int
    error: str | None
    published_at: str | None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime):
        return dt.isoformat()

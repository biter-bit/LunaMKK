from datetime import datetime

from enums.status import StatusTask
from pydantic import BaseModel

class OutboxScheme(BaseModel):
    id: int
    event_type: str
    aggregate_id: int
    payload: dict

    status: StatusTask
    routing_key: str
    attempts: int
    error: str | None
    published_at: str | None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
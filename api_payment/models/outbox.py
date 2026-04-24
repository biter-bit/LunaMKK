from db.config import Base, created_at, updated_at
from db.config import intpk
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, JSON, Integer
from datetime import datetime


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[intpk]
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    aggregate_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    routing_key: Mapped[str]
    status: Mapped[str]
    attempts: Mapped[int]
    error: Mapped[str | None]
    published_at: Mapped[datetime | None]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


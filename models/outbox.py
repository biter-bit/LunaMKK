from core.database import Base, created_at, updated_at
from core.database import intpk
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, JSON, Integer, Enum
from enums.status import StatusTask
from datetime import datetime


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[intpk]
    event_type: Mapped[str] = mapped_column(String(100), nullable=False) # что произошло (название события)
    aggregate_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    routing_key: Mapped[str] = mapped_column(String(100), nullable=False) # куда отправить в rabbit
    status: Mapped[StatusTask] = mapped_column(Enum(StatusTask), nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error: Mapped[str | None]
    published_at: Mapped[datetime | None]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


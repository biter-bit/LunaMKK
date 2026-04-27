from core.database import Base, intpk, created_at, updated_at
from enums.currency import CurrencyEnum
from enums.status import StatusTask
from sqlalchemy import Integer, String, JSON, Enum
from sqlalchemy.orm import mapped_column, Mapped


class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[intpk]

    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[StatusTask] = mapped_column(Enum(StatusTask), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    webhook_url: Mapped[str | None] = mapped_column(String(320), nullable=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
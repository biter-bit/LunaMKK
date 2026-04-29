from core.database import Base, intpk, created_at, updated_at
from enums.currency import CurrencyEnum
from enums.status import StatusPayment
from sqlalchemy import Integer, String, JSON, Enum
from sqlalchemy.orm import mapped_column, Mapped


class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[intpk]

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    status: Mapped[StatusPayment] = mapped_column(Enum(StatusPayment), nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum), nullable=False)

    description: Mapped[str | None] = mapped_column(String)
    meta: Mapped[dict | None] = mapped_column(JSON)
    webhook_url: Mapped[str | None] = mapped_column(String(320))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
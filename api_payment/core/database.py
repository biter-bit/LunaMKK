from sqlalchemy.orm import DeclarativeBase, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, func
from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.config import settings

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine(settings.ASYNC_LINK_PG)
async_session = async_sessionmaker(engine=async_engine)

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)]
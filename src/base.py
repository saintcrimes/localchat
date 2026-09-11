from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from Config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from Config import settings
from sqlalchemy import MetaData, Boolean, DateTime
from datetime import datetime, timezone
import logging

logger = logging.getLogger(f"chatapp.{__name__}")
url = settings.database

engine = create_async_engine(url)
logger.info(f"⚡HERE WE GO: {engine}")

metadata = MetaData(schema=settings.DB_SCHEMA)

sessionlocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False
)

async def get_db():
    async with sessionlocal() as session:
        yield session

class Base(DeclarativeBase):

    __abstract__ = True

    metadata = metadata 

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_deleted:  Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
            }


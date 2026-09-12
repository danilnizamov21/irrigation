from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.config import async_database_url

engine = create_async_engine(async_database_url())
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as s:
        yield s


class Base(DeclarativeBase):
    pass

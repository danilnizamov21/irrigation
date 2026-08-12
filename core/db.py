import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

password = os.getenv("POSTGRES_PWD")
name = os.getenv("POSTGRES_NAME")
host = os.getenv("POSTGRES_HOST")
url = f"postgresql+asyncpg://postgres:{password}@{host}/{name}"
url1 = "postgresql+asyncpg://postgres:1234@localhost/irrigation"
engine = create_async_engine(url)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as s:
        yield s


class Base(DeclarativeBase):
    pass

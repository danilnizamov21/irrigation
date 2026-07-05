from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
session = async_sessionmaker(engine, expire_on_commit=False)
from sqlalchemy.orm import declarative_base
async def get_session():
    async with session() as s:
        try:
            yield s
        except:
            await s.close()

Base = declarative_base()
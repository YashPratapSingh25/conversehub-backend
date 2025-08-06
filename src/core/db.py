from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from .config import settings

engine = create_async_engine(
    url = settings.DB_URL,
    pool_size = 10,
    max_overflow = 20,
    pool_pre_ping = True,
    pool_timeout = 30,
    pool_recycle = 3600,
    echo = False
)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
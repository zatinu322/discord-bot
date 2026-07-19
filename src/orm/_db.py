from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from shared.app_context import get_config

config = get_config()


class Base(DeclarativeBase):
    ...


engine = create_async_engine(config.POSTGRES_DSN.get_secret_value())
async_db_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_atomic_session() -> AsyncGenerator[AsyncSession]:
    """Get atomic session."""
    async with async_db_session_maker() as session:
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from accordiq.core.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database.url, echo=settings.database.echo)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

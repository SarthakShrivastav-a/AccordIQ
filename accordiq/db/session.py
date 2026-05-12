from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from accordiq.core.config import get_settings
from accordiq.db.base import Base
import accordiq.models  # noqa: F401


settings = get_settings()
engine = create_async_engine(settings.database.url, echo=settings.database.echo)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


async def init_models() -> None:
    if not settings.database.auto_create_tables:
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

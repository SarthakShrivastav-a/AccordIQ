from __future__ import annotations

from sqlalchemy import inspect, text
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
        if settings.database.url.startswith("sqlite"):
            await conn.run_sync(_ensure_sqlite_dev_columns)


def _ensure_sqlite_dev_columns(sync_conn) -> None:
    inspector = inspect(sync_conn)
    if "workspaces" not in inspector.get_table_names():
        return
    workspace_columns = {column["name"] for column in inspector.get_columns("workspaces")}
    if "organization_id" not in workspace_columns:
        sync_conn.execute(text("ALTER TABLE workspaces ADD COLUMN organization_id VARCHAR"))
        sync_conn.execute(text("CREATE INDEX IF NOT EXISTS ix_workspaces_organization_id ON workspaces (organization_id)"))

from __future__ import annotations

from fastapi import FastAPI
from accordiq.api.admin import router as admin_router
from accordiq.api.health import router as health_router
from accordiq.api.internal import router as internal_router
from accordiq.api.notion import router as notion_router
from accordiq.api.slack import router as slack_router
from accordiq.core.config import get_settings
from accordiq.core.logging import configure_logging

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app.name, version=settings.app.version)
app.include_router(health_router)
app.include_router(slack_router)
app.include_router(notion_router)
app.include_router(admin_router)
app.include_router(internal_router)

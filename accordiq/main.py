from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from accordiq.api.admin import router as admin_router
from accordiq.api.auth import router as auth_router
from accordiq.api.health import router as health_router
from accordiq.api.internal import router as internal_router
from accordiq.api.notion import router as notion_router
from accordiq.api.slack import router as slack_router
from accordiq.core.config import get_settings
from accordiq.core.logging import configure_logging
from accordiq.db.session import init_models


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_models()
    yield

configure_logging()
settings = get_settings()
app = FastAPI(title=settings.app.name, version=settings.app.version, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.auth.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(slack_router)
app.include_router(notion_router)
app.include_router(admin_router)
app.include_router(internal_router)

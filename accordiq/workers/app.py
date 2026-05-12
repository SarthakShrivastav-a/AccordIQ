from __future__ import annotations

from accordiq.core.config import get_settings

def worker_settings() -> dict:
    settings = get_settings()
    return {"queue_name": settings.redis.queue_name, "redis_url": settings.redis.url}

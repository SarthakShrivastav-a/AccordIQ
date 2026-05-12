from fastapi import APIRouter
from accordiq.core.config import get_settings

router = APIRouter(tags=["system"])

@router.get("/health")
async def health():
    return {"status": "ok", "service": get_settings().app.name}

@router.get("/ready")
async def ready():
    return {"status": "ready"}

@router.get("/version")
async def version():
    settings = get_settings()
    return {"name": settings.app.name, "version": settings.app.version}

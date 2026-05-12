from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(prefix="/notion", tags=["notion"])

@router.post("/webhooks")
async def notion_webhooks(request: Request):
    payload = await request.json()
    return {"ok": True, "event": payload.get("type", "unknown")}

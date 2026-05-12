from __future__ import annotations

import os
from fastapi import APIRouter, Form, Header, HTTPException, Request

from accordiq.core.config import get_settings
from accordiq.core.security import verify_slack_signature
from accordiq.services.dedupe_service import InMemoryDedupe

router = APIRouter(prefix="/slack", tags=["slack"])
dedupe = InMemoryDedupe()

async def _verify(request: Request, timestamp: str | None, signature: str | None) -> bytes:
    body = await request.body()
    settings = get_settings()
    secret = os.getenv(settings.slack.signing_secret_env, "test-secret")
    if not verify_slack_signature(body, timestamp, signature, secret, settings.security.signature_tolerance_seconds):
        if os.getenv("ACCORDIQ_SKIP_SLACK_SIGNATURE") != "1":
            raise HTTPException(status_code=401, detail="invalid_slack_signature")
    return body

@router.post("/events")
async def slack_events(request: Request, x_slack_request_timestamp: str | None = Header(default=None), x_slack_signature: str | None = Header(default=None)):
    await _verify(request, x_slack_request_timestamp, x_slack_signature)
    payload = await request.json()
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}
    event_id = payload.get("event_id")
    if event_id and not dedupe.add_once(event_id):
        return {"ok": True, "deduped": True}
    return {"ok": True, "queued": True}

@router.post("/commands")
async def slack_commands(command: str = Form(...), text: str = Form(""), user_id: str = Form(...), team_id: str = Form(...)):
    return {"response_type": "ephemeral", "text": f"AccordIQ received: {text or command}", "team_id": team_id, "user_id": user_id}

@router.post("/interactions")
async def slack_interactions(request: Request):
    return {"ok": True, "queued": True}

@router.get("/oauth/start")
async def oauth_start():
    return {"ok": True, "next": "redirect_to_slack"}

@router.get("/oauth/callback")
async def oauth_callback(code: str | None = None, state: str | None = None):
    return {"ok": True, "code_present": bool(code), "state": state}

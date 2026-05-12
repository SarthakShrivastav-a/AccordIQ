from __future__ import annotations

from accordiq.services.retention_service import retention_cutoff_days

async def process_retention_job(payload: dict) -> dict:
    return {"workspace_id": payload.get("workspace_id"), "cutoff_days": retention_cutoff_days(payload.get("retention_days", 365))}

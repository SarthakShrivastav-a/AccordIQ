from __future__ import annotations

from accordiq.core.security import deterministic_id

def build_accordiq_id(workspace_id: str, message_ts: str, entity_type: str, title: str) -> str:
    return deterministic_id(workspace_id, message_ts, entity_type, title.lower(), prefix="acc")

def route_entity_status(confidence: float, threshold: float) -> str:
    return "active" if confidence >= threshold else "review"

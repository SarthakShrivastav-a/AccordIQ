from __future__ import annotations

def build_export_payload(workspace_id: str, rows: list[dict]) -> dict:
    return {"workspace_id": workspace_id, "format": "json", "rows": rows}

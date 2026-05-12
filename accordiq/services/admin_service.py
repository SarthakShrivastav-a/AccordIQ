from __future__ import annotations

class AdminService:
    def list_workspaces(self) -> list[dict]:
        return []

    def get_workspace(self, workspace_id: str) -> dict:
        return {"workspace_id": workspace_id, "capture_enabled": True}

    def metrics(self, workspace_id: str) -> dict:
        return {"workspace_id": workspace_id, "captured_messages": 0, "entities": 0, "queries": 0}

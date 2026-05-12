from __future__ import annotations

from fastapi import APIRouter
from accordiq.schemas.admin import RetryJobRequest, ReviewUpdate, WorkspaceSettingsUpdate
from accordiq.services.admin_service import AdminService
from accordiq.services.export_service import build_export_payload

router = APIRouter(prefix="/api/admin", tags=["admin"])
service = AdminService()

@router.get("/workspaces")
async def list_workspaces():
    return {"items": service.list_workspaces()}

@router.get("/workspaces/{workspace_id}")
async def get_workspace(workspace_id: str):
    return service.get_workspace(workspace_id)

@router.patch("/workspaces/{workspace_id}/settings")
async def update_settings(workspace_id: str, payload: WorkspaceSettingsUpdate):
    return {"workspace_id": workspace_id, "updated": payload.model_dump(exclude_none=True)}

@router.get("/workspaces/{workspace_id}/activity")
async def activity(workspace_id: str):
    return {"workspace_id": workspace_id, "items": []}

@router.get("/workspaces/{workspace_id}/entities")
async def entities(workspace_id: str, status: str | None = None):
    return {"workspace_id": workspace_id, "status": status, "items": []}

@router.patch("/entities/{entity_id}/review")
async def review_entity(entity_id: str, payload: ReviewUpdate):
    return {"entity_id": entity_id, "review": payload.model_dump()}

@router.get("/workspaces/{workspace_id}/jobs")
async def jobs(workspace_id: str):
    return {"workspace_id": workspace_id, "items": []}

@router.post("/jobs/{job_id}/retry")
async def retry_job(job_id: str, payload: RetryJobRequest):
    return {"job_id": job_id, "retry": True, "reason": payload.reason}

@router.get("/workspaces/{workspace_id}/audit-log")
async def audit_log(workspace_id: str):
    return {"workspace_id": workspace_id, "items": []}

@router.get("/workspaces/{workspace_id}/metrics")
async def metrics(workspace_id: str):
    return service.metrics(workspace_id)

@router.get("/workspaces/{workspace_id}/export")
async def export_workspace(workspace_id: str):
    return build_export_payload(workspace_id, [])

@router.delete("/workspaces/{workspace_id}/wipe")
async def wipe_workspace(workspace_id: str):
    return {"workspace_id": workspace_id, "wipe_queued": True}

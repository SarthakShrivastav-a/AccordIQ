from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.api.deps import get_current_user, require_role, require_workspace_member
from accordiq.db.session import get_db_session
from accordiq.models.auth import User
from accordiq.models.entity import Entity
from accordiq.models.job import JobRecord
from accordiq.schemas.admin import RetryJobRequest, ReviewUpdate, WorkspaceSettingsUpdate
from accordiq.services.admin_service import AdminService
from accordiq.services.export_service import build_export_payload

router = APIRouter(prefix="/api/admin", tags=["admin"])
service = AdminService()


@router.get("/workspaces")
async def list_workspaces(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return {"items": await service.list_workspaces(session, user)}


@router.get("/workspaces/{workspace_id}")
async def get_workspace(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    workspace = await service.get_workspace(session, workspace_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="workspace_not_found")
    return workspace


@router.patch("/workspaces/{workspace_id}/settings")
async def update_settings(workspace_id: str, payload: WorkspaceSettingsUpdate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    membership = await require_workspace_member(workspace_id, user, session)
    require_role(membership, {"owner", "admin"})
    workspace = await service.update_settings(session, workspace_id, payload.model_dump(exclude_none=True), user.id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="workspace_not_found")
    return workspace


@router.get("/workspaces/{workspace_id}/activity")
async def activity(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    return {"workspace_id": workspace_id, "items": await service.activity(session, workspace_id)}


@router.get("/workspaces/{workspace_id}/entities")
async def entities(workspace_id: str, status: str | None = None, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    return {"workspace_id": workspace_id, "status": status, "items": await service.entities(session, workspace_id, status)}


@router.patch("/entities/{entity_id}/review")
async def review_entity(entity_id: str, payload: ReviewUpdate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    existing = await session.get(Entity, entity_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="entity_not_found")
    await require_workspace_member(existing.workspace_id, user, session)
    entity = await service.review_entity(session, entity_id, payload.status, user.id, payload.note)
    return entity


@router.get("/workspaces/{workspace_id}/jobs")
async def jobs(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    return {"workspace_id": workspace_id, "items": await service.jobs(session, workspace_id)}


@router.post("/jobs/{job_id}/retry")
async def retry_job(job_id: str, payload: RetryJobRequest, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    existing = await session.get(JobRecord, job_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="job_not_found")
    if existing.workspace_id:
        await require_workspace_member(existing.workspace_id, user, session)
    retry = await service.retry_job(session, job_id, user.id, payload.reason)
    return {"retry": retry}


@router.get("/workspaces/{workspace_id}/audit-log")
async def audit_log(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    return {"workspace_id": workspace_id, "items": await service.audit_log(session, workspace_id)}


@router.get("/workspaces/{workspace_id}/metrics")
async def metrics(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    return await service.metrics(session, workspace_id)


@router.get("/workspaces/{workspace_id}/export")
async def export_workspace(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await require_workspace_member(workspace_id, user, session)
    entities_payload = await service.entities(session, workspace_id)
    return build_export_payload(workspace_id, entities_payload)


@router.delete("/workspaces/{workspace_id}/wipe")
async def wipe_workspace(workspace_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    membership = await require_workspace_member(workspace_id, user, session)
    require_role(membership, {"owner", "admin"})
    return {"workspace_id": workspace_id, "wipe_queued": True, "job": await service.queue_wipe(session, workspace_id, user.id)}

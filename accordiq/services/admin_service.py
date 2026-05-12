from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.core.time import utc_now
from accordiq.models.audit import AuditEvent
from accordiq.models.auth import User, WorkspaceMembership
from accordiq.models.entity import Entity
from accordiq.models.graph_run import GraphRun
from accordiq.models.job import JobRecord
from accordiq.models.message import SlackMessage
from accordiq.models.workspace import Workspace


class AdminService:
    async def list_workspaces(self, session: AsyncSession, user: User) -> list[dict]:
        result = await session.execute(
            select(Workspace, WorkspaceMembership.role)
            .join(WorkspaceMembership, WorkspaceMembership.workspace_id == Workspace.id)
            .where(WorkspaceMembership.user_id == user.id)
            .order_by(Workspace.name)
        )
        return [self._workspace_dict(workspace, role) for workspace, role in result.all()]

    async def get_workspace(self, session: AsyncSession, workspace_id: str) -> dict | None:
        workspace = await session.get(Workspace, workspace_id)
        if workspace is None:
            return None
        return self._workspace_dict(workspace)

    async def update_settings(self, session: AsyncSession, workspace_id: str, payload: dict, actor_id: str) -> dict | None:
        workspace = await session.get(Workspace, workspace_id)
        if workspace is None:
            return None
        settings_json = dict(workspace.settings_json or {})
        for key, value in payload.items():
            if key == "capture_enabled":
                workspace.capture_enabled = bool(value)
            else:
                settings_json[key] = value
        workspace.settings_json = settings_json
        session.add(AuditEvent(workspace_id=workspace_id, actor_id=actor_id, action="workspace.settings.updated", target_type="workspace", target_id=workspace_id, payload_json=payload))
        await session.commit()
        await session.refresh(workspace)
        return self._workspace_dict(workspace)

    async def activity(self, session: AsyncSession, workspace_id: str) -> list[dict]:
        result = await session.execute(
            select(AuditEvent).where(AuditEvent.workspace_id == workspace_id).order_by(AuditEvent.created_at.desc()).limit(50)
        )
        return [self._audit_dict(item) for item in result.scalars().all()]

    async def entities(self, session: AsyncSession, workspace_id: str, status: str | None = None) -> list[dict]:
        query = select(Entity).where(Entity.workspace_id == workspace_id).order_by(Entity.updated_at.desc())
        if status:
            query = query.where(Entity.status == status)
        result = await session.execute(query.limit(100))
        return [self._entity_dict(item) for item in result.scalars().all()]

    async def review_entity(self, session: AsyncSession, entity_id: str, status: str, reviewer_id: str, note: str | None = None) -> dict | None:
        entity = await session.get(Entity, entity_id)
        if entity is None:
            return None
        entity.status = status
        payload = {"status": status, "note": note}
        session.add(AuditEvent(workspace_id=entity.workspace_id, actor_id=reviewer_id, action="entity.reviewed", target_type="entity", target_id=entity.id, payload_json=payload))
        await session.commit()
        await session.refresh(entity)
        return self._entity_dict(entity)

    async def jobs(self, session: AsyncSession, workspace_id: str) -> list[dict]:
        result = await session.execute(
            select(JobRecord).where(JobRecord.workspace_id == workspace_id).order_by(JobRecord.created_at.desc()).limit(100)
        )
        return [self._job_dict(item) for item in result.scalars().all()]

    async def retry_job(self, session: AsyncSession, job_id: str, actor_id: str, reason: str | None = None) -> dict | None:
        job = await session.get(JobRecord, job_id)
        if job is None:
            return None
        retry = JobRecord(workspace_id=job.workspace_id, job_type=job.job_type, status="queued", payload_json=job.payload_json, error=None)
        session.add(retry)
        if job.workspace_id:
            session.add(AuditEvent(workspace_id=job.workspace_id, actor_id=actor_id, action="job.retry_queued", target_type="job", target_id=job.id, payload_json={"reason": reason, "retry_job_id": retry.id}))
        await session.commit()
        await session.refresh(retry)
        return self._job_dict(retry)

    async def audit_log(self, session: AsyncSession, workspace_id: str) -> list[dict]:
        result = await session.execute(
            select(AuditEvent).where(AuditEvent.workspace_id == workspace_id).order_by(AuditEvent.created_at.desc()).limit(100)
        )
        return [self._audit_dict(item) for item in result.scalars().all()]

    async def metrics(self, session: AsyncSession, workspace_id: str) -> dict:
        captured_messages = await self._count(session, SlackMessage, workspace_id)
        entities = await self._count(session, Entity, workspace_id)
        jobs = await self._count(session, JobRecord, workspace_id)
        failed_jobs = await self._count(session, JobRecord, workspace_id, JobRecord.status == "failed")
        queries = await self._count(session, GraphRun, workspace_id, GraphRun.graph_name == "query")
        return {"workspace_id": workspace_id, "captured_messages": captured_messages, "entities": entities, "jobs": jobs, "failed_jobs": failed_jobs, "queries": queries}

    async def queue_wipe(self, session: AsyncSession, workspace_id: str, actor_id: str) -> dict:
        job = JobRecord(workspace_id=workspace_id, job_type="workspace_wipe", status="queued", payload_json={"requested_at": utc_now().isoformat()})
        session.add(job)
        session.add(AuditEvent(workspace_id=workspace_id, actor_id=actor_id, action="workspace.wipe_queued", target_type="workspace", target_id=workspace_id, payload_json={"job_id": job.id}))
        await session.commit()
        await session.refresh(job)
        return self._job_dict(job)

    async def _count(self, session: AsyncSession, model, workspace_id: str, *conditions) -> int:
        result = await session.execute(select(func.count()).select_from(model).where(model.workspace_id == workspace_id, *conditions))
        return int(result.scalar_one())

    def _workspace_dict(self, workspace: Workspace, role: str | None = None) -> dict:
        settings = workspace.settings_json or {}
        return {
            "workspace_id": workspace.id,
            "name": workspace.name,
            "capture_enabled": workspace.capture_enabled,
            "retention_days": int(settings.get("retention_days", 365)),
            "channel_mode": settings.get("channel_mode", "invited_channels"),
            "last_activity": workspace.updated_at.isoformat() if workspace.updated_at else None,
            "role": role,
        }

    def _entity_dict(self, entity: Entity) -> dict:
        source = entity.payload_json.get("source", {}) if entity.payload_json else {}
        return {
            "id": entity.id,
            "workspace_id": entity.workspace_id,
            "title": entity.title,
            "entity_type": entity.entity_type,
            "confidence": entity.confidence,
            "status": entity.status,
            "source": source.get("permalink") or source.get("channel_id") or entity.source_message_id,
            "summary": entity.summary,
            "updated_at": entity.updated_at.isoformat() if entity.updated_at else None,
        }

    def _job_dict(self, job: JobRecord) -> dict:
        return {
            "id": job.id,
            "workspace_id": job.workspace_id,
            "job_type": job.job_type,
            "status": job.status,
            "error": job.error,
            "created_at": job.created_at.isoformat() if job.created_at else None,
        }

    def _audit_dict(self, item: AuditEvent) -> dict:
        return {
            "id": item.id,
            "workspace_id": item.workspace_id,
            "actor_id": item.actor_id,
            "action": item.action,
            "target_type": item.target_type,
            "target_id": item.target_id,
            "payload": item.payload_json,
            "created_at": item.created_at.isoformat() if item.created_at else None,
        }

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.api.deps import get_current_user
from accordiq.db.session import get_db_session
from accordiq.models.auth import User
from accordiq.schemas.organization import CapturePolicyRead, CapturePolicyUpdate, IntegrationRead, InviteCreate, InviteRead, OrganizationCreate, OrganizationMemberRead, OrganizationRead, UsageRead
from accordiq.services.organization_service import OrganizationService

router = APIRouter(prefix="/api/orgs", tags=["organizations"])
service = OrganizationService()


@router.post("", response_model=OrganizationRead)
async def create_org(payload: OrganizationCreate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await service.create_organization(session, user, payload.name)


@router.get("", response_model=list[OrganizationRead])
async def list_orgs(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await service.list_organizations(session, user)


@router.get("/{org_id}", response_model=OrganizationRead)
async def get_org(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    return await _require_org(org_id, user, session)


@router.get("/{org_id}/members", response_model=list[OrganizationMemberRead])
async def members(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session)
    return await service.list_members(session, org_id)


@router.post("/{org_id}/invites", response_model=InviteRead)
async def invites(org_id: str, payload: InviteCreate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    membership = await service.get_membership(session, org_id, user)
    if membership is None:
        raise HTTPException(status_code=403, detail="organization_access_denied")
    if membership.role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="role_not_allowed")
    try:
        return await service.create_invite(session, org_id, payload.email, payload.role, user.id)
    except ValueError:
        raise HTTPException(status_code=422, detail="invalid_role")


@router.get("/{org_id}/integrations", response_model=list[IntegrationRead])
async def integrations(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session)
    return await service.list_integrations(session, org_id)


@router.post("/{org_id}/integrations/slack/start")
async def slack_start(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session, {"owner", "admin"})
    integration = await service.mark_integration_pending(session, org_id, "slack")
    return {"provider": "slack", "status": integration["status"], "next": "/slack/oauth/start"}


@router.post("/{org_id}/integrations/notion/start")
async def notion_start(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session, {"owner", "admin"})
    integration = await service.mark_integration_pending(session, org_id, "notion")
    return {"provider": "notion", "status": integration["status"], "next": "/notion/oauth/start"}


@router.get("/{org_id}/usage", response_model=UsageRead)
async def usage(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session)
    return await service.usage(session, org_id)


@router.get("/{org_id}/capture-policy", response_model=CapturePolicyRead)
async def capture_policy(org_id: str, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session)
    return await service.capture_policy(session, org_id)


@router.patch("/{org_id}/capture-policy", response_model=CapturePolicyRead)
async def update_capture_policy(org_id: str, payload: CapturePolicyUpdate, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    await _require_org(org_id, user, session, {"owner", "admin"})
    return await service.update_capture_policy(session, org_id, payload.model_dump(exclude_none=True))


async def _require_org(org_id: str, user: User, session: AsyncSession, roles: set[str] | None = None) -> dict:
    membership = await service.get_membership(session, org_id, user)
    if membership is None:
        raise HTTPException(status_code=403, detail="organization_access_denied")
    if roles and membership.role not in roles:
        raise HTTPException(status_code=403, detail="role_not_allowed")
    try:
        return await service.organization_read(session, org_id, user)
    except PermissionError:
        raise HTTPException(status_code=403, detail="organization_access_denied")

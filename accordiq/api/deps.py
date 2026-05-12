from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.core.config import get_settings
from accordiq.core.security import decode_access_token
from accordiq.db.session import get_db_session
from accordiq.models.auth import User, WorkspaceMembership
from accordiq.models.organization import OrganizationMembership
from accordiq.models.workspace import Workspace

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing_bearer_token")
    try:
        claims = decode_access_token(credentials.credentials, get_settings().auth.jwt)
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token")
    result = await session.execute(select(User).where(User.id == claims["sub"], User.status == "active"))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user_not_found")
    return user


async def require_workspace_member(workspace_id: str, user: User, session: AsyncSession) -> WorkspaceMembership:
    result = await session.execute(
        select(WorkspaceMembership).where(
            WorkspaceMembership.user_id == user.id,
            WorkspaceMembership.workspace_id == workspace_id,
        )
    )
    membership = result.scalar_one_or_none()
    if membership is not None:
        return membership
    workspace = await session.get(Workspace, workspace_id)
    if workspace and workspace.organization_id:
        org_result = await session.execute(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == user.id,
                OrganizationMembership.organization_id == workspace.organization_id,
            )
        )
        org_membership = org_result.scalar_one_or_none()
        if org_membership is not None:
            return WorkspaceMembership(user_id=user.id, workspace_id=workspace_id, role=org_membership.role)
    if membership is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="workspace_access_denied")
    return membership


def require_role(membership: WorkspaceMembership, allowed_roles: set[str]) -> None:
    if membership.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="role_not_allowed")

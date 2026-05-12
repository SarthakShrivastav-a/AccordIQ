from __future__ import annotations

from urllib.parse import urlencode

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.api.deps import get_current_user
from accordiq.core.config import get_settings
from accordiq.db.session import get_db_session
from accordiq.models.auth import User, WorkspaceMembership
from accordiq.models.organization import OrganizationMembership
from accordiq.schemas.auth import MembershipRead, OrganizationMembershipRead, UserRead
from accordiq.services.auth_service import AuthError, AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/google/start")
async def google_start(session: AsyncSession = Depends(get_db_session)):
    try:
        url = await AuthService().build_google_start_url(session)
    except AuthError as exc:
        return _error_redirect(exc.code)
    return RedirectResponse(url)


@router.get("/google/callback")
async def google_callback(code: str | None = None, state: str | None = None, session: AsyncSession = Depends(get_db_session)):
    try:
        token = await AuthService().handle_google_callback(session, code, state)
    except AuthError as exc:
        await session.rollback()
        return _error_redirect(exc.code)
    success_url = get_settings().auth.frontend_success_url
    separator = "&" if "?" in success_url else "?"
    return RedirectResponse(f"{success_url}{separator}{urlencode({'token': token})}")


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(WorkspaceMembership).where(WorkspaceMembership.user_id == user.id))
    memberships = [MembershipRead(workspace_id=item.workspace_id, role=item.role) for item in result.scalars().all()]
    org_result = await session.execute(select(OrganizationMembership).where(OrganizationMembership.user_id == user.id))
    organizations = [OrganizationMembershipRead(organization_id=item.organization_id, role=item.role) for item in org_result.scalars().all()]
    return UserRead(id=user.id, email=user.email, name=user.name, picture=user.picture, memberships=memberships, organizations=organizations)


@router.post("/logout")
async def logout():
    return {"ok": True}


def _error_redirect(code: str) -> RedirectResponse:
    error_url = get_settings().auth.frontend_error_url
    separator = "&" if "?" in error_url else "?"
    return RedirectResponse(f"{error_url}{separator}{urlencode({'error': code})}")

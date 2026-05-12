from __future__ import annotations

import os
import uuid

from accordiq.core.config import get_settings
from accordiq.core.security import create_access_token
from accordiq.db.session import AsyncSessionLocal, init_models
from accordiq.models.auth import User, WorkspaceMembership
from accordiq.models.organization import Organization, OrganizationMembership
from accordiq.models.workspace import Workspace

os.environ.setdefault("ACCORDIQ_JWT_SECRET", "test-jwt-secret-for-accordiq-auth-tests")


async def seed_member(role: str = "admin") -> tuple[dict[str, str], str, str]:
    await init_models()
    suffix = uuid.uuid4().hex[:8]
    async with AsyncSessionLocal() as session:
        user = User(email=f"admin-{suffix}@example.com", name="Admin", google_sub=f"google-{suffix}", status="active")
        organization = Organization(name=f"Org {suffix}", slug=f"org-{suffix}", owner_user_id=user.id, settings_json={"retention_days": 365, "channel_mode": "invited_channels", "ignored_channels": [], "allowed_channels": []})
        session.add(user)
        await session.flush()
        organization.owner_user_id = user.id
        session.add(organization)
        await session.flush()
        workspace = Workspace(organization_id=organization.id, slack_team_id=f"T-{suffix}", name=f"Workspace {suffix}", capture_enabled=True, settings_json={"retention_days": 365, "channel_mode": "invited_channels"})
        session.add(workspace)
        await session.flush()
        session.add(OrganizationMembership(organization_id=organization.id, user_id=user.id, role="owner" if role == "admin" else role))
        session.add(WorkspaceMembership(user_id=user.id, workspace_id=workspace.id, role=role))
        await session.commit()
        token = create_access_token(user.id, user.email, get_settings().auth.jwt)
        return {"Authorization": f"Bearer {token}"}, workspace.id, user.id

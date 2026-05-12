from __future__ import annotations

import re

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from accordiq.core.config import get_settings
from accordiq.models.auth import User, WorkspaceMembership
from accordiq.models.organization import IntegrationConnection, Organization, OrganizationInvite, OrganizationMembership, UsageEvent
from accordiq.models.workspace import Workspace


class OrganizationService:
    def _slug(self, name: str) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "organization"
        return base[:64]

    async def create_organization(self, session: AsyncSession, user: User, name: str) -> dict:
        slug = await self._unique_slug(session, self._slug(name))
        organization = Organization(name=name, slug=slug, owner_user_id=user.id, settings_json=self._default_settings())
        session.add(organization)
        await session.flush()
        session.add(OrganizationMembership(organization_id=organization.id, user_id=user.id, role="owner"))
        await self._ensure_default_integrations(session, organization.id)
        workspace = Workspace(organization_id=organization.id, slack_team_id=f"pending-{organization.id}", name=name, capture_enabled=True, settings_json=organization.settings_json)
        session.add(workspace)
        await session.flush()
        session.add(WorkspaceMembership(user_id=user.id, workspace_id=workspace.id, role="admin"))
        await session.commit()
        await session.refresh(organization)
        return await self.organization_read(session, organization.id, user)

    async def list_organizations(self, session: AsyncSession, user: User) -> list[dict]:
        result = await session.execute(
            select(Organization, OrganizationMembership.role)
            .join(OrganizationMembership, OrganizationMembership.organization_id == Organization.id)
            .where(OrganizationMembership.user_id == user.id)
            .order_by(Organization.created_at.desc())
        )
        return [self._org_dict(org, role) for org, role in result.all()]

    async def organization_read(self, session: AsyncSession, organization_id: str, user: User) -> dict:
        result = await session.execute(
            select(Organization, OrganizationMembership.role)
            .join(OrganizationMembership, OrganizationMembership.organization_id == Organization.id)
            .where(Organization.id == organization_id, OrganizationMembership.user_id == user.id)
        )
        row = result.one_or_none()
        if row is None:
            raise PermissionError("organization_access_denied")
        org, role = row
        return self._org_dict(org, role)

    async def get_membership(self, session: AsyncSession, organization_id: str, user: User) -> OrganizationMembership | None:
        result = await session.execute(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.user_id == user.id,
            )
        )
        return result.scalar_one_or_none()

    async def list_members(self, session: AsyncSession, organization_id: str) -> list[dict]:
        result = await session.execute(
            select(User, OrganizationMembership.role)
            .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
            .where(OrganizationMembership.organization_id == organization_id)
            .order_by(User.email)
        )
        return [{"user_id": user.id, "email": user.email, "name": user.name, "role": role} for user, role in result.all()]

    async def create_invite(self, session: AsyncSession, organization_id: str, email: str, role: str, invited_by_user_id: str) -> dict:
        allowed = set(get_settings().saas.allowed_org_roles)
        if role not in allowed:
            raise ValueError("invalid_role")
        invite = OrganizationInvite(organization_id=organization_id, email=email.lower(), role=role, invited_by_user_id=invited_by_user_id)
        session.add(invite)
        await session.commit()
        await session.refresh(invite)
        return self._invite_dict(invite)

    async def list_integrations(self, session: AsyncSession, organization_id: str) -> list[dict]:
        await self._ensure_default_integrations(session, organization_id)
        result = await session.execute(select(IntegrationConnection).where(IntegrationConnection.organization_id == organization_id).order_by(IntegrationConnection.provider))
        return [self._integration_dict(item) for item in result.scalars().all()]

    async def mark_integration_pending(self, session: AsyncSession, organization_id: str, provider: str) -> dict:
        await self._ensure_default_integrations(session, organization_id)
        result = await session.execute(select(IntegrationConnection).where(IntegrationConnection.organization_id == organization_id, IntegrationConnection.provider == provider))
        integration = result.scalar_one()
        integration.status = "pending"
        await session.commit()
        await session.refresh(integration)
        return self._integration_dict(integration)

    async def usage(self, session: AsyncSession, organization_id: str) -> dict:
        counts: dict[str, int] = {}
        for event_type in get_settings().saas.usage.event_types:
            result = await session.execute(
                select(func.coalesce(func.sum(UsageEvent.quantity), 0)).where(
                    UsageEvent.organization_id == organization_id,
                    UsageEvent.event_type == event_type,
                )
            )
            counts[event_type] = int(result.scalar_one())
        return {
            "organization_id": organization_id,
            "captured_messages": counts.get("captured_message", 0),
            "extracted_entities": counts.get("extracted_entity", 0),
            "grounded_queries": counts.get("grounded_query", 0),
            "notion_syncs": counts.get("notion_sync", 0),
        }

    async def capture_policy(self, session: AsyncSession, organization_id: str) -> dict:
        org = await session.get(Organization, organization_id)
        if org is None:
            raise LookupError("organization_not_found")
        settings = dict(org.settings_json or self._default_settings())
        return {"organization_id": organization_id, **settings}

    async def update_capture_policy(self, session: AsyncSession, organization_id: str, update: dict) -> dict:
        org = await session.get(Organization, organization_id)
        if org is None:
            raise LookupError("organization_not_found")
        settings = dict(org.settings_json or self._default_settings())
        settings.update(update)
        org.settings_json = settings
        result = await session.execute(select(Workspace).where(Workspace.organization_id == organization_id))
        for workspace in result.scalars().all():
            workspace.settings_json = settings
        await session.commit()
        return {"organization_id": organization_id, **settings}

    async def record_usage(self, session: AsyncSession, organization_id: str, event_type: str, workspace_id: str | None = None, quantity: int = 1) -> None:
        session.add(UsageEvent(organization_id=organization_id, workspace_id=workspace_id, event_type=event_type, quantity=quantity, metadata_json={}))

    async def _unique_slug(self, session: AsyncSession, slug: str) -> str:
        candidate = slug
        index = 2
        while True:
            result = await session.execute(select(Organization).where(Organization.slug == candidate))
            if result.scalar_one_or_none() is None:
                return candidate
            candidate = f"{slug}-{index}"
            index += 1

    async def _ensure_default_integrations(self, session: AsyncSession, organization_id: str) -> None:
        for provider in ("slack", "notion"):
            result = await session.execute(select(IntegrationConnection).where(IntegrationConnection.organization_id == organization_id, IntegrationConnection.provider == provider))
            if result.scalar_one_or_none() is None:
                session.add(IntegrationConnection(organization_id=organization_id, provider=provider, status="not_connected", metadata_json={}))
        await session.flush()

    def _default_settings(self) -> dict:
        settings = get_settings()
        return {
            "channel_mode": settings.capture.default_mode,
            "retention_days": settings.workflow.default_retention_days,
            "ignored_channels": [],
            "allowed_channels": [],
        }

    def _org_dict(self, org: Organization, role: str) -> dict:
        required = set(get_settings().saas.onboarding.required_steps)
        completed = set((org.settings_json or {}).get("completed_steps", []))
        return {"id": org.id, "name": org.name, "slug": org.slug, "role": role, "status": org.status, "onboarding_complete": required.issubset(completed)}

    def _invite_dict(self, invite: OrganizationInvite) -> dict:
        return {"id": invite.id, "organization_id": invite.organization_id, "email": invite.email, "role": invite.role, "accepted": invite.accepted_at is not None}

    def _integration_dict(self, item: IntegrationConnection) -> dict:
        return {"provider": item.provider, "status": item.status, "external_id": item.external_id, "metadata": item.metadata_json or {}}

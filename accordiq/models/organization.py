import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from accordiq.db.base import Base
from accordiq.models.mixins import TimestampMixin


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    owner_user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String, default="active", index=True)
    settings_json: Mapped[dict] = mapped_column(JSON, default=dict)


class OrganizationMembership(TimestampMixin, Base):
    __tablename__ = "organization_memberships"
    __table_args__ = (UniqueConstraint("organization_id", "user_id", name="uq_org_membership_org_user"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String, default="owner", index=True)


class OrganizationInvite(TimestampMixin, Base):
    __tablename__ = "organization_invites"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), index=True)
    email: Mapped[str] = mapped_column(String, index=True)
    role: Mapped[str] = mapped_column(String, default="viewer")
    invited_by_user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class IntegrationConnection(TimestampMixin, Base):
    __tablename__ = "integration_connections"
    __table_args__ = (UniqueConstraint("organization_id", "provider", name="uq_integration_org_provider"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), index=True)
    provider: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, default="not_connected", index=True)
    external_id: Mapped[str | None] = mapped_column(String, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class UsageEvent(TimestampMixin, Base):
    __tablename__ = "usage_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), index=True)
    workspace_id: Mapped[str | None] = mapped_column(String, ForeignKey("workspaces.id"), index=True, nullable=True)
    event_type: Mapped[str] = mapped_column(String, index=True)
    quantity: Mapped[int] = mapped_column(default=1)
    billable: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

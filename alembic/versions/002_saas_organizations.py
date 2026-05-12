"""add saas organization tables

Revision ID: 002_saas_organizations
Revises: 001_auth_tables
Create Date: 2026-05-13
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "002_saas_organizations"
down_revision = "001_auth_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("owner_user_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("settings_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organizations_owner_user_id"), "organizations", ["owner_user_id"], unique=False)
    op.create_index(op.f("ix_organizations_slug"), "organizations", ["slug"], unique=True)
    op.create_index(op.f("ix_organizations_status"), "organizations", ["status"], unique=False)
    op.add_column("workspaces", sa.Column("organization_id", sa.String(), nullable=True))
    op.create_foreign_key("fk_workspaces_organization_id", "workspaces", "organizations", ["organization_id"], ["id"])
    op.create_index(op.f("ix_workspaces_organization_id"), "workspaces", ["organization_id"], unique=False)
    op.create_table(
        "organization_memberships",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "user_id", name="uq_org_membership_org_user"),
    )
    op.create_index(op.f("ix_organization_memberships_organization_id"), "organization_memberships", ["organization_id"], unique=False)
    op.create_index(op.f("ix_organization_memberships_role"), "organization_memberships", ["role"], unique=False)
    op.create_index(op.f("ix_organization_memberships_user_id"), "organization_memberships", ["user_id"], unique=False)
    op.create_table(
        "organization_invites",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("invited_by_user_id", sa.String(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["invited_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organization_invites_email"), "organization_invites", ["email"], unique=False)
    op.create_index(op.f("ix_organization_invites_invited_by_user_id"), "organization_invites", ["invited_by_user_id"], unique=False)
    op.create_index(op.f("ix_organization_invites_organization_id"), "organization_invites", ["organization_id"], unique=False)
    op.create_table(
        "integration_connections",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "provider", name="uq_integration_org_provider"),
    )
    op.create_index(op.f("ix_integration_connections_organization_id"), "integration_connections", ["organization_id"], unique=False)
    op.create_index(op.f("ix_integration_connections_provider"), "integration_connections", ["provider"], unique=False)
    op.create_index(op.f("ix_integration_connections_status"), "integration_connections", ["status"], unique=False)
    op.create_table(
        "usage_events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("organization_id", sa.String(), nullable=False),
        sa.Column("workspace_id", sa.String(), nullable=True),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("billable", sa.Boolean(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_usage_events_event_type"), "usage_events", ["event_type"], unique=False)
    op.create_index(op.f("ix_usage_events_organization_id"), "usage_events", ["organization_id"], unique=False)
    op.create_index(op.f("ix_usage_events_workspace_id"), "usage_events", ["workspace_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_usage_events_workspace_id"), table_name="usage_events")
    op.drop_index(op.f("ix_usage_events_organization_id"), table_name="usage_events")
    op.drop_index(op.f("ix_usage_events_event_type"), table_name="usage_events")
    op.drop_table("usage_events")
    op.drop_index(op.f("ix_integration_connections_status"), table_name="integration_connections")
    op.drop_index(op.f("ix_integration_connections_provider"), table_name="integration_connections")
    op.drop_index(op.f("ix_integration_connections_organization_id"), table_name="integration_connections")
    op.drop_table("integration_connections")
    op.drop_index(op.f("ix_organization_invites_organization_id"), table_name="organization_invites")
    op.drop_index(op.f("ix_organization_invites_invited_by_user_id"), table_name="organization_invites")
    op.drop_index(op.f("ix_organization_invites_email"), table_name="organization_invites")
    op.drop_table("organization_invites")
    op.drop_index(op.f("ix_organization_memberships_user_id"), table_name="organization_memberships")
    op.drop_index(op.f("ix_organization_memberships_role"), table_name="organization_memberships")
    op.drop_index(op.f("ix_organization_memberships_organization_id"), table_name="organization_memberships")
    op.drop_table("organization_memberships")
    op.drop_index(op.f("ix_workspaces_organization_id"), table_name="workspaces")
    op.drop_constraint("fk_workspaces_organization_id", "workspaces", type_="foreignkey")
    op.drop_column("workspaces", "organization_id")
    op.drop_index(op.f("ix_organizations_status"), table_name="organizations")
    op.drop_index(op.f("ix_organizations_slug"), table_name="organizations")
    op.drop_index(op.f("ix_organizations_owner_user_id"), table_name="organizations")
    op.drop_table("organizations")

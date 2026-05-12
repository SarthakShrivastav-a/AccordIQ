import asyncio
import uuid

from fastapi.testclient import TestClient

from accordiq.db.session import AsyncSessionLocal
from accordiq.main import app
from accordiq.models.auth import User
from accordiq.models.organization import Organization, OrganizationMembership, UsageEvent
from tests.helpers import seed_member


def test_orgs_require_auth():
    client = TestClient(app)
    assert client.get("/api/orgs").status_code == 401


def test_create_org_creates_owner_workspace_and_integrations():
    headers, _, _ = asyncio.run(seed_member())
    with TestClient(app) as client:
        response = client.post("/api/orgs", json={"name": "Acme Product"}, headers=headers)
        assert response.status_code == 200
        org_id = response.json()["id"]
        orgs = client.get("/api/orgs", headers=headers)
        integrations = client.get(f"/api/orgs/{org_id}/integrations", headers=headers)
    assert any(item["id"] == org_id for item in orgs.json())
    assert {item["provider"] for item in integrations.json()} == {"notion", "slack"}


def test_org_invite_and_usage_are_db_backed():
    headers, _, _ = asyncio.run(seed_member())
    with TestClient(app) as client:
        org_id = client.get("/api/orgs", headers=headers).json()[0]["id"]
        invite = client.post(f"/api/orgs/{org_id}/invites", json={"email": "teammate@example.com", "role": "viewer"}, headers=headers)
    assert invite.status_code == 200
    assert invite.json()["email"] == "teammate@example.com"

    async def seed_usage():
        async with AsyncSessionLocal() as session:
            session.add(UsageEvent(organization_id=org_id, event_type="captured_message", quantity=7, metadata_json={}))
            await session.commit()

    asyncio.run(seed_usage())
    with TestClient(app) as client:
        usage = client.get(f"/api/orgs/{org_id}/usage", headers=headers)
    assert usage.status_code == 200
    assert usage.json()["captured_messages"] == 7


def test_cross_org_access_is_forbidden():
    headers, _, _ = asyncio.run(seed_member())

    async def seed_other_org():
        async with AsyncSessionLocal() as session:
            suffix = uuid.uuid4().hex[:8]
            user = User(email=f"other-owner-{suffix}@example.com", google_sub=f"other-owner-{suffix}", status="active")
            session.add(user)
            await session.flush()
            org = Organization(name="Other", slug=f"other-secure-{suffix}", owner_user_id=user.id, settings_json={})
            session.add(org)
            await session.flush()
            session.add(OrganizationMembership(organization_id=org.id, user_id=user.id, role="owner"))
            await session.commit()
            return org.id

    other_org_id = asyncio.run(seed_other_org())
    with TestClient(app) as client:
        response = client.get(f"/api/orgs/{other_org_id}", headers=headers)
    assert response.status_code == 403

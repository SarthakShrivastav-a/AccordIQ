import asyncio

from fastapi.testclient import TestClient

from accordiq.db.session import AsyncSessionLocal
from accordiq.main import app
from accordiq.models.entity import Entity
from accordiq.models.job import JobRecord
from accordiq.models.message import SlackMessage
from tests.helpers import seed_member


def test_admin_requires_auth():
    client = TestClient(app)
    response = client.get("/api/admin/workspaces")
    assert response.status_code == 401


def test_admin_workspace_returns_real_membership():
    headers, workspace_id, _ = asyncio.run(seed_member())
    with TestClient(app) as client:
        response = client.get(f"/api/admin/workspaces/{workspace_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["workspace_id"] == workspace_id


def test_admin_entities_jobs_metrics_are_db_backed():
    headers, workspace_id, _ = asyncio.run(seed_member())

    async def seed_rows():
        async with AsyncSessionLocal() as session:
            message = SlackMessage(workspace_id=workspace_id, channel_id="C1", user_id="U1", message_ts="1.0", raw_text="ship billing change", redacted_text="ship billing change", permalink="https://slack.test/1")
            entity = Entity(accordiq_id=f"acc-{workspace_id}", workspace_id=workspace_id, source_message_id="1.0", entity_type="decision", title="Ship billing change", status="review", confidence=0.9, payload_json={"source": {"permalink": "https://slack.test/1"}})
            job = JobRecord(workspace_id=workspace_id, job_type="capture", status="failed", payload_json={}, error="boom")
            session.add_all([message, entity, job])
            await session.commit()

    asyncio.run(seed_rows())
    with TestClient(app) as client:
        entities = client.get(f"/api/admin/workspaces/{workspace_id}/entities", headers=headers)
        jobs = client.get(f"/api/admin/workspaces/{workspace_id}/jobs", headers=headers)
        metrics = client.get(f"/api/admin/workspaces/{workspace_id}/metrics", headers=headers)
    assert entities.status_code == 200
    assert entities.json()["items"][0]["title"] == "Ship billing change"
    assert jobs.json()["items"][0]["status"] == "failed"
    assert metrics.json()["captured_messages"] == 1
    assert metrics.json()["entities"] == 1

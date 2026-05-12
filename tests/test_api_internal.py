import asyncio

from fastapi.testclient import TestClient

from accordiq.db.session import AsyncSessionLocal
from accordiq.main import app
from accordiq.models.message import SlackMessage
from tests.helpers import seed_member


def test_query_endpoint_requires_auth():
    client = TestClient(app)
    response = client.post("/api/query", json={"workspace_id": "W1", "user_id": "U1", "text": "what did we decide"})
    assert response.status_code == 401


def test_query_endpoint_uses_real_captured_messages():
    headers, workspace_id, _ = asyncio.run(seed_member())

    async def seed_message():
        async with AsyncSessionLocal() as session:
            session.add(SlackMessage(workspace_id=workspace_id, channel_id="C1", user_id="U1", message_ts="1.0", raw_text="we decided to keep notion as source of truth", redacted_text="we decided to keep notion as source of truth", permalink="https://slack.test/source"))
            await session.commit()

    asyncio.run(seed_message())
    with TestClient(app) as client:
        response = client.post("/api/query", json={"workspace_id": workspace_id, "user_id": "ignored", "text": "notion source truth"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["grounded"] is True
    assert response.json()["citations"][0]["url"] == "https://slack.test/source"

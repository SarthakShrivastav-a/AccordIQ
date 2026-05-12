from fastapi.testclient import TestClient
from accordiq.main import app

def test_url_verification(monkeypatch):
    monkeypatch.setenv("ACCORDIQ_SKIP_SLACK_SIGNATURE", "1")
    client = TestClient(app)
    response = client.post("/slack/events", json={"type": "url_verification", "challenge": "abc"})
    assert response.json()["challenge"] == "abc"

from fastapi.testclient import TestClient
from accordiq.main import app

def test_query_endpoint():
    client = TestClient(app)
    response = client.post("/api/query", json={"workspace_id": "W1", "user_id": "U1", "text": "what did we decide"})
    assert response.status_code == 200
    assert response.json()["grounded"] is True

from fastapi.testclient import TestClient
from accordiq.main import app

def test_admin_workspace():
    client = TestClient(app)
    response = client.get("/api/admin/workspaces/W1")
    assert response.status_code == 200
    assert response.json()["workspace_id"] == "W1"

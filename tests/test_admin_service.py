from accordiq.services.admin_service import AdminService

def test_admin_metrics_shape():
    metrics = AdminService().metrics("W1")
    assert metrics["workspace_id"] == "W1"

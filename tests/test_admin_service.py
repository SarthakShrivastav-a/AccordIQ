import pytest

from accordiq.db.session import AsyncSessionLocal
from accordiq.services.admin_service import AdminService
from tests.helpers import seed_member


@pytest.mark.asyncio
async def test_admin_metrics_shape():
    _, workspace_id, _ = await seed_member()
    async with AsyncSessionLocal() as session:
        metrics = await AdminService().metrics(session, workspace_id)
    assert metrics["workspace_id"] == workspace_id
    assert metrics["captured_messages"] == 0

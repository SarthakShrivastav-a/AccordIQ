import pytest
from accordiq.adapters.notion_client import NotionClient

@pytest.mark.asyncio
async def test_notion_upsert_stub():
    client = NotionClient()
    page = await client.upsert_entity("ds", "acc_1", {"Title": "Ship"})
    assert page["page_id"] == "page_acc_1"

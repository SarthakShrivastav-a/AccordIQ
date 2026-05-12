import pytest
from accordiq.workers.capture_worker import process_capture_job
from accordiq.workers.query_worker import process_query_job

@pytest.mark.asyncio
async def test_capture_worker():
    result = await process_capture_job({"workspace_id": "W", "text": "I will ship", "source": {"message_ts": "1"}})
    assert result["entities"]

@pytest.mark.asyncio
async def test_query_worker():
    result = await process_query_job({"workspace_id": "W", "user_id": "U", "text": "what did we decide"})
    assert result["grounded"]

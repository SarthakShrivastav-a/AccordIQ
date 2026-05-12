import pytest
from accordiq.adapters.queue import QueueStub

@pytest.mark.asyncio
async def test_queue_stub():
    queue = QueueStub()
    await queue.enqueue("capture", {"id": 1})
    assert queue.jobs[0]["job_type"] == "capture"

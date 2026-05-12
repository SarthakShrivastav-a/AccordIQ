from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class QueueStub:
    jobs: list[dict] = field(default_factory=list)

    async def enqueue(self, job_type: str, payload: dict) -> dict:
        job = {"job_type": job_type, "payload": payload}
        self.jobs.append(job)
        return job

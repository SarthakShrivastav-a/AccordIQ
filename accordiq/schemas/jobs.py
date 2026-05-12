from pydantic import BaseModel, Field

class JobEnvelope(BaseModel):
    job_type: str
    workspace_id: str | None = None
    payload: dict = Field(default_factory=dict)
    idempotency_key: str | None = None

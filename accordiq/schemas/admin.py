from pydantic import BaseModel, Field

class WorkspaceSettingsUpdate(BaseModel):
    capture_enabled: bool | None = None
    retention_days: int | None = None
    channel_mode: str | None = None
    redaction_patterns: list[str] | None = None

class ReviewUpdate(BaseModel):
    status: str = Field(pattern="^(active|review|ignored|done)$")
    reviewer_id: str | None = None
    note: str | None = None

class RetryJobRequest(BaseModel):
    reason: str | None = None

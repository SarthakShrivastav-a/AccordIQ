from pydantic import BaseModel, Field

class SourceRef(BaseModel):
    workspace_id: str
    channel_id: str
    message_ts: str
    permalink: str | None = None

class EntityPayload(BaseModel):
    entity_type: str
    title: str
    owner_slack_id: str | None = None
    due_text: str | None = None
    status: str = "review"
    confidence: float = Field(ge=0, le=1)
    source: SourceRef
    metadata: dict = Field(default_factory=dict)

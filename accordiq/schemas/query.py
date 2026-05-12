from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    workspace_id: str
    user_id: str
    text: str
    channel_id: str | None = None

class Citation(BaseModel):
    title: str
    url: str
    preview: str

class QueryResponse(BaseModel):
    answer: str
    intent: str
    citations: list[Citation] = Field(default_factory=list)
    grounded: bool

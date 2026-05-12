from pydantic import BaseModel, Field

class SlackEventEnvelope(BaseModel):
    token: str | None = None
    challenge: str | None = None
    type: str
    event_id: str | None = None
    team_id: str | None = None
    event: dict = Field(default_factory=dict)

class SlackCommand(BaseModel):
    team_id: str
    user_id: str
    channel_id: str
    command: str
    text: str
    response_url: str | None = None

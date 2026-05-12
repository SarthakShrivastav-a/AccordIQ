from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class OrganizationRead(BaseModel):
    id: str
    name: str
    slug: str
    role: str
    status: str
    onboarding_complete: bool


class InviteCreate(BaseModel):
    email: str
    role: str = "viewer"


class InviteRead(BaseModel):
    id: str
    organization_id: str
    email: str
    role: str
    accepted: bool


class OrganizationMemberRead(BaseModel):
    user_id: str
    email: str
    name: str | None
    role: str


class IntegrationRead(BaseModel):
    provider: str
    status: str
    external_id: str | None = None
    metadata: dict = Field(default_factory=dict)


class CapturePolicyRead(BaseModel):
    organization_id: str
    channel_mode: str
    retention_days: int
    ignored_channels: list[str]
    allowed_channels: list[str]


class CapturePolicyUpdate(BaseModel):
    channel_mode: str | None = None
    retention_days: int | None = None
    ignored_channels: list[str] | None = None
    allowed_channels: list[str] | None = None


class UsageRead(BaseModel):
    organization_id: str
    captured_messages: int
    extracted_entities: int
    grounded_queries: int
    notion_syncs: int

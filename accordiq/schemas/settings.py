from pydantic import BaseModel

class CapturePolicySettings(BaseModel):
    channel_mode: str = "invited_channels"
    retention_days: int = 365
    ignored_channels: list[str] = []
    allowed_channels: list[str] = []

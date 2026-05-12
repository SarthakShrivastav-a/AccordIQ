import uuid
from sqlalchemy import Boolean, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from accordiq.db.base import Base
from accordiq.models.mixins import TimestampMixin

class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str | None] = mapped_column(String, ForeignKey("organizations.id"), index=True, nullable=True)
    slack_team_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    capture_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    settings_json: Mapped[dict] = mapped_column(JSON, default=dict)

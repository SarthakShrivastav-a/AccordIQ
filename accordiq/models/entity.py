import uuid
from sqlalchemy import Float, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from accordiq.db.base import Base
from accordiq.models.mixins import TimestampMixin

class Entity(TimestampMixin, Base):
    __tablename__ = "entities"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    accordiq_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    workspace_id: Mapped[str] = mapped_column(String, index=True)
    source_message_id: Mapped[str] = mapped_column(String, index=True)
    entity_type: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="review")
    confidence: Mapped[float] = mapped_column(Float, default=0)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

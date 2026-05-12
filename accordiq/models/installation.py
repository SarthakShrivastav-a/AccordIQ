import uuid
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from accordiq.db.base import Base
from accordiq.models.mixins import TimestampMixin

class Installation(TimestampMixin, Base):
    __tablename__ = "installations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id: Mapped[str] = mapped_column(String, index=True)
    slack_bot_token_ciphertext: Mapped[str | None] = mapped_column(Text, nullable=True)
    notion_token_ciphertext: Mapped[str | None] = mapped_column(Text, nullable=True)
    notion_data_source_id: Mapped[str | None] = mapped_column(String, nullable=True)

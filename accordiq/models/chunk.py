import uuid
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from accordiq.db.base import Base
from accordiq.models.mixins import TimestampMixin

class MessageChunk(TimestampMixin, Base):
    __tablename__ = "message_chunks"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id: Mapped[str] = mapped_column(String, index=True)
    message_id: Mapped[str] = mapped_column(String, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    embedding_ref: Mapped[str | None] = mapped_column(String, nullable=True)

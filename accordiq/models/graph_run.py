import uuid
from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from accordiq.db.base import Base
from accordiq.models.mixins import TimestampMixin

class GraphRun(TimestampMixin, Base):
    __tablename__ = "graph_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id: Mapped[str] = mapped_column(String, index=True)
    graph_name: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, default="started")
    state_json: Mapped[dict] = mapped_column(JSON, default=dict)

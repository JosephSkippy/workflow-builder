import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    nodes_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    @property
    def nodes(self) -> list[dict]:
        return json.loads(self.nodes_json)

    @nodes.setter
    def nodes(self, value: list[dict]) -> None:
        self.nodes_json = json.dumps(value)

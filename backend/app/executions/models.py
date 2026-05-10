from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Execution(Base):
    __tablename__ = "execution"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    workflow_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="running")
    steps_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def steps(self) -> list[dict]:
        import json
        return json.loads(self.steps_json)

    @steps.setter
    def steps(self, value: list[dict]) -> None:
        import json
        self.steps_json = json.dumps(value)

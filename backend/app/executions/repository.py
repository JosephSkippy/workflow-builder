from sqlalchemy.orm import Session

from app.executions.models import Execution


class ExecutionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, execution_id: str) -> Execution | None:
        return self.db.get(Execution, execution_id)

    def list_by_workflow(self, workflow_id: str) -> list[Execution]:
        return (
            self.db.query(Execution)
            .filter(Execution.workflow_id == workflow_id)
            .order_by(Execution.created_at.desc())
            .all()
        )

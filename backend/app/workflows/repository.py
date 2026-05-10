from sqlalchemy.orm import Session

from app.workflows.models import Workflow
from app.workflows.schemas import WorkflowPayload


class WorkflowRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert(self, workflow_id: str, payload: WorkflowPayload) -> Workflow:
        """Create or replace a workflow."""
        workflow = Workflow(id=workflow_id, name=payload.name)
        workflow.nodes = [node.model_dump() for node in payload.nodes]
        workflow = self.db.merge(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def get_by_id(self, workflow_id: str) -> Workflow | None:
        return self.db.get(Workflow, workflow_id)

    def list_all(self) -> list[Workflow]:
        return self.db.query(Workflow).order_by(Workflow.created_at.desc()).all()

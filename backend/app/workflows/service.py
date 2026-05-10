from app.workflows.models import Workflow
from app.workflows.repository import WorkflowRepository
from app.workflows.schemas import WorkflowPayload
from app.workflows.validator import ValidationError, validate_workflow


class WorkflowService:
    def __init__(self, repo: WorkflowRepository) -> None:
        self.repo = repo

    def save(self, workflow_id: str, payload: WorkflowPayload) -> Workflow | list[ValidationError]:
        """Validate and persist. Returns Workflow on success, list of errors on failure."""
        errors = validate_workflow(payload)
        if errors:
            return errors
        return self.repo.upsert(workflow_id, payload)

    def get(self, workflow_id: str) -> Workflow | None:
        return self.repo.get_by_id(workflow_id)

    def list_all(self) -> list[Workflow]:
        return self.repo.list_all()

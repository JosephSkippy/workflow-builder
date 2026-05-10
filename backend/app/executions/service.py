from app.core.database import SessionLocal
from app.executions.executor import WorkflowExecutor
from app.executions.models import Execution
from app.executions.repository import ExecutionRepository
from app.workflows.models import Workflow
from app.workflows.repository import WorkflowRepository


def run_execution_background(execution_id: str, workflow_id: str) -> None:
    """Background task — uses its own DB session outside request lifecycle.

    Runs in-process via FastAPI BackgroundTasks. No retry, no crash recovery.
    Production: replace with SQS + ECS worker for durable
    execution with automatic retry and independent scaling.
    """
    db = SessionLocal()
    try:
        workflow = WorkflowRepository(db).get_by_id(workflow_id)
        if workflow:
            WorkflowExecutor(db).run(execution_id, workflow)
    finally:
        db.close()


class ExecutionService:
    def __init__(
        self,
        repo: ExecutionRepository,
        workflow_repo: WorkflowRepository,
        executor: WorkflowExecutor,
    ) -> None:
        self.repo = repo
        self.workflow_repo = workflow_repo
        self.executor = executor

    def start(self, workflow_id: str) -> tuple[Execution, Workflow]:
        """Validate workflow exists and create an execution record.

        Returns the execution and workflow so the router can schedule the
        background task (which needs request-scoped BackgroundTasks).
        """
        workflow = self.workflow_repo.get_by_id(workflow_id)
        if workflow is None:
            raise WorkflowNotFoundError(workflow_id)
        execution = self.executor.create(workflow)
        return execution, workflow

    def get(self, execution_id: str) -> Execution | None:
        return self.repo.get_by_id(execution_id)

    def list_by_workflow(self, workflow_id: str) -> list[Execution]:
        return self.repo.list_by_workflow(workflow_id)


class WorkflowNotFoundError(Exception):
    def __init__(self, workflow_id: str) -> None:
        self.workflow_id = workflow_id
        super().__init__(f"Workflow {workflow_id} not found")

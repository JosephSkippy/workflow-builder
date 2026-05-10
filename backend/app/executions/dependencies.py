from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.executions.executor import WorkflowExecutor
from app.executions.repository import ExecutionRepository
from app.executions.service import ExecutionService
from app.workflows.dependencies import get_workflow_repository
from app.workflows.repository import WorkflowRepository


def get_execution_repository(db: Session = Depends(get_db)) -> ExecutionRepository:
    return ExecutionRepository(db)


def get_workflow_executor(db: Session = Depends(get_db)) -> WorkflowExecutor:
    return WorkflowExecutor(db)


def get_execution_service(
    repo: ExecutionRepository = Depends(get_execution_repository),
    workflow_repo: WorkflowRepository = Depends(get_workflow_repository),
    executor: WorkflowExecutor = Depends(get_workflow_executor),
) -> ExecutionService:
    return ExecutionService(repo, workflow_repo, executor)

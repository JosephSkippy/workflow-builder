from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.workflows.repository import WorkflowRepository
from app.workflows.service import WorkflowService


def get_workflow_repository(db: Session = Depends(get_db)) -> WorkflowRepository:
    return WorkflowRepository(db)


def get_workflow_service(
    repo: WorkflowRepository = Depends(get_workflow_repository),
) -> WorkflowService:
    return WorkflowService(repo)

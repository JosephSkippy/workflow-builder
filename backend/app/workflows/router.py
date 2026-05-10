from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.workflows.dependencies import get_workflow_service
from app.workflows.models import Workflow
from app.workflows.schemas import WorkflowPayload, WorkflowResponse
from app.workflows.service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["workflows"])


def _to_response(workflow: Workflow) -> WorkflowResponse:
    return WorkflowResponse(id=workflow.id, name=workflow.name, nodes=workflow.nodes)


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def save_workflow(
    workflow_id: UUID,
    payload: WorkflowPayload,
    service: WorkflowService = Depends(get_workflow_service),
):
    result = service.save(str(workflow_id), payload)
    if isinstance(result, list):
        raise HTTPException(status_code=422, detail=result[0].message)
    return _to_response(result)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_by_id(
    workflow_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    workflow = service.get(str(workflow_id))
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _to_response(workflow)


@router.get("/", response_model=list[WorkflowResponse])
async def list_all_workflows(
    service: WorkflowService = Depends(get_workflow_service),
):
    return [_to_response(w) for w in service.list_all()]

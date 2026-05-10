from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.executions.dependencies import get_execution_service
from app.executions.schemas import ExecutionResponse, ExecutionStarted, ExecutionSummary, StepResult
from app.executions.service import ExecutionService, WorkflowNotFoundError, run_execution_background

router = APIRouter(prefix="/executions", tags=["executions"])


@router.get("/workflow/{workflow_id}", response_model=list[ExecutionSummary])
def list_executions(
    workflow_id: str,
    service: ExecutionService = Depends(get_execution_service),
):
    executions = service.list_by_workflow(workflow_id)
    return [
        ExecutionSummary(
            execution_id=e.id,
            status=e.status,
            created_at=e.created_at.isoformat(),
        )
        for e in executions
    ]


@router.post("/{workflow_id}", response_model=ExecutionStarted)
def start_execution(
    workflow_id: str,
    background_tasks: BackgroundTasks,
    service: ExecutionService = Depends(get_execution_service),
):
    try:
        execution, workflow = service.start(workflow_id)
    except WorkflowNotFoundError:
        raise HTTPException(status_code=404, detail="Workflow not found")

    background_tasks.add_task(run_execution_background, execution.id, workflow.id)

    return ExecutionStarted(execution_id=execution.id, status=execution.status)


@router.get("/{execution_id}", response_model=ExecutionResponse)
def get_execution(
    execution_id: str,
    service: ExecutionService = Depends(get_execution_service),
):
    execution = service.get(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return ExecutionResponse(
        execution_id=execution.id,
        workflow_id=execution.workflow_id,
        status=execution.status,
        steps=[StepResult(**s) for s in execution.steps],
    )

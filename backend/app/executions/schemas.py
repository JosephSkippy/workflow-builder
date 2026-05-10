from typing import Any

from pydantic import BaseModel


class StepResult(BaseModel):
    node_id: str
    node_type: str
    output: Any


class ExecutionStarted(BaseModel):
    execution_id: str
    status: str


class ExecutionResponse(BaseModel):
    execution_id: str
    workflow_id: str
    status: str
    steps: list[StepResult]


class ExecutionSummary(BaseModel):
    execution_id: str
    status: str
    created_at: str

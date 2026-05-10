from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator, model_validator


class InputVariable(BaseModel):
    name: str
    value: str


class InputConfig(BaseModel):
    variables: list[InputVariable]


class ToolConfig(BaseModel):
    tool_name: str
    inputs: dict[str, str]
    output_variable: str


class PromptConfig(BaseModel):
    template: str


class WorkflowNode(BaseModel):
    id: str
    type: Literal["input", "tool", "prompt"]
    order: int
    config: InputConfig | ToolConfig | PromptConfig

    @model_validator(mode="before")
    @classmethod
    def parse_config_by_type(cls, data: dict) -> dict:
        """Parse config dict into the correct model based on node type."""
        if isinstance(data, dict) and isinstance(data.get("config"), dict):
            node_type = data.get("type")
            config = data["config"]
            if node_type == "input":
                data["config"] = InputConfig(**config)
            elif node_type == "tool":
                data["config"] = ToolConfig(**config)
            elif node_type == "prompt":
                data["config"] = PromptConfig(**config)
        return data


class WorkflowPayload(BaseModel):
    name: str
    nodes: list[WorkflowNode]

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Workflow name cannot be empty")
        return v

    @field_validator("nodes")
    @classmethod
    def at_least_one_node(cls, v: list[WorkflowNode]) -> list[WorkflowNode]:
        if not v:
            raise ValueError("Workflow must have at least one node")
        return v


class WorkflowResponse(BaseModel):
    id: str
    name: str
    nodes: list[WorkflowNode]

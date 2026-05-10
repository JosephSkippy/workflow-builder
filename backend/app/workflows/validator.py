"""Workflow validation — checks variable references resolve to preceding nodes."""

from __future__ import annotations

import re

from app.tools.registry import TOOL_REGISTRY
from app.workflows.schemas import (
    InputConfig,
    PromptConfig,
    ToolConfig,
    WorkflowNode,
    WorkflowPayload,
)

_VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


class ValidationError:
    def __init__(self, node_id: str, field: str, message: str) -> None:
        self.node_id = node_id
        self.field = field
        self.message = message

    def to_dict(self) -> dict:
        return {"node_id": self.node_id, "field": self.field, "message": self.message}


def validate_workflow(payload: WorkflowPayload) -> list[ValidationError]:
    """Validate the full workflow. Returns a list of errors (empty = valid)."""
    errors: list[ValidationError] = []
    sorted_nodes = sorted(payload.nodes, key=lambda n: n.order)

    for node in sorted_nodes:
        available = _available_variables(sorted_nodes, node.order)

        if node.type == "input":
            errors.extend(_validate_input_node(node))
        elif node.type == "tool":
            errors.extend(_validate_tool_node(node, available))
        elif node.type == "prompt":
            errors.extend(_validate_prompt_node(node, available))

    return errors


def _available_variables(sorted_nodes: list[WorkflowNode], current_order: int) -> set[str]:
    """Collect variable names defined by nodes preceding the current order."""
    names: set[str] = set()
    for node in sorted_nodes:
        if node.order >= current_order:
            break
        if node.type == "input":
            config = node.config
            if isinstance(config, InputConfig):
                for v in config.variables:
                    if v.name:
                        names.add(v.name)
        elif node.type == "tool":
            config = node.config
            if isinstance(config, ToolConfig) and config.output_variable:
                names.add(config.output_variable)
    return names


def _validate_input_node(node: WorkflowNode) -> list[ValidationError]:
    errors: list[ValidationError] = []
    config = node.config
    if not isinstance(config, InputConfig):
        errors.append(ValidationError(node.id, "config", "Invalid config for input node"))
        return errors

    if not config.variables:
        errors.append(ValidationError(node.id, "variables", "Input node must have at least one variable"))
        return errors

    for i, var in enumerate(config.variables):
        if not var.name.strip():
            errors.append(ValidationError(node.id, f"variables[{i}].name", "Variable name cannot be empty"))
        if not var.value.strip():
            errors.append(ValidationError(node.id, f"variables[{i}].value", "Variable value cannot be empty"))

    return errors


def _validate_tool_node(node: WorkflowNode, available: set[str]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    config = node.config
    if not isinstance(config, ToolConfig):
        errors.append(ValidationError(node.id, "config", "Invalid config for tool node"))
        return errors

    # Check tool exists
    tool_def = TOOL_REGISTRY.get(config.tool_name)
    if not tool_def:
        errors.append(ValidationError(node.id, "tool_name", f"Unknown tool: {config.tool_name}"))
        return errors

    # Check required inputs are filled
    for tool_input in tool_def.inputs:
        value = config.inputs.get(tool_input.name, "")
        if tool_input.required and not value.strip():
            errors.append(
                ValidationError(node.id, f"inputs.{tool_input.name}", f"Required input '{tool_input.name}' is empty")
            )
            continue
        # Check variable references resolve
        if value:
            _check_references(node.id, f"inputs.{tool_input.name}", value, available, errors)

    # Check output_variable is set
    if not config.output_variable.strip():
        errors.append(ValidationError(node.id, "output_variable", "Output variable name cannot be empty"))

    return errors


def _validate_prompt_node(node: WorkflowNode, available: set[str]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    config = node.config
    if not isinstance(config, PromptConfig):
        errors.append(ValidationError(node.id, "config", "Invalid config for prompt node"))
        return errors

    if not config.template.strip():
        errors.append(ValidationError(node.id, "template", "Prompt template cannot be empty"))
        return errors

    _check_references(node.id, "template", config.template, available, errors)
    return errors


def _check_references(
    node_id: str,
    field: str,
    value: str,
    available: set[str],
    errors: list[ValidationError],
) -> None:
    """Find all {{var}} references in a value and check they resolve."""
    for match in _VAR_PATTERN.finditer(value):
        var_name = match.group(1)
        if var_name not in available:
            errors.append(
                ValidationError(
                    node_id,
                    field,
                    f"Variable '{{{{{var_name}}}}}' does not resolve to any preceding node",
                )
            )

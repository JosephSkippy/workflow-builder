"""Tests for workflow validation — variable resolution, empty fields, unknown tools."""

import pytest

from app.workflows.schemas import WorkflowPayload
from app.workflows.validator import validate_workflow


def _payload(nodes: list[dict]) -> WorkflowPayload:
    return WorkflowPayload(name="test", nodes=nodes)


def _input_node(order: int, variables: list[dict], node_id: str = "input-1") -> dict:
    return {"id": node_id, "type": "input", "order": order, "config": {"variables": variables}}


def _tool_node(
    order: int,
    tool_name: str = "query_subway_db",
    inputs: dict | None = None,
    output_variable: str = "db_results",
    node_id: str = "tool-1",
) -> dict:
    return {
        "id": node_id,
        "type": "tool",
        "order": order,
        "config": {
            "tool_name": tool_name,
            "inputs": inputs or {"station": "{{station}}"},
            "output_variable": output_variable,
        },
    }


def _prompt_node(order: int, template: str, node_id: str = "prompt-1") -> dict:
    return {"id": node_id, "type": "prompt", "order": order, "config": {"template": template}}


# ---------------------------------------------------------------------------
# 1. Happy path: Input → Tool → Prompt — all references valid
# ---------------------------------------------------------------------------
class TestHappyPath:
    def test_valid_pipeline_no_errors(self):
        payload = _payload([
            _input_node(1, [{"name": "station", "value": "UNION STATION"}]),
            _tool_node(2, inputs={"station": "{{station}}"}, output_variable="db_results"),
            _prompt_node(3, "Summarize: {{db_results}}"),
        ])
        errors = validate_workflow(payload)
        assert errors == []


# ---------------------------------------------------------------------------
# 2. Tool node references a variable from a LATER node
# ---------------------------------------------------------------------------
class TestForwardReference:
    def test_tool_references_future_variable(self):
        payload = _payload([
            _tool_node(1, inputs={"station": "{{station}}"}, output_variable="db_results"),
            _input_node(2, [{"name": "station", "value": "UNION STATION"}]),
        ])
        errors = validate_workflow(payload)
        assert len(errors) == 1
        assert "station" in errors[0].message
        assert errors[0].node_id == "tool-1"


# ---------------------------------------------------------------------------
# 3. Prompt node references a variable that doesn't exist at all
# ---------------------------------------------------------------------------
class TestNonexistentVariable:
    def test_prompt_references_undefined_variable(self):
        payload = _payload([
            _input_node(1, [{"name": "station", "value": "UNION STATION"}]),
            _prompt_node(2, "Summarize: {{does_not_exist}}"),
        ])
        errors = validate_workflow(payload)
        assert len(errors) == 1
        assert "does_not_exist" in errors[0].message
        assert errors[0].node_id == "prompt-1"


# ---------------------------------------------------------------------------
# 4. Prompt node references a valid variable from preceding input node
# ---------------------------------------------------------------------------
class TestValidPromptReference:
    def test_prompt_references_preceding_input(self):
        payload = _payload([
            _input_node(1, [{"name": "station", "value": "UNION STATION"}]),
            _prompt_node(2, "Station is: {{station}}"),
        ])
        errors = validate_workflow(payload)
        assert errors == []


# ---------------------------------------------------------------------------
# 5. Reorder breaks a dependency — prompt used to be after tool, now before
# ---------------------------------------------------------------------------
class TestReorderBreaksDependency:
    def test_prompt_before_tool_breaks_reference(self):
        payload = _payload([
            _input_node(1, [{"name": "station", "value": "UNION STATION"}]),
            _prompt_node(2, "Summarize: {{db_results}}"),
            _tool_node(3, inputs={"station": "{{station}}"}, output_variable="db_results"),
        ])
        errors = validate_workflow(payload)
        assert len(errors) == 1
        assert "db_results" in errors[0].message
        assert errors[0].node_id == "prompt-1"


# ---------------------------------------------------------------------------
# 6. Input node with empty variable name
# ---------------------------------------------------------------------------
class TestEmptyVariableName:
    def test_empty_name_fails(self):
        payload = _payload([
            _input_node(1, [{"name": "", "value": "UNION STATION"}]),
        ])
        errors = validate_workflow(payload)
        assert any("name" in e.field and "empty" in e.message.lower() for e in errors)

    def test_whitespace_name_fails(self):
        payload = _payload([
            _input_node(1, [{"name": "   ", "value": "UNION STATION"}]),
        ])
        errors = validate_workflow(payload)
        assert any("name" in e.field and "empty" in e.message.lower() for e in errors)


# ---------------------------------------------------------------------------
# 7. Input node with empty variable value
# ---------------------------------------------------------------------------
class TestEmptyVariableValue:
    def test_empty_value_fails(self):
        payload = _payload([
            _input_node(1, [{"name": "station", "value": ""}]),
        ])
        errors = validate_workflow(payload)
        assert any("value" in e.field and "empty" in e.message.lower() for e in errors)

    def test_whitespace_value_fails(self):
        payload = _payload([
            _input_node(1, [{"name": "station", "value": "   "}]),
        ])
        errors = validate_workflow(payload)
        assert any("value" in e.field and "empty" in e.message.lower() for e in errors)


# ---------------------------------------------------------------------------
# 8. Tool node with unknown tool name
# ---------------------------------------------------------------------------
class TestUnknownTool:
    def test_nonexistent_tool_fails(self):
        payload = _payload([
            _tool_node(1, tool_name="this_tool_does_not_exist", inputs={}, output_variable="out"),
        ])
        errors = validate_workflow(payload)
        assert any("Unknown tool" in e.message for e in errors)
        assert errors[0].node_id == "tool-1"


# ---------------------------------------------------------------------------
# 9. Tool node with empty required input
# ---------------------------------------------------------------------------
class TestEmptyRequiredInput:
    def test_missing_required_input_fails(self):
        payload = _payload([
            _tool_node(1, inputs={"station": ""}, output_variable="out"),
        ])
        errors = validate_workflow(payload)
        assert any("station" in e.field and "empty" in e.message.lower() for e in errors)

    def test_whitespace_required_input_fails(self):
        payload = _payload([
            _tool_node(1, inputs={"station": "   "}, output_variable="out"),
        ])
        errors = validate_workflow(payload)
        assert any("station" in e.field and "empty" in e.message.lower() for e in errors)


# ---------------------------------------------------------------------------
# 10. Tool node with empty output_variable
# ---------------------------------------------------------------------------
class TestEmptyOutputVariable:
    def test_empty_output_variable_fails(self):
        payload = _payload([
            _tool_node(1, inputs={"station": "literal"}, output_variable=""),
        ])
        errors = validate_workflow(payload)
        assert any("output_variable" in e.field for e in errors)

    def test_whitespace_output_variable_fails(self):
        payload = _payload([
            _tool_node(1, inputs={"station": "literal"}, output_variable="   "),
        ])
        errors = validate_workflow(payload)
        assert any("output_variable" in e.field for e in errors)


# ---------------------------------------------------------------------------
# 11. Prompt node with empty template
# ---------------------------------------------------------------------------
class TestEmptyPromptTemplate:
    def test_empty_template_fails(self):
        payload = _payload([
            _prompt_node(1, ""),
        ])
        errors = validate_workflow(payload)
        assert any("template" in e.field for e in errors)

    def test_whitespace_template_fails(self):
        payload = _payload([
            _prompt_node(1, "   "),
        ])
        errors = validate_workflow(payload)
        assert any("template" in e.field for e in errors)

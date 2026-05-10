from sqlalchemy.orm import Session

from app.nodes.base import BaseNodeHandler
from app.shared.variable_resolver import resolve_variables
from app.tools.registry import TOOL_REGISTRY
from app.workflows.schemas import ToolConfig, WorkflowNode


class ToolHandler(BaseNodeHandler[ToolConfig]):
    def parse_config(self, node: WorkflowNode) -> ToolConfig:
        return ToolConfig.model_validate(node.config)

    def run(self, config: ToolConfig, context: dict[str, str], db: Session) -> str:
        resolved_inputs = {
            key: resolve_variables(value, context) for key, value in config.inputs.items()
        }

        tool_def = TOOL_REGISTRY[config.tool_name]
        result = tool_def.instance.run(resolved_inputs, db)

        context[config.output_variable] = result
        return result

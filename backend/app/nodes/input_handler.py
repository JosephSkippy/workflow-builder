import json

from sqlalchemy.orm import Session

from app.nodes.base import BaseNodeHandler
from app.workflows.schemas import InputConfig, WorkflowNode


class InputHandler(BaseNodeHandler[InputConfig]):
    def parse_config(self, node: WorkflowNode) -> InputConfig:
        return InputConfig.model_validate(node.config)

    def run(self, config: InputConfig, context: dict[str, str], db: Session) -> str:
        for var in config.variables:
            context[var.name] = var.value
        return json.dumps({var.name: var.value for var in config.variables})

import logging

from sqlalchemy.orm import Session

from app.integrations.openai.client import chat_completion
from app.nodes.base import BaseNodeHandler
from app.shared.variable_resolver import resolve_variables
from app.workflows.schemas import PromptConfig, WorkflowNode

logger = logging.getLogger(__name__)


class PromptHandler(BaseNodeHandler[PromptConfig]):
    def parse_config(self, node: WorkflowNode) -> PromptConfig:
        return PromptConfig.model_validate(node.config)

    def run(self, config: PromptConfig, context: dict[str, str], db: Session) -> str:
        prompt = resolve_variables(config.template, context)
        logger.info("=== PROMPT SENT TO LLM ===\n%s\n=== END PROMPT ===", prompt)
        return chat_completion(prompt)

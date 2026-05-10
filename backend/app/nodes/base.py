from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.workflows.schemas import WorkflowNode

ConfigT = TypeVar("ConfigT")


class BaseNodeHandler(ABC, Generic[ConfigT]):
    """Base class for node execution handlers.

    Parameterized by ConfigT so each handler declares its config type
    (e.g. BaseNodeHandler[InputConfig]). This lets the type checker
    verify config access without runtime casts or type: ignore.
    """

    @abstractmethod
    def parse_config(self, node: WorkflowNode) -> ConfigT:
        pass

    @abstractmethod
    def run(self, config: ConfigT, context: dict[str, str], db: Session) -> str:
        pass

    def execute(self, node: WorkflowNode, context: dict[str, str], db: Session) -> str:
        config = self.parse_config(node)
        return self.run(config, context, db)

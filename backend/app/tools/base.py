from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseTool(ABC):
    """Contract for all tools. Each tool takes inputs + db session, returns a string result."""

    @abstractmethod
    def run(self, inputs: dict[str, str], db: Session) -> str:
        pass

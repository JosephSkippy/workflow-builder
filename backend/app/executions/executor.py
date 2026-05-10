import logging
import uuid

from sqlalchemy.orm import Session

from app.executions.models import Execution
from app.executions.schemas import StepResult
from app.nodes.registry import NODE_REGISTRY
from app.workflows.models import Workflow
from app.workflows.schemas import WorkflowNode

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, workflow: Workflow) -> Execution:
        """Create execution record with 'running' status."""
        execution = Execution(
            id=str(uuid.uuid4()),
            workflow_id=workflow.id,
            status="running",
        )
        execution.steps = []
        self.db.add(execution)
        self.db.commit()
        return execution

    def run(self, execution_id: str, workflow: Workflow) -> None:
        """Execute workflow nodes — designed to run in background."""
        execution = self.db.query(Execution).filter(Execution.id == execution_id).first()
        if not execution:
            logger.error(f"Execution {execution_id} not found")
            return

        try:
            self._run(workflow, execution)
            execution.status = "completed"
        except Exception as e:
            execution.status = "failed"
            logger.error(f"Execution {execution.id} failed: {e}")
        finally:
            self.db.commit()

    def _run(self, workflow: Workflow, execution: Execution) -> None:
        nodes = sorted(
            [WorkflowNode(**n) for n in workflow.nodes], key=lambda n: n.order
        )
        context: dict[str, str] = {}
        steps: list[dict] = []

        for node in nodes:
            handler = NODE_REGISTRY[node.type]
            output = handler.execute(node, context, self.db)
            steps.append(StepResult(node_id=node.id, node_type=node.type, output=output).model_dump())
            execution.steps = steps
            self.db.commit()

        logger.debug(f"Execution {execution.id} complete: {len(steps)} steps")

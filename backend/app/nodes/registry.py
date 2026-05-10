from app.nodes.base import BaseNodeHandler
from app.nodes.input_handler import InputHandler
from app.nodes.prompt_handler import PromptHandler
from app.nodes.tool_handler import ToolHandler

NODE_REGISTRY: dict[str, BaseNodeHandler] = {
    "input": InputHandler(),
    "tool": ToolHandler(),
    "prompt": PromptHandler(),
}

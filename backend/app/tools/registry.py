"""Tool registry — single source of truth for available tools and their required inputs."""

from __future__ import annotations

from dataclasses import dataclass

from app.tools.base import BaseTool
from app.tools.subway_db_query.average_delay import AverageDelayTool
from app.tools.subway_db_query.tool import SubwayDbQueryTool


@dataclass(frozen=True)
class ToolInput:
    name: str
    required: bool = False


@dataclass(frozen=True)
class ToolDef:
    name: str
    description: str
    inputs: tuple[ToolInput, ...]
    instance: BaseTool


TOOL_REGISTRY: dict[str, ToolDef] = {}


def _register(*tools: ToolDef) -> None:
    for tool in tools:
        TOOL_REGISTRY[tool.name] = tool


_register(
    ToolDef(
        name="query_subway_db",
        description="Query Toronto subway delay records by station",
        inputs=(ToolInput(name="station", required=True),),
        instance=SubwayDbQueryTool(),
    ),
    ToolDef(
        name="calculate_average_delay",
        description="Calculate average delay in minutes for a station",
        inputs=(ToolInput(name="station", required=True),),
        instance=AverageDelayTool(),
    ),
)

from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Protocol

from pydantic import BaseModel


class ModelAdapter(Protocol):
    async def decide(self, messages: list[dict[str, str]], tools: list[dict[str, Any]]) -> dict[str, Any]: ...


ToolFn = Callable[..., Awaitable[Any]]


@dataclass
class Tool:
    name: str
    description: str
    schema: type[BaseModel]
    fn: ToolFn

    def declaration(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description,
                "parameters": self.schema.model_json_schema()}


class ToolError(Exception):
    """A safe, user-facing tool failure."""


class ToolExecutor:
    def __init__(self, tools: list[Tool], timeout: float = 5.0) -> None:
        self.tools = {tool.name: tool for tool in tools}
        self.timeout = timeout

    async def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self.tools.get(name)
        if tool is None:
            raise ToolError(f"unknown tool: {name}")
        try:
            parsed = tool.schema.model_validate(arguments)
        except Exception as exc:
            raise ToolError(f"invalid arguments for {name}: {exc}") from exc
        try:
            return await asyncio.wait_for(tool.fn(**parsed.model_dump()), timeout=self.timeout)
        except asyncio.TimeoutError as exc:
            raise ToolError(f"tool timed out: {name}") from exc
        except ToolError:
            raise
        except Exception as exc:
            raise ToolError(f"tool failed: {name}: {exc}") from exc


async def run_agent_loop(model: ModelAdapter, user_input: str, executor: ToolExecutor,
                         max_steps: int = 8) -> str:
    """Small framework-free loop used in week 1 and as a reference implementation."""
    messages = [{"role": "user", "content": user_input}]
    for _ in range(max_steps):
        result = await model.decide(messages, [t.declaration() for t in executor.tools.values()])
        if result.get("type") == "final":
            return str(result.get("content", ""))
        if result.get("type") != "tool_call":
            raise ToolError("model returned an invalid decision")
        name, args = result.get("name"), result.get("arguments", {})
        try:
            output = await executor.execute(name, args)
            messages.append({"role": "tool", "content": json.dumps(output, default=str)})
        except ToolError as exc:
            messages.append({"role": "tool", "content": json.dumps({"error": str(exc)})})
    raise ToolError(f"maximum agent steps exceeded: {max_steps}")


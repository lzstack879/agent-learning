import asyncio
import pytest
from pydantic import BaseModel

from agent_learning.core import Tool, ToolError, ToolExecutor, run_agent_loop


class Args(BaseModel):
    value: int


async def echo(value: int):
    return value


class Model:
    async def decide(self, messages, tools):
        if len(messages) == 1:
            return {"type": "tool_call", "name": "echo", "arguments": {"value": 2}}
        return {"type": "final", "content": "ok"}


def test_loop_and_schema_validation():
    executor = ToolExecutor([Tool("echo", "echo", Args, echo)])
    assert asyncio.run(run_agent_loop(Model(), "x", executor)) == "ok"
    with pytest.raises(ToolError, match="unknown tool"):
        asyncio.run(executor.execute("missing", {}))
    with pytest.raises(ToolError, match="invalid arguments"):
        asyncio.run(executor.execute("echo", {"value": "bad"}))


def test_timeout():
    async def slow(value: int):
        await asyncio.sleep(0.05)
    executor = ToolExecutor([Tool("slow", "slow", Args, slow)], timeout=0.001)
    with pytest.raises(ToolError, match="timed out"):
        asyncio.run(executor.execute("slow", {"value": 1}))

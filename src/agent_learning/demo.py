import asyncio

from .core import ToolExecutor, run_agent_loop
from .tools import default_tools


class DemoModel:
    async def decide(self, messages, tools):
        if not any(m["role"] == "tool" for m in messages):
            return {"type": "tool_call", "name": "weather", "arguments": {"city": "Shanghai"}}
        return {"type": "final", "content": "已查询上海天气：晴，22°C。"}


async def main() -> None:
    result = await run_agent_loop(DemoModel(), "上海天气如何？", ToolExecutor(default_tools()))
    print(result)


if __name__ == "__main__":
    asyncio.run(main())


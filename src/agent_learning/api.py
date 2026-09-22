from __future__ import annotations

import asyncio
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from .core import ToolError, ToolExecutor, run_agent_loop
from .demo import DemoModel
from .tools import default_tools

app = FastAPI(title="Agent Learning Lab", version="0.1.0")
executor = ToolExecutor(default_tools())


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    try:
        return {"answer": await run_agent_loop(DemoModel(), request.message, executor)}
    except ToolError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/chat/stream")
async def stream(request: ChatRequest) -> StreamingResponse:
    async def events():
        answer = await run_agent_loop(DemoModel(), request.message, executor)
        for token in answer:
            yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0)
        yield "data: [DONE]\n\n"
    return StreamingResponse(events(), media_type="text/event-stream")


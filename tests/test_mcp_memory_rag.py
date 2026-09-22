from pathlib import Path

import pytest

from agent_learning.memory import Memory
from agent_learning.mcp_server import SafeFileSystem
from agent_learning.rag import Document, InMemoryRetriever, RetrievalTool


def test_safe_filesystem(tmp_path: Path):
    fs = SafeFileSystem(tmp_path)
    fs.write("a.txt", "hello agent")
    assert fs.read("a.txt") == "hello agent"
    assert "a.txt" in fs.search("agent")
    with pytest.raises(ValueError):
        fs.read("../outside.txt")


def test_memory_and_retrieval():
    memory = Memory()
    memory.remember("city", "Shanghai")
    assert memory.recall("city") == "Shanghai"
    tool = RetrievalTool(InMemoryRetriever([Document("1", "python agent", "a.md")]))
    assert tool("agent")["sources"][0]["id"] == "1"


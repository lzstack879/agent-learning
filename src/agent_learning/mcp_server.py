from __future__ import annotations

import os
from pathlib import Path


class SafeFileSystem:
    def __init__(self, root: str | Path | None = None, max_bytes: int = 1_000_000) -> None:
        self.root = Path(root or os.getenv("ROOT_DIRECTORY", ".")).resolve()
        self.max_bytes = max_bytes

    def _path(self, relative: str) -> Path:
        target = (self.root / relative).resolve()
        if target != self.root and self.root not in target.parents:
            raise ValueError("path escapes sandbox root")
        return target

    def read(self, path: str) -> str:
        return self._path(path).read_text(encoding="utf-8")

    def write(self, path: str, content: str) -> dict[str, object]:
        if len(content.encode()) > self.max_bytes:
            raise ValueError("content exceeds size limit")
        target = self._path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"path": str(target.relative_to(self.root)), "bytes": len(content.encode())}

    def list(self, path: str = ".") -> list[str]:
        return sorted(p.name for p in self._path(path).iterdir())

    def search(self, query: str) -> list[str]:
        hits = []
        for path in self.root.rglob("*"):
            if path.is_file() and path.stat().st_size <= self.max_bytes:
                if query.lower() in path.read_text(encoding="utf-8", errors="ignore").lower():
                    hits.append(str(path.relative_to(self.root)))
        return sorted(hits)


try:
    from fastmcp import FastMCP
    mcp = FastMCP("safe-filesystem")
    _fs = SafeFileSystem()

    @mcp.tool()
    def read_file(path: str) -> str: return _fs.read(path)
    @mcp.tool()
    def write_file(path: str, content: str) -> dict: return _fs.write(path, content)
    @mcp.tool()
    def list_directory(path: str = ".") -> list[str]: return _fs.list(path)
    @mcp.tool()
    def search_content(query: str) -> list[str]: return _fs.search(query)
except ImportError:  # The safe core remains testable without optional MCP dependencies.
    mcp = None


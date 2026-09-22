from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    id: str
    text: str
    source: str


class InMemoryRetriever:
    """Deterministic retriever; swap with ChromaDB/Milvus behind the same interface."""
    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents

    def search(self, query: str, k: int = 3) -> list[Document]:
        terms = set(query.lower().split())
        ranked = sorted(self.documents,
                        key=lambda d: len(terms & set(d.text.lower().split())), reverse=True)
        return ranked[:k]


class RetrievalTool:
    def __init__(self, retriever: InMemoryRetriever) -> None:
        self.retriever = retriever
        self.calls = 0

    def __call__(self, query: str, k: int = 3) -> dict:
        self.calls += 1
        docs = self.retriever.search(query, k)
        return {"query": query, "sources": [{"id": d.id, "source": d.source, "text": d.text} for d in docs]}


def should_retrieve(answer_confidence: float, query: str) -> bool:
    return answer_confidence < 0.75 or any(word in query.lower() for word in ("最新", "依据", "来源"))


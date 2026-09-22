from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Review:
    approved: bool
    feedback: str


@dataclass
class WritingTeam:
    researcher: Callable[[str], str]
    writer: Callable[[str, str], str]
    reviewer: Callable[[str], Review]
    max_rounds: int = 2

    def run(self, topic: str) -> dict[str, object]:
        research = self.researcher(topic)
        draft = self.writer(topic, research)
        history: list[dict[str, str]] = []
        for round_no in range(1, self.max_rounds + 1):
            review = self.reviewer(draft)
            history.append({"round": str(round_no), "feedback": review.feedback})
            if review.approved:
                break
            draft = self.writer(topic, research + "\nReviewer feedback: " + review.feedback)
        return {"topic": topic, "research": research, "draft": draft, "history": history,
                "approved": review.approved}


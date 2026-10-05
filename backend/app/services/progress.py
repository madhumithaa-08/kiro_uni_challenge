"""Progress use case: streaks, totals, and per-topic breakdown."""

from __future__ import annotations

from datetime import date
from typing import Any

from ..domain.streaks import current_streak, longest_streak
from ..repository.db import Database


def get_progress(db: Database, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    days = db.active_days()
    counts = db.topic_counts()
    by_topic = [{"topic": t, "count": c} for t, c in sorted(counts.items())]
    return {
        "current_streak": current_streak(days, today),
        "longest_streak": longest_streak(days),
        "total_solved": db.total_problems(),
        "total_flashcards": db.count_flashcards(),
        "by_topic": by_topic,
    }

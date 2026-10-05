"""Review use case: list due flashcards and grade/reschedule them."""

from __future__ import annotations

from datetime import date
from typing import Any

from ..domain.scheduler import Card, schedule
from ..repository.db import Database


def due_cards(db: Database, today: date | None = None) -> list[dict[str, Any]]:
    today = today or date.today()
    return db.due_flashcards(today)


def grade_card(db: Database, card_id: int, grade: str, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    row = db.get_flashcard(card_id)
    if row is None:
        raise KeyError(card_id)
    card = Card(
        interval_days=int(row["interval_days"]),
        ease=float(row["ease"]),
        due_date=date.fromisoformat(row["due_date"]),
        last_reviewed=date.fromisoformat(row["last_reviewed"]) if row["last_reviewed"] else None,
    )
    updated = schedule(card, grade, today)
    assert updated.due_date is not None
    db.update_flashcard_schedule(
        card_id,
        updated.interval_days,
        updated.ease,
        updated.due_date.isoformat(),
        today.isoformat(),
    )
    db.record_activity(today, "review")
    return {
        "id": card_id,
        "interval_days": updated.interval_days,
        "due_date": updated.due_date.isoformat(),
    }

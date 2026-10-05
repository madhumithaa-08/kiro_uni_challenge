"""Capture use case: turn a submitted solution into a stored, organized,
analyzed, flashcarded record. Orchestrates domain + repository + vault.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from ..domain import complexity as complexity_mod
from ..domain import generate
from ..domain.language import detect_language
from ..domain.slugify import slugify
from ..repository.db import Database
from ..vault import write_solution


def capture_solution(
    db: Database,
    vault_root: Path,
    *,
    title: str,
    code: str,
    topic: str,
    platform: str = "other",
    language: str | None = None,
    problem_slug: str | None = None,
    notes: str = "",
    today: date | None = None,
) -> dict[str, Any]:
    """Execute the full capture flow and return the stored problem dict."""
    today = today or date.today()
    lang = language or detect_language(code, None)
    slug = slugify(problem_slug or title) or "solution"

    result = complexity_mod.analyze(code, lang)
    explanation = generate.build_explanation(title, topic, lang, result)

    existing = db.find_problem(platform, slug)
    previous_path = existing["file_path"] if existing else None
    # Preserve a user's edited explanation/notes on re-capture of same problem.
    if existing:
        explanation = existing["explanation"] or explanation
        notes = notes or existing["notes"]

    file_path = write_solution(
        vault_root=vault_root,
        topic=topic,
        problem_slug=slug,
        language=lang,
        code=code,
        previous_path=previous_path,
    )

    now = today.isoformat()
    record = {
        "title": title,
        "platform": platform,
        "problem_slug": slug,
        "topic": slugify(topic) or "uncategorized",
        "language": lang,
        "code": code,
        "explanation": explanation,
        "notes": notes,
        "time_complexity": result.time,
        "space_complexity": result.space,
        "file_path": file_path,
        "created_at": now,
        "updated_at": now,
    }
    pid = db.upsert_problem(record)

    # (Re)build flashcards, due today for first review.
    seeds = generate.build_flashcards(title, record["topic"], result)
    cards = [
        {
            "front": s.front,
            "back": s.back,
            "interval_days": 0,
            "ease": 2.5,
            "due_date": now,
            "last_reviewed": None,
        }
        for s in seeds
    ]
    db.replace_flashcards(pid, cards)

    db.record_activity(today, "capture")

    stored = db.get_problem(pid)
    assert stored is not None
    return stored

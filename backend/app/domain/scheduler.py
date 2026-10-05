"""Spaced-repetition scheduling (SM-2-lite).

Pure module: no I/O. The current date is injected (never read from the clock)
so the scheduler is deterministic and property-testable.

Invariants (requirements 6.4, 6.5, 9.3):
- The new ``due_date`` is always strictly after the review date (``today``).
- ``interval_days`` is never negative; ``ease`` never drops below ``MIN_EASE``.
- Grade "again" never yields a larger interval than grade "good" for the same
  starting card.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, timedelta

MIN_EASE = 1.3
DEFAULT_EASE = 2.5

GRADES = ("again", "good", "easy")


@dataclass(frozen=True)
class Card:
    """Spaced-repetition state for a single flashcard."""

    interval_days: int = 0
    ease: float = DEFAULT_EASE
    due_date: date | None = None
    last_reviewed: date | None = None


def new_card(today: date) -> Card:
    """Create a fresh card due immediately on ``today``."""
    return Card(interval_days=0, ease=DEFAULT_EASE, due_date=today, last_reviewed=None)


def _next_interval(interval_days: int, ease: float, grade: str) -> int:
    if grade == "again":
        return 1
    if interval_days <= 0:
        # First successful review moves a brand-new card to a 1-day interval
        # ("good") or a slightly longer one ("easy").
        return 2 if grade == "easy" else 1
    scaled = round(interval_days * ease)
    if grade == "easy":
        scaled = round(scaled * 1.3)
    return max(1, scaled)


def _next_ease(ease: float, grade: str) -> float:
    if grade == "again":
        return max(MIN_EASE, ease - 0.2)
    if grade == "easy":
        return ease + 0.15
    return ease  # "good" keeps ease steady


def schedule(card: Card, grade: str, today: date) -> Card:
    """Return the updated card after reviewing it with ``grade`` on ``today``.

    ``grade`` must be one of :data:`GRADES`. The returned card's ``due_date`` is
    strictly after ``today``.
    """
    if grade not in GRADES:
        raise ValueError(f"grade must be one of {GRADES}, got {grade!r}")

    interval = _next_interval(card.interval_days, card.ease, grade)
    ease = _next_ease(card.ease, grade)
    # interval is always >= 1 here, so due_date is strictly after today.
    due = today + timedelta(days=interval)
    return replace(
        card,
        interval_days=interval,
        ease=ease,
        due_date=due,
        last_reviewed=today,
    )

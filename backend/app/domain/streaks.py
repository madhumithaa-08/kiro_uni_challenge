"""Daily streak computation from a set of active calendar days.

Pure module: no I/O. The current date is injected. See requirements 5.1-5.3,
5.5 and invariant 9.2.
"""

from __future__ import annotations

from datetime import date, timedelta


def current_streak(active_days: set[date], today: date) -> int:
    """Number of consecutive active days ending on ``today``.

    If ``today`` is not active, the streak is 0 (requirement 5.2). The result
    is never negative and never exceeds ``len(active_days)`` (invariant 9.2).
    """
    if today not in active_days:
        return 0
    streak = 0
    day = today
    while day in active_days:
        streak += 1
        day = day - timedelta(days=1)
    return streak


def longest_streak(active_days: set[date]) -> int:
    """Length of the longest run of consecutive active days (requirement 5.5).

    Always ``>= current_streak`` for the same day set, and ``0`` when there is
    no activity.
    """
    if not active_days:
        return 0
    best = 0
    for day in active_days:
        # Only start counting from the beginning of a run (no active day before).
        if day - timedelta(days=1) in active_days:
            continue
        length = 0
        cursor = day
        while cursor in active_days:
            length += 1
            cursor = cursor + timedelta(days=1)
        best = max(best, length)
    return best

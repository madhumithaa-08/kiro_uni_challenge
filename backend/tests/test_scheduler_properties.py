"""Property tests for the spaced-repetition scheduler.

Task 6.4, requirements 6.4 / 6.5 / 9.3.
"""

from datetime import date, timedelta

from hypothesis import given, strategies as st

from app.domain.scheduler import GRADES, MIN_EASE, Card, schedule

dates = st.dates(min_value=date(2000, 1, 1), max_value=date(2100, 1, 1))
intervals = st.integers(min_value=0, max_value=3650)
eases = st.floats(min_value=1.3, max_value=4.0, allow_nan=False, allow_infinity=False)
grades = st.sampled_from(GRADES)


def _card(interval: int, ease: float, today: date) -> Card:
    return Card(interval_days=interval, ease=ease, due_date=today, last_reviewed=None)


@given(intervals, eases, grades, dates)
def test_due_date_strictly_after_review(interval, ease, grade, today) -> None:
    updated = schedule(_card(interval, ease, today), grade, today)
    assert updated.due_date is not None
    assert updated.due_date > today  # strictly after (invariant 9.3)


@given(intervals, eases, grades, dates)
def test_interval_nonnegative_and_ease_floored(interval, ease, grade, today) -> None:
    updated = schedule(_card(interval, ease, today), grade, today)
    assert updated.interval_days >= 1
    assert updated.ease >= MIN_EASE


@given(intervals, eases, dates)
def test_again_never_exceeds_good(interval, ease, today) -> None:
    base = _card(interval, ease, today)
    again = schedule(base, "again", today)
    good = schedule(base, "good", today)
    assert again.interval_days <= good.interval_days


@given(intervals, eases, grades, dates)
def test_last_reviewed_is_today(interval, ease, grade, today) -> None:
    updated = schedule(_card(interval, ease, today), grade, today)
    assert updated.last_reviewed == today

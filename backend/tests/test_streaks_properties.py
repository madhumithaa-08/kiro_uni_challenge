"""Property tests for streak computation.

Task 6.5, requirements 5.1 / 5.2 / 5.3 / 9.2.
"""

from datetime import date, timedelta

from hypothesis import given, strategies as st

from app.domain.streaks import current_streak, longest_streak

base_dates = st.dates(min_value=date(2000, 1, 1), max_value=date(2100, 1, 1))
day_offsets = st.sets(st.integers(min_value=-400, max_value=0), max_size=60)


def _days(today: date, offsets: set[int]) -> set[date]:
    return {today + timedelta(days=o) for o in offsets}


@given(base_dates, day_offsets)
def test_current_streak_bounded_by_active_days(today, offsets) -> None:
    days = _days(today, offsets)
    cs = current_streak(days, today)
    assert 0 <= cs <= len(days)


@given(base_dates, day_offsets)
def test_current_streak_zero_when_today_inactive(today, offsets) -> None:
    days = _days(today, offsets) - {today}
    assert current_streak(days, today) == 0


@given(base_dates, day_offsets)
def test_current_streak_counts_consecutive_run(today, offsets) -> None:
    days = _days(today, offsets)
    cs = current_streak(days, today)
    if today in days:
        # Every day in the counted run must be active, and the day just before
        # the run must be absent.
        for k in range(cs):
            assert (today - timedelta(days=k)) in days
        assert (today - timedelta(days=cs)) not in days
    else:
        assert cs == 0


@given(base_dates, day_offsets)
def test_longest_at_least_current(today, offsets) -> None:
    days = _days(today, offsets)
    assert longest_streak(days) >= current_streak(days, today)


@given(day_offsets)
def test_longest_bounded_by_total(offsets) -> None:
    today = date(2026, 1, 1)
    days = _days(today, offsets)
    assert 0 <= longest_streak(days) <= len(days)


def test_empty_has_no_streak() -> None:
    assert current_streak(set(), date(2026, 1, 1)) == 0
    assert longest_streak(set()) == 0

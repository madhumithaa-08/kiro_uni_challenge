"""Property test: per-topic counts always reconcile with the total.

Task 6.7, requirements 5.4 / 5.5 / 9.5. Uses a temp SQLite DB and temp vault so
the test is hermetic and leaves no stray files.
"""

import tempfile
from datetime import date
from pathlib import Path

from hypothesis import given, settings, strategies as st

from app.repository.db import Database
from app.services.capture import capture_solution
from app.services.progress import get_progress

topics = st.sampled_from(["arrays", "graphs", "trees", "strings", "hashing"])
titles = st.text(
    alphabet=st.characters(min_codepoint=97, max_codepoint=122), min_size=1, max_size=8
)


@settings(max_examples=25, deadline=None)
@given(st.lists(st.tuples(titles, topics), min_size=0, max_size=12))
def test_topic_counts_sum_to_total(entries) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Database(Path(tmp) / "t.db")
        vault = Path(tmp) / "vault"
        today = date(2026, 1, 1)
        for i, (title, topic) in enumerate(entries):
            capture_solution(
                db,
                vault,
                title=title,
                code="def f(x):\n    return x\n",
                topic=topic,
                platform="leetcode",
                problem_slug=f"p-{i}",  # unique slug -> each is a distinct problem
                today=today,
            )
        progress = get_progress(db, today)
        by_topic_sum = sum(tc["count"] for tc in progress["by_topic"])
        assert by_topic_sum == progress["total_solved"]
        assert progress["total_solved"] == len(entries)
        db.close()

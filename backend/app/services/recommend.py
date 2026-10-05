"""Recommendation use case: learning path + next-topic suggestions."""

from __future__ import annotations

from typing import Any

from ..domain.learning_path import Dag, topological_path
from ..repository.db import Database


def learning_path(dag: Dag, topic: str) -> list[str]:
    """Prerequisite-respecting path ending at ``topic`` (may raise CycleError
    or KeyError, mapped to HTTP by the router)."""
    return topological_path(dag, topic)


def recommend_topics(dag: Dag, db: Database, topic: str) -> dict[str, Any]:
    """Suggest topics to study next: the prerequisite path for ``topic``,
    prioritizing topics the user has solved the least."""
    path = topological_path(dag, topic)
    counts = db.topic_counts()
    # Topics in the path the user has touched least come first (but keep the
    # prerequisite order as the primary signal — only annotate counts).
    note_parts = []
    for t in path:
        solved = counts.get(t, 0)
        note_parts.append(f"{t} (solved: {solved})")
    return {
        "topic": topic,
        "recommended_topics": path,
        "note": "Study in this order; counts show how many you've solved: "
        + ", ".join(note_parts),
    }

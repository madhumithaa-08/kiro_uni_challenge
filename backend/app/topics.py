"""Load the topic DAG from topics.yaml."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from .config import topics_file
from .domain.learning_path import Dag


def load_topics(path: Path | None = None) -> Dag:
    p = path or topics_file()
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    dag: Dag = {}
    for topic, prereqs in raw.items():
        dag[str(topic)] = [str(x) for x in (prereqs or [])]
    # Ensure every referenced prerequisite exists as a node.
    for prereqs in list(dag.values()):
        for pre in prereqs:
            dag.setdefault(pre, [])
    return dag


@lru_cache(maxsize=1)
def cached_topics() -> Dag:
    return load_topics()

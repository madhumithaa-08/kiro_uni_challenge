"""Property tests for the learning-path topic DAG.

Task 6.6, requirements 7.1 / 7.2 / 7.3 / 9.4.

Strategy: generate a random DAG by giving each node only lower-indexed nodes as
prerequisites (guarantees acyclicity), then separately inject a back-edge to
force a cycle and assert detection.
"""

import pytest
from hypothesis import given, strategies as st

from app.domain.learning_path import CycleError, detect_cycle, topological_path


@st.composite
def acyclic_dags(draw):
    n = draw(st.integers(min_value=1, max_value=8))
    nodes = [f"t{i}" for i in range(n)]
    dag = {}
    for i, node in enumerate(nodes):
        # Prerequisites may only point to earlier nodes -> no cycles possible.
        possible = nodes[:i]
        prereqs = draw(st.lists(st.sampled_from(possible), unique=True)) if possible else []
        dag[node] = prereqs
    return dag


@given(acyclic_dags())
def test_topological_order_is_valid(dag) -> None:
    target = f"t{len(dag) - 1}"
    order = topological_path(dag, target)
    # Every topic appears exactly once (no duplicates, no omissions among reachable).
    assert len(order) == len(set(order))
    position = {node: idx for idx, node in enumerate(order)}
    # No topic appears before any of its prerequisites.
    for node in order:
        for prereq in dag.get(node, []):
            assert prereq in position
            assert position[prereq] < position[node]


@given(acyclic_dags())
def test_acyclic_dag_has_no_cycle(dag) -> None:
    assert detect_cycle(dag) is None


@given(acyclic_dags())
def test_injected_cycle_is_detected(dag) -> None:
    # Force a self-loop on the last node -> guaranteed cycle.
    last = f"t{len(dag) - 1}"
    dag[last] = list(dag[last]) + [last]
    with pytest.raises(CycleError):
        topological_path(dag, last)


def test_unknown_topic_raises_keyerror() -> None:
    with pytest.raises(KeyError):
        topological_path({"a": []}, "nope")

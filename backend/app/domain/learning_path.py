"""Topic prerequisite graph: cycle detection and topological ordering.

Pure module: no I/O. See requirements 7.1-7.3 and invariant 9.4.

A DAG is represented as a mapping of ``topic -> list of prerequisite topics``.
``topological_path(dag, target)`` returns the prerequisites-first order of all
topics reachable from ``target`` (including ``target`` last).
"""

from __future__ import annotations

Dag = dict[str, list[str]]


class CycleError(Exception):
    """Raised when the prerequisite graph contains a cycle."""

    def __init__(self, edge: tuple[str, str]) -> None:
        self.edge = edge
        super().__init__(f"prerequisite cycle detected at edge {edge[0]} -> {edge[1]}")


def _reachable(dag: Dag, target: str) -> set[str]:
    """All topics reachable from ``target`` following prerequisite edges."""
    seen: set[str] = set()
    stack = [target]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        for prereq in dag.get(node, []):
            if prereq not in seen:
                stack.append(prereq)
    return seen


def detect_cycle(dag: Dag) -> tuple[str, str] | None:
    """Return an offending edge if the graph has a cycle, else ``None``."""
    WHITE, GREY, BLACK = 0, 1, 2
    color: dict[str, int] = {node: WHITE for node in dag}

    def visit(node: str) -> tuple[str, str] | None:
        color[node] = GREY
        for prereq in dag.get(node, []):
            state = color.get(prereq, WHITE)
            if state == GREY:
                return (node, prereq)
            if state == WHITE:
                found = visit(prereq)
                if found is not None:
                    return found
        color[node] = BLACK
        return None

    for node in dag:
        if color[node] == WHITE:
            found = visit(node)
            if found is not None:
                return found
    return None


def topological_path(dag: Dag, target: str) -> list[str]:
    """Return topics reachable from ``target`` in prerequisites-first order.

    Every reachable topic appears exactly once, and no topic appears before any
    of its prerequisites (invariant 9.4). Raises :class:`CycleError` if the
    graph contains a cycle.
    """
    if target not in dag:
        raise KeyError(f"unknown topic: {target!r}")

    reachable = _reachable(dag, target)
    # Restrict the graph to the reachable subgraph for cycle detection + sort.
    sub: Dag = {node: [p for p in dag.get(node, []) if p in reachable] for node in reachable}

    cycle = detect_cycle(sub)
    if cycle is not None:
        raise CycleError(cycle)

    order: list[str] = []
    visited: set[str] = set()

    def emit(node: str) -> None:
        if node in visited:
            return
        visited.add(node)
        for prereq in sub.get(node, []):
            emit(prereq)
        order.append(node)

    emit(target)
    return order

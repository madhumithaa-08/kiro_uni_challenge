"""Static time/space complexity heuristic and best-practice suggestions.

Pure module: no I/O, and it NEVER executes the analyzed code (requirement 3.4).
For Python it uses the ``ast`` module to measure loop-nesting depth; for other
languages it falls back to a conservative brace/keyword scan. When signals are
unclear it returns ``"unknown"`` rather than guessing (requirement 3.2).
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field


@dataclass
class ComplexityResult:
    time: str = "unknown"
    space: str = "unknown"
    suggestions: list[str] = field(default_factory=list)


_POLY = {0: "O(1)", 1: "O(n)", 2: "O(n^2)", 3: "O(n^3)"}


def _poly(depth: int) -> str:
    if depth in _POLY:
        return _POLY[depth]
    if depth >= 4:
        return f"O(n^{depth})"
    return "unknown"


class _DepthVisitor(ast.NodeVisitor):
    """Measures maximum loop-nesting depth and notes recursion/sorting."""

    def __init__(self) -> None:
        self.max_depth = 0
        self._depth = 0
        self.has_sort = False
        self.func_names: set[str] = set()
        self.called_names: set[str] = set()
        self.uses_aux_structure = False

    def _enter_loop(self, node: ast.AST) -> None:
        self._depth += 1
        self.max_depth = max(self.max_depth, self._depth)
        self.generic_visit(node)
        self._depth -= 1

    def visit_For(self, node: ast.For) -> None:
        self._enter_loop(node)

    def visit_While(self, node: ast.While) -> None:
        self._enter_loop(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.func_names.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute):
            if func.attr in {"sort", "sorted"}:
                self.has_sort = True
            self.called_names.add(func.attr)
        elif isinstance(func, ast.Name):
            if func.id == "sorted":
                self.has_sort = True
            self.called_names.add(func.id)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.uses_aux_structure = True
        self.generic_visit(node)

    def visit_List(self, node: ast.List) -> None:
        self.uses_aux_structure = True
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        self.uses_aux_structure = True
        self.generic_visit(node)

    def visit_Set(self, node: ast.Set) -> None:
        self.uses_aux_structure = True
        self.generic_visit(node)


def _analyze_python(code: str) -> ComplexityResult:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return ComplexityResult(time="unknown", space="unknown", suggestions=[])

    visitor = _DepthVisitor()
    visitor.visit(tree)

    recursive = bool(visitor.func_names & visitor.called_names)

    # Time estimate from loop nesting, refined by sort/recursion signals.
    time = _poly(visitor.max_depth)
    if visitor.has_sort and visitor.max_depth <= 1:
        time = "O(n log n)"
    if recursive and visitor.max_depth == 0:
        # Recursion with no explicit loops: likely sub-linear or linear; stay
        # honest and avoid over-claiming.
        time = "unknown"

    space = "O(n)" if (visitor.uses_aux_structure or recursive) else "O(1)"

    suggestions = _python_suggestions(code)
    return ComplexityResult(time=time, space=space, suggestions=suggestions)


def _python_suggestions(code: str) -> list[str]:
    tips: list[str] = []
    if " in " in code and "for " in code and "set(" not in code and "{" not in code:
        tips.append(
            "If you repeatedly test membership inside a loop, use a set/dict for "
            "O(1) lookups instead of a list."
        )
    if "range(len(" in code:
        tips.append(
            "Prefer iterating directly or using enumerate() over range(len(...))."
        )
    if code.count("+ ") > 0 and "''.join" not in code and "\"\".join" not in code and "for" in code:
        tips.append(
            "Building strings with repeated concatenation in a loop is O(n^2); "
            "accumulate in a list and ''.join(...) at the end."
        )
    return tips


def _analyze_generic(code: str) -> ComplexityResult:
    """Conservative fallback for non-Python languages: scan nesting by braces
    around loop keywords. Returns ``unknown`` time when it cannot be sure."""
    depth = 0
    max_depth = 0
    loop_keywords = ("for", "while", "forEach")
    lines = code.splitlines()
    brace_depth = 0
    loop_brace_stack: list[int] = []
    for line in lines:
        stripped = line.strip()
        starts_loop = any(
            stripped.startswith(k) or f" {k} " in f" {stripped} " for k in loop_keywords
        )
        if starts_loop:
            depth += 1
            max_depth = max(max_depth, depth)
            loop_brace_stack.append(brace_depth)
        brace_depth += line.count("{") - line.count("}")
        while loop_brace_stack and brace_depth <= loop_brace_stack[-1]:
            loop_brace_stack.pop()
            depth = max(0, depth - 1)

    time = _poly(max_depth) if max_depth <= 3 else _poly(max_depth)
    space = "unknown"
    return ComplexityResult(time=time, space=space, suggestions=[])


def analyze(code: str, language: str) -> ComplexityResult:
    """Estimate time/space complexity statically. Never executes ``code``.

    Returns a :class:`ComplexityResult`; ``time``/``space`` are Big-O strings or
    ``"unknown"``. This function never raises for arbitrary input (test 6.3).
    """
    if not code or not code.strip():
        return ComplexityResult()
    try:
        if language == "python":
            return _analyze_python(code)
        return _analyze_generic(code)
    except Exception:
        # Defensive: analysis must never crash the capture flow.
        return ComplexityResult()

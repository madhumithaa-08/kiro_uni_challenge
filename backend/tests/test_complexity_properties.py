"""Property tests for the complexity analyzer (task 6.3, requirements 3.*)."""

import re

from hypothesis import given, strategies as st

from app.domain.complexity import ComplexityResult, analyze
from app.domain.language import KNOWN_LANGUAGES

BIGO_RE = re.compile(r"^(unknown|O\(.+\))$")


@given(st.text(), st.sampled_from(sorted(KNOWN_LANGUAGES)))
def test_analyze_never_raises_and_shapes_output(code: str, language: str) -> None:
    result = analyze(code, language)
    assert isinstance(result, ComplexityResult)
    assert BIGO_RE.match(result.time)
    assert BIGO_RE.match(result.space)
    assert isinstance(result.suggestions, list)
    assert all(isinstance(s, str) for s in result.suggestions)


@given(st.text())
def test_analyze_is_deterministic(code: str) -> None:
    a = analyze(code, "python")
    b = analyze(code, "python")
    assert (a.time, a.space, a.suggestions) == (b.time, b.space, b.suggestions)


def test_single_loop_is_linear() -> None:
    code = "def f(a):\n    for x in a:\n        print(x)\n"
    assert analyze(code, "python").time == "O(n)"


def test_nested_loop_is_quadratic() -> None:
    code = "def f(a):\n    for x in a:\n        for y in a:\n            print(x, y)\n"
    assert analyze(code, "python").time == "O(n^2)"


def test_no_loop_is_constant_time() -> None:
    code = "def f(a):\n    return a + 1\n"
    assert analyze(code, "python").time == "O(1)"

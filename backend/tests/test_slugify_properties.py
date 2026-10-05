"""Property tests for slugify (tasks 6.1, requirements 2.4 / 9.1)."""

import re

from hypothesis import given, strategies as st

from app.domain.slugify import slugify

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@given(st.text())
def test_slug_is_idempotent(s: str) -> None:
    once = slugify(s)
    twice = slugify(once)
    assert once == twice


@given(st.text())
def test_slug_charset_and_shape(s: str) -> None:
    out = slugify(s)
    # Either empty (no alphanumerics in input) or a clean hyphenated slug.
    assert out == "" or SLUG_RE.match(out)
    assert out == out.lower()
    assert " " not in out
    assert not out.startswith("-")
    assert not out.endswith("-")
    assert "--" not in out


@given(st.text(alphabet=st.characters(min_codepoint=48, max_codepoint=122)))
def test_slug_stable_across_inputs(s: str) -> None:
    # Deterministic: same input always maps to the same slug.
    assert slugify(s) == slugify(s)


@given(st.text(), st.integers(min_value=1, max_value=80))
def test_slug_respects_max_length(s: str, limit: int) -> None:
    out = slugify(s, max_length=limit)
    # Never exceeds the cap, stays a clean slug, and is idempotent under the cap.
    assert len(out) <= limit
    assert out == "" or SLUG_RE.match(out)
    assert slugify(out, max_length=limit) == out

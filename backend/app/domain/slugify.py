"""Filesystem-safe, idempotent slug generation.

Pure module: no I/O. See requirements 2.4 and 9.1.
"""

from __future__ import annotations

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_EDGE_HYPHENS = re.compile(r"^-+|-+$")


def slugify(text: str, max_length: int | None = None) -> str:
    """Return a lowercase, hyphenated, filesystem-safe slug.

    The function is idempotent: ``slugify(slugify(s)) == slugify(s)`` for any
    input ``s``. Output matches ``^[a-z0-9]+(-[a-z0-9]+)*$`` or is the empty
    string (for input with no alphanumeric characters).

    If ``max_length`` is given, the slug is truncated to at most that many
    characters at a hyphen boundary (so a word is never cut in half), keeping
    the result a valid slug. ``max_length`` is still idempotent: truncating an
    already-truncated slug with the same limit returns the same value.
    """
    lowered = text.strip().lower()
    # Collapse any run of non-alphanumeric characters into a single hyphen.
    hyphenated = _NON_ALNUM.sub("-", lowered)
    # Trim leading/trailing hyphens produced by the substitution.
    trimmed = _EDGE_HYPHENS.sub("", hyphenated)

    if max_length is not None and len(trimmed) > max_length:
        clipped = trimmed[:max_length]
        # Prefer cutting at the last hyphen so we don't leave a partial word.
        if "-" in clipped:
            clipped = clipped[: clipped.rfind("-")]
        trimmed = _EDGE_HYPHENS.sub("", clipped)
    return trimmed

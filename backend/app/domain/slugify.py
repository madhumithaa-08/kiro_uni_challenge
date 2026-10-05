"""Filesystem-safe, idempotent slug generation.

Pure module: no I/O. See requirements 2.4 and 9.1.
"""

from __future__ import annotations

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_EDGE_HYPHENS = re.compile(r"^-+|-+$")


def slugify(text: str) -> str:
    """Return a lowercase, hyphenated, filesystem-safe slug.

    The function is idempotent: ``slugify(slugify(s)) == slugify(s)`` for any
    input ``s``. Output matches ``^[a-z0-9]+(-[a-z0-9]+)*$`` or is the empty
    string (for input with no alphanumeric characters).
    """
    lowered = text.strip().lower()
    # Collapse any run of non-alphanumeric characters into a single hyphen.
    hyphenated = _NON_ALNUM.sub("-", lowered)
    # Trim leading/trailing hyphens produced by the substitution.
    trimmed = _EDGE_HYPHENS.sub("", hyphenated)
    return trimmed

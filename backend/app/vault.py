"""On-disk organized code tree: ``vault/<topic-slug>/<problem-slug>.<ext>``.

This is the only module permitted to write the vault filesystem tree
(steering: structure). Collision-safe per requirement 2.5.
"""

from __future__ import annotations

from pathlib import Path

from .domain.language import extension_for
from .domain.slugify import slugify


def _unique_path(directory: Path, base_slug: str, ext: str, keep: Path | None) -> Path:
    """Return a path under ``directory`` that does not clash with a different
    problem's file. ``keep`` is the current file for this problem (if any),
    which is allowed to be reused."""
    candidate = directory / f"{base_slug}.{ext}"
    if keep is not None and candidate.resolve() == keep.resolve():
        return candidate
    n = 2
    while candidate.exists() and (keep is None or candidate.resolve() != keep.resolve()):
        candidate = directory / f"{base_slug}-{n}.{ext}"
        n += 1
    return candidate


def write_solution(
    vault_root: Path,
    topic: str,
    problem_slug: str,
    language: str,
    code: str,
    previous_path: str | None = None,
) -> str:
    """Write ``code`` to the topic tree and return the repo-relative path.

    Creates the topic directory if needed (requirement 2.2). If the solution
    moved topics or changed slug, the old file is removed so the tree stays
    consistent (requirement 2.3).
    """
    topic_slug = slugify(topic) or "uncategorized"
    base = slugify(problem_slug) or "solution"
    ext = extension_for(language)

    topic_dir = vault_root / topic_slug
    topic_dir.mkdir(parents=True, exist_ok=True)

    keep: Path | None = None
    old_abs: Path | None = None
    if previous_path:
        old_abs = vault_root / previous_path if not Path(previous_path).is_absolute() else Path(previous_path)
        # Allow reusing the same file only if it is already in the right folder.
        if old_abs.parent.resolve() == topic_dir.resolve():
            keep = old_abs

    target = _unique_path(topic_dir, base, ext, keep)
    target.write_text(code, encoding="utf-8")

    # Remove a stale file if the solution was relocated/renamed.
    if old_abs is not None and old_abs.exists() and old_abs.resolve() != target.resolve():
        try:
            old_abs.unlink()
        except OSError:
            pass

    return str(target.relative_to(vault_root).as_posix())

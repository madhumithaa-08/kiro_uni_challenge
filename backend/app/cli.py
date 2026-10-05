"""Small CLI for DSA Vault, used by Kiro hooks and for manual use.

Usage:
    python -m app.cli progress        # print a progress snapshot
    python -m app.cli due             # print flashcards due today
    python -m app.cli sync-index      # rebuild vault/INDEX.md from the DB

Kept dependency-light so a hook can invoke it quickly.
"""

from __future__ import annotations

import sys
from datetime import date

from .config import vault_root
from .deps import get_db
from .services.progress import get_progress
from .services.review import due_cards


def _cmd_progress() -> int:
    db = get_db()
    p = get_progress(db)
    print("DSA Vault — progress")
    print(f"  current streak : {p['current_streak']} day(s)")
    print(f"  longest streak : {p['longest_streak']} day(s)")
    print(f"  solved         : {p['total_solved']}")
    print(f"  flashcards     : {p['total_flashcards']}")
    if p["by_topic"]:
        print("  by topic:")
        for tc in p["by_topic"]:
            print(f"    - {tc['topic']}: {tc['count']}")
    return 0


def _cmd_due() -> int:
    db = get_db()
    cards = due_cards(db)
    if not cards:
        print("No flashcards due today. Nice — you're caught up.")
        return 0
    print(f"{len(cards)} flashcard(s) due today:")
    for c in cards[:20]:
        print(f"  - [{c['problem_title']}] {c['front']}")
    return 0


def _cmd_sync_index() -> int:
    """Write a human-readable vault/INDEX.md listing solved problems by topic."""
    db = get_db()
    problems = db.list_problems()
    by_topic: dict[str, list[dict]] = {}
    for p in problems:
        by_topic.setdefault(p["topic"], []).append(p)

    lines = ["# DSA Vault — Index", "", "Auto-generated listing of solved problems by topic.", ""]
    for topic in sorted(by_topic):
        lines.append(f"## {topic}")
        for p in sorted(by_topic[topic], key=lambda x: x["problem_slug"]):
            lines.append(
                f"- **{p['title']}** ({p['language']}, {p['time_complexity']} time / "
                f"{p['space_complexity']} space) — `{p['file_path']}`"
            )
        lines.append("")
    if not by_topic:
        lines.append("_No solutions captured yet._")

    root = vault_root()
    root.mkdir(parents=True, exist_ok=True)
    (root / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {root / 'INDEX.md'} ({len(problems)} problem(s)).")
    return 0


COMMANDS = {
    "progress": _cmd_progress,
    "due": _cmd_due,
    "sync-index": _cmd_sync_index,
}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args or args[0] not in COMMANDS:
        print(f"usage: python -m app.cli [{'|'.join(COMMANDS)}]", file=sys.stderr)
        return 2
    return COMMANDS[args[0]]()


if __name__ == "__main__":
    raise SystemExit(main())

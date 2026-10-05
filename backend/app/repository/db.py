"""SQLite persistence for problems, flashcards, and activity.

All SQLite access lives in this layer (steering: structure). Rows are converted
to plain dicts/dataclasses so higher layers never see sqlite3 types.
"""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    platform TEXT NOT NULL DEFAULT 'other',
    problem_slug TEXT NOT NULL,
    topic TEXT NOT NULL,
    language TEXT NOT NULL,
    code TEXT NOT NULL,
    explanation TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    time_complexity TEXT NOT NULL DEFAULT 'unknown',
    space_complexity TEXT NOT NULL DEFAULT 'unknown',
    file_path TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(platform, problem_slug)
);

CREATE TABLE IF NOT EXISTS flashcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    interval_days INTEGER NOT NULL DEFAULT 0,
    ease REAL NOT NULL DEFAULT 2.5,
    due_date TEXT NOT NULL,
    last_reviewed TEXT
);

CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL
);
"""


class Database:
    def __init__(self, path: Path | str) -> None:
        self.path = str(path)
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # ----- problems ---------------------------------------------------------
    def upsert_problem(self, data: dict[str, Any]) -> int:
        """Insert or update a problem keyed by (platform, problem_slug).

        Returns the problem id.
        """
        existing = self._conn.execute(
            "SELECT id, created_at FROM problems WHERE platform=? AND problem_slug=?",
            (data["platform"], data["problem_slug"]),
        ).fetchone()
        if existing is None:
            cur = self._conn.execute(
                """INSERT INTO problems
                   (title, platform, problem_slug, topic, language, code,
                    explanation, notes, time_complexity, space_complexity,
                    file_path, created_at, updated_at)
                   VALUES (:title,:platform,:problem_slug,:topic,:language,:code,
                    :explanation,:notes,:time_complexity,:space_complexity,
                    :file_path,:created_at,:updated_at)""",
                data,
            )
            self._conn.commit()
            return int(cur.lastrowid)
        pid = int(existing["id"])
        merged = dict(data)
        merged["id"] = pid
        merged["created_at"] = existing["created_at"]
        self._conn.execute(
            """UPDATE problems SET
                 title=:title, topic=:topic, language=:language, code=:code,
                 explanation=:explanation, notes=:notes,
                 time_complexity=:time_complexity, space_complexity=:space_complexity,
                 file_path=:file_path, updated_at=:updated_at
               WHERE id=:id""",
            merged,
        )
        self._conn.commit()
        return pid

    def get_problem(self, pid: int) -> dict[str, Any] | None:
        row = self._conn.execute("SELECT * FROM problems WHERE id=?", (pid,)).fetchone()
        return dict(row) if row else None

    def find_problem(self, platform: str, problem_slug: str) -> dict[str, Any] | None:
        row = self._conn.execute(
            "SELECT * FROM problems WHERE platform=? AND problem_slug=?",
            (platform, problem_slug),
        ).fetchone()
        return dict(row) if row else None

    def list_problems(self, search: str | None = None, topic: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM problems"
        clauses: list[str] = []
        params: list[Any] = []
        if search:
            clauses.append("(title LIKE ? OR notes LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        if topic:
            clauses.append("topic = ?")
            params.append(topic)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY updated_at DESC, id DESC"
        rows = self._conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def update_problem_fields(self, pid: int, fields: dict[str, Any]) -> dict[str, Any] | None:
        if not fields:
            return self.get_problem(pid)
        allowed = {"explanation", "notes"}
        sets = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not sets:
            return self.get_problem(pid)
        assignments = ", ".join(f"{k}=?" for k in sets)
        params = list(sets.values()) + [pid]
        self._conn.execute(f"UPDATE problems SET {assignments} WHERE id=?", params)
        self._conn.commit()
        return self.get_problem(pid)

    def topic_counts(self) -> dict[str, int]:
        rows = self._conn.execute(
            "SELECT topic, COUNT(*) AS c FROM problems GROUP BY topic"
        ).fetchall()
        return {r["topic"]: int(r["c"]) for r in rows}

    def total_problems(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS c FROM problems").fetchone()
        return int(row["c"])

    def solved_slugs(self) -> set[str]:
        rows = self._conn.execute("SELECT problem_slug FROM problems").fetchall()
        return {r["problem_slug"] for r in rows}

    # ----- flashcards -------------------------------------------------------
    def replace_flashcards(self, problem_id: int, cards: list[dict[str, Any]]) -> None:
        self._conn.execute("DELETE FROM flashcards WHERE problem_id=?", (problem_id,))
        for c in cards:
            self._conn.execute(
                """INSERT INTO flashcards
                   (problem_id, front, back, interval_days, ease, due_date, last_reviewed)
                   VALUES (?,?,?,?,?,?,?)""",
                (
                    problem_id,
                    c["front"],
                    c["back"],
                    c.get("interval_days", 0),
                    c.get("ease", 2.5),
                    c["due_date"],
                    c.get("last_reviewed"),
                ),
            )
        self._conn.commit()

    def due_flashcards(self, today: date) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            """SELECT f.*, p.title AS problem_title
               FROM flashcards f JOIN problems p ON p.id = f.problem_id
               WHERE f.due_date <= ? ORDER BY f.due_date ASC, f.id ASC""",
            (today.isoformat(),),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_flashcard(self, card_id: int) -> dict[str, Any] | None:
        row = self._conn.execute("SELECT * FROM flashcards WHERE id=?", (card_id,)).fetchone()
        return dict(row) if row else None

    def update_flashcard_schedule(
        self, card_id: int, interval_days: int, ease: float, due_date: str, last_reviewed: str
    ) -> None:
        self._conn.execute(
            """UPDATE flashcards SET interval_days=?, ease=?, due_date=?, last_reviewed=?
               WHERE id=?""",
            (interval_days, ease, due_date, last_reviewed, card_id),
        )
        self._conn.commit()

    def count_flashcards(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS c FROM flashcards").fetchone()
        return int(row["c"])

    # ----- activity ---------------------------------------------------------
    def record_activity(self, day: date, kind: str) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO activity (day, kind) VALUES (?, ?)",
            (day.isoformat(), kind),
        )
        self._conn.commit()

    def active_days(self) -> set[date]:
        rows = self._conn.execute("SELECT day FROM activity").fetchall()
        return {date.fromisoformat(r["day"]) for r in rows}

# DSA Vault — Design

## Overview

DSA Vault is a local-first, full-stack application. A Python FastAPI backend owns
all domain logic and persistence (SQLite + an on-disk topic-organized code tree).
A React (Vite + TypeScript) frontend consumes the backend's REST API.

The design keeps the domain logic (complexity analysis, spaced repetition, streak
computation, slugging, learning-path graph) in pure, dependency-light modules so
they are easy to property-test with Hypothesis — this is deliberate, because the
testable invariants in Requirement 9 live in these modules.

```
┌───────────────────────────┐        HTTP/JSON        ┌──────────────────────────┐
│  React (Vite + TS)        │  ───────────────────▶   │  FastAPI backend         │
│  - Dashboard              │                         │  - routers (REST)        │
│  - Add Solution           │  ◀───────────────────   │  - services (use cases)  │
│  - Problems browser       │                         │  - domain (pure logic)   │
│  - Review (flashcards)    │                         │  - repository (SQLite)   │
│  - Learn (recommendations)│                         │  - vault writer (disk)   │
└───────────────────────────┘                         └───────────┬──────────────┘
                                                                   │
                                           ┌───────────────────────┼───────────────────┐
                                           ▼                       ▼                   ▼
                                   dsa_vault.db (SQLite)   vault/<topic>/*.py   topics.yaml (DAG)
```

## Architecture

### Backend layers

1. **Routers** (`app/routers/`) — thin FastAPI endpoints; validate input via
   Pydantic schemas, call services, map results to responses.
2. **Services** (`app/services/`) — use-case orchestration: capture flow,
   progress aggregation, review session, recommendations. No framework code.
3. **Domain** (`app/domain/`) — pure functions and small classes with no I/O:
   - `slugify.py` — filesystem-safe, idempotent slugs.
   - `complexity.py` — static heuristic Big-O estimator + best-practice rules.
   - `scheduler.py` — spaced-repetition (SM-2-lite) interval scheduling.
   - `streaks.py` — streak and longest-streak computation from activity dates.
   - `learning_path.py` — topic DAG, cycle detection, topological ordering.
   - `language.py` — language detection from code/extension.
4. **Repository** (`app/repository/`) — SQLite persistence via SQLAlchemy Core
   or sqlite3; converts rows to/from domain/record dataclasses.
5. **Vault writer** (`app/vault.py`) — writes/updates the on-disk topic tree.

### Why these boundaries

The domain layer is pure (no DB, no filesystem, no network). That makes
Requirement 9's invariants directly testable with generated inputs, and keeps the
hooks/agent/MCP integrations (other lessons) reading plain files and a plain API.

## Components and Interfaces

### Data model (SQLite)

**problems**
| column        | type    | notes                                   |
|---------------|---------|-----------------------------------------|
| id            | INTEGER | primary key                             |
| title         | TEXT    | e.g., "Two Sum"                         |
| platform      | TEXT    | leetcode/hackerrank/codechef/gfg/other  |
| problem_slug  | TEXT    | stable slug; unique with platform       |
| topic         | TEXT    | topic slug (fk-ish to topics.yaml)      |
| language      | TEXT    | detected or provided                    |
| code          | TEXT    | full source                             |
| explanation   | TEXT    | generated, user-editable                |
| notes         | TEXT    | user free-text                          |
| time_complexity  | TEXT | Big-O or "unknown"                      |
| space_complexity | TEXT | Big-O or "unknown"                      |
| file_path     | TEXT    | relative path in vault/                 |
| created_at    | TEXT    | ISO date (local)                        |
| updated_at    | TEXT    | ISO date (local)                        |

Unique constraint: (`platform`, `problem_slug`) enforces Requirement 1.5.

**flashcards**
| column        | type    | notes                                   |
|---------------|---------|-----------------------------------------|
| id            | INTEGER | primary key                             |
| problem_id    | INTEGER | fk → problems.id                        |
| front         | TEXT    | question                                |
| back          | TEXT    | answer                                  |
| interval_days | INTEGER | current spacing interval                |
| ease          | REAL    | ease factor (SM-2-lite)                 |
| due_date      | TEXT    | ISO date                                |
| last_reviewed | TEXT    | ISO date or null                        |

**activity**
| column   | type    | notes                                    |
|----------|---------|------------------------------------------|
| id       | INTEGER | primary key                              |
| day      | TEXT    | ISO date (local); unique                 |
| kind     | TEXT    | "capture" or "review" (first of day)     |

Streaks are computed from distinct `activity.day` values.

### Domain interfaces (pure)

```python
# slugify.py
def slugify(text: str) -> str: ...          # idempotent, [a-z0-9-]

# language.py
def detect_language(code: str, filename: str | None) -> str: ...

# complexity.py
@dataclass
class ComplexityResult:
    time: str          # e.g. "O(n)", or "unknown"
    space: str
    suggestions: list[str]
def analyze(code: str, language: str) -> ComplexityResult: ...

# scheduler.py
@dataclass
class Card:
    interval_days: int
    ease: float
    due_date: date
    last_reviewed: date | None
def schedule(card: Card, grade: str, today: date) -> Card: ...  # grade in {"again","good","easy"}

# streaks.py
def current_streak(active_days: set[date], today: date) -> int: ...
def longest_streak(active_days: set[date]) -> int: ...

# learning_path.py
class CycleError(Exception): ...
def topological_path(dag: dict[str, list[str]], target: str) -> list[str]: ...
```

### REST API (selected endpoints)

| Method | Path                       | Purpose                                  |
|--------|----------------------------|------------------------------------------|
| POST   | /api/solutions             | Capture a solution (Req 1,2,3,4,6)       |
| GET    | /api/solutions             | List/search problems                     |
| GET    | /api/solutions/{id}        | Get one problem with full detail         |
| PATCH  | /api/solutions/{id}        | Update notes/explanation (Req 4)         |
| GET    | /api/progress              | Streaks, totals, per-topic (Req 5)       |
| GET    | /api/review/due            | Flashcards due today (Req 6)             |
| POST   | /api/review/{cardId}/grade | Grade a card, reschedule (Req 6)         |
| GET    | /api/learn/path?topic=     | Learning path for a topic (Req 7)        |
| GET    | /api/learn/recommend?topic=| Recommended unsolved problems (Req 7)    |

### Capture flow (sequence)

1. Router validates payload (code, title required).
2. Service calls `detect_language` if language absent.
3. Service calls `slugify` for topic and problem slug.
4. Service calls `complexity.analyze` → time/space/suggestions.
5. Service generates an initial explanation (template from analysis + metadata).
6. Repository upserts the problem (unique platform+slug).
7. Vault writer writes `vault/<topic>/<slug>.<ext>` (disambiguates on collision).
8. Service creates flashcards and schedules them (due today initially).
9. Service records today's activity (kind="capture").
10. Router returns the created record + analysis.

## Complexity analyzer heuristic (static)

The analyzer is a transparent heuristic, not an execution engine:

- Parse structure (for Python, use `ast`; for others, use bracket/keyword scans).
- Count maximum loop nesting depth → base polynomial time estimate (depth 1 → O(n),
  depth 2 → O(n^2), ...).
- Detect common patterns: divide-and-conquer recursion → O(log n)/O(n log n);
  single hash-map pass → O(n); sort call → at least O(n log n).
- Space: detect auxiliary structures (lists/sets/dicts/recursion) → O(n), else O(1).
- IF signals conflict or structure is unrecognized THEN return "unknown".
- Best-practice rules per language (e.g., Python: prefer comprehensions, avoid
  `in` on list for membership in loops, use `collections` where apt).

This heuristic is intentionally modest and honest; the README documents its limits.

## Spaced repetition (SM-2-lite)

- New card: `interval_days = 0`, `ease = 2.5`, `due_date = today`.
- grade "again": `interval_days = 1`, `ease = max(1.3, ease - 0.2)`.
- grade "good": `interval_days = max(1, round(interval_days * ease))` (first good → 1 then 3...).
- grade "easy": like good with a small bonus to interval.
- `due_date = today + interval_days` (always strictly after review when interval ≥ 1;
  for the initial same-day case the first grade moves it to a future day). This satisfies
  Requirement 6.5 and the invariant in 9.3.

## Learning path (topic DAG)

- `topics.yaml` declares each topic and its prerequisites.
- `topological_path(dag, target)` returns prerequisites-first order ending at target.
- Cycle detection via DFS coloring; on cycle, raise `CycleError(edge)` → API 400.
- Satisfies Requirements 7.1–7.3 and invariant 9.4.

## On-disk vault layout

```
vault/
  arrays/0001-two-sum.py
  graphs/0200-number-of-islands.py
  dynamic-programming/0070-climbing-stairs.py
```

- Slug collisions get a numeric suffix (`-2`, `-3`) (Req 2.5).
- The tree is committed to git — it is both a feature and the data source the MCP
  server reads (MCP lesson).

## Error Handling

- Validation errors → HTTP 422 with field names (FastAPI/Pydantic default).
- Cycle in learning path → HTTP 400 with offending edge.
- Not found (unknown id) → HTTP 404.
- Vault write failures → HTTP 500 with a safe message; DB transaction rolled back
  so the DB and disk never diverge silently.
- Frontend surfaces all errors as readable toasts/messages (Req 8.3).

## Testing Strategy

- **Property-based (Hypothesis)** on the pure domain modules — the primary focus
  for Lesson 4, targeting the invariants in Requirement 9:
  - slug idempotency and charset.
  - streak ≤ distinct active days; monotonic behavior.
  - scheduler due_date strictly after review date; interval non-negative.
  - topological order validity + every node once; generated DAGs.
  - per-topic counts sum to total.
- **Example-based unit tests** for analyzer heuristics and service flows.
- **API smoke tests** with FastAPI's TestClient for the main endpoints.

## Technology Choices

- **FastAPI + Uvicorn** — typed, fast to build, auto OpenAPI docs for the demo.
- **SQLite via Python stdlib / SQLAlchemy** — zero-install, file-based (confirmed
  present on the target macOS machine).
- **Hypothesis + pytest** — property-based testing (Lesson 4).
- **React + Vite + TypeScript** — fast dev server, clean typed UI.
- **PyYAML** — read the topic DAG.

## Deployment / Run (local, macOS)

- Backend: `python -m venv .venv && source .venv/bin/activate && pip install -r
  backend/requirements.txt && uvicorn app.main:app --reload` (port 8000).
- Frontend: `cd frontend && npm install && npm run dev` (Vite, port 5173, proxied
  to the backend).

# DSA Vault — Implementation Plan

Each task is incremental, references the requirements it satisfies, and is
ordered so the project runs and is testable as early as possible. Lesson-tagged
tasks also note which Kiro University lesson they demonstrate.

- [ ] 1. Scaffold the backend project
  - Create `backend/` with `app/` package, `requirements.txt`, and a `main.py`
    that boots FastAPI with a health endpoint.
  - Set up a `.venv` and install FastAPI, Uvicorn, SQLAlchemy, PyYAML,
    pytest, Hypothesis.
  - _Requirements: 8.1, 8.4_

- [ ] 2. Implement pure domain modules (no I/O)
  - [ ] 2.1 `domain/slugify.py` — idempotent, lowercase, hyphenated slugs.
    - _Requirements: 2.4, 9.1_
  - [ ] 2.2 `domain/language.py` — detect language from code/extension.
    - _Requirements: 1.2_
  - [ ] 2.3 `domain/complexity.py` — static Big-O heuristic + best-practice rules.
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  - [ ] 2.4 `domain/scheduler.py` — SM-2-lite spaced-repetition scheduling.
    - _Requirements: 6.2, 6.4, 6.5, 9.3_
  - [ ] 2.5 `domain/streaks.py` — current and longest streak from activity days.
    - _Requirements: 5.1, 5.2, 5.3, 5.5, 9.2_
  - [ ] 2.6 `domain/learning_path.py` — topic DAG, cycle detection, topo order.
    - _Requirements: 7.1, 7.2, 7.3, 9.4_

- [ ] 3. Persistence and vault writer
  - [ ] 3.1 SQLite schema + repository for problems, flashcards, activity.
    - _Requirements: 1.1, 1.5, 4.2, 4.3_
  - [ ] 3.2 `vault.py` — write/update `vault/<topic>/<slug>.<ext>`, collision-safe.
    - _Requirements: 2.1, 2.2, 2.3, 2.5_

- [ ] 4. Services (use cases)
  - [ ] 4.1 Capture service wiring the full capture flow.
    - _Requirements: 1.1–1.5, 2.*, 3.*, 4.1, 6.1_
  - [ ] 4.2 Progress service (streaks, totals, per-topic breakdown).
    - _Requirements: 5.1, 5.4, 5.5, 9.5_
  - [ ] 4.3 Review service (due cards, grade + reschedule).
    - _Requirements: 6.3, 6.4_
  - [ ] 4.4 Recommendation service (path + unsolved suggestions).
    - _Requirements: 7.2, 7.4_

- [ ] 5. REST API routers
  - Wire all endpoints from the design's API table; Pydantic schemas; error
    mapping (422/400/404/500).
  - _Requirements: 8.1, 8.3_

- [ ] 6. [Lesson 4] Property-based tests with Hypothesis
  - [ ] 6.1 Slug idempotency & charset
    - `slugify(slugify(s)) == slugify(s)` for any text `s`.
    - Output matches `^[a-z0-9]+(-[a-z0-9]+)*$` or is empty; no leading/trailing
      or doubled hyphens; no uppercase or whitespace.
    - _Requirements: 2.4, 9.1_
  - [ ] 6.2 Language detection total & stable
    - `detect_language` returns a value from the known set for any input and
      never raises; same input always yields the same result.
    - _Requirements: 1.2_
  - [ ] 6.3 Complexity analyzer safety
    - `analyze` never raises on arbitrary strings, always returns Big-O-shaped
      strings or "unknown", and never executes the input.
    - _Requirements: 3.1, 3.2, 3.4_
  - [ ] 6.4 Scheduler monotonicity (spaced repetition)
    - For any card and any grade, the new `due_date` is strictly after the
      review date (`today`); `interval_days >= 0`; `ease >= 1.3`.
    - Grade "again" never produces a larger interval than grade "good" from the
      same card.
    - _Requirements: 6.4, 6.5, 9.3_
  - [ ] 6.5 Streak bounds & reset
    - `current_streak(active_days, today) <= len(active_days)` and
      `<= days elapsed since first active day`; never negative.
    - A gap day before today forces `current_streak == 0` unless today is active.
    - `longest_streak >= current_streak` for the same day set.
    - _Requirements: 5.1, 5.2, 5.3, 9.2_
  - [ ] 6.6 Learning-path topological validity
    - On any generated acyclic DAG, `topological_path` returns every reachable
      topic exactly once (no duplicates, no omissions) and never places a topic
      before one of its prerequisites.
    - On any generated DAG with an injected cycle, it raises `CycleError`.
    - _Requirements: 7.1, 7.2, 7.3, 9.4_
  - [ ] 6.7 Per-topic counts reconcile
    - The sum of per-topic solved counts always equals the total solved count
      for any generated set of problem records.
    - _Requirements: 5.4, 5.5, 9.5_

- [ ] 7. [Lesson 3] Agent hook
  - Hook that, on new solution file in `vault/`, triggers a progress/flashcard
    refresh (and/or a daily review reminder).
  - _Requirements: 5.*, 6.*_

- [ ] 8. [Lesson 6] Custom agent
  - A scoped "complexity & best-practices analyzer" agent definition that reviews
    a solution and returns complexity + suggestions.
  - _Requirements: 3.1, 3.3_

- [ ] 9. [Lesson 5] MCP server config
  - Configure a filesystem/git MCP server pointed at the `vault/` tree so Kiro can
    read the organized solutions.
  - _Requirements: 2.1_

- [ ] 10. [Lesson 7] Package a Kiro Power
  - Package the analyzer/flashcard capability as a reusable Power.
  - _Requirements: 3.*, 6.*_

- [ ] 11. React frontend
  - [ ] 11.1 Scaffold Vite + TS app, API client, routing, dev proxy to backend.
    - _Requirements: 8.2, 8.4_
  - [ ] 11.2 Dashboard view (progress + due cards).
    - _Requirements: 5.*, 6.3_
  - [ ] 11.3 Add Solution view (paste/upload → analysis preview → save).
    - _Requirements: 1.*, 3.*_
  - [ ] 11.4 Problems browser (list/search, detail with code/explanation/notes).
    - _Requirements: 1.1, 4.*_
  - [ ] 11.5 Review view (flashcard session with grading).
    - _Requirements: 6.3, 6.4_
  - [ ] 11.6 Learn view (topic path + recommendations).
    - _Requirements: 7.2, 7.4_

- [ ] 12. Documentation and verification
  - README with run instructions and a lesson-by-lesson writeup; verify the app
    runs end-to-end and tests pass.
  - _Requirements: 8.4_

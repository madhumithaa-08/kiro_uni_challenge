# Tech — DSA Vault

## Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn. Persistence: SQLite via the Python
  stdlib `sqlite3` (zero-install, file-based). YAML via PyYAML for the topic DAG.
- **Testing:** pytest + Hypothesis (property-based testing is a first-class
  requirement, not optional).
- **Frontend:** React + Vite + TypeScript. Plain fetch-based API client.
- **Runtime target:** local macOS (Apple Silicon, arm64). No cloud services.

## Backend conventions

- **Layering is strict:**
  - `app/domain/` — pure functions/classes. NO I/O (no DB, no filesystem, no
    network, no `datetime.now()` inside pure logic — pass `today`/clock in).
  - `app/repository/` — all SQLite access. Returns dataclasses/dicts, not rows.
  - `app/vault.py` — all filesystem writes for the organized code tree.
  - `app/services/` — use-case orchestration; composes domain + repository + vault.
  - `app/routers/` — thin FastAPI endpoints; Pydantic schemas in/out only.
- **Purity enables testing.** Domain functions must be deterministic given their
  inputs so Hypothesis can test invariants. Inject the current date explicitly.
- **Type hints everywhere.** Public functions are fully annotated.
- **Dataclasses** for internal domain structures; **Pydantic** only at the API
  boundary.
- **Errors:** raise domain-specific exceptions in domain/services; map to HTTP
  status in routers (422 validation, 400 bad request/cycle, 404 not found,
  500 internal). Never leak stack traces to clients.
- **No code execution.** The complexity analyzer parses/inspects source text
  statically. It must never `exec`/`eval`/subprocess user code.
- **Determinism for generated content.** Given the same solution, explanation and
  flashcards should be reproducible (no randomness in core generation).

## Frontend conventions

- TypeScript strict mode. Functional components + hooks.
- One typed API client module; components never call `fetch` directly.
- Every network call handles loading and error states; errors shown to the user.
- Keep styling simple and clean (a single lightweight stylesheet or CSS modules);
  prioritize clarity over visual complexity given the timeline.

## Dependencies

- Prefer the standard library. Add a dependency only when it clearly earns its
  place. Pin versions in `requirements.txt` / `package.json`.
- Do not add a heavyweight ORM if `sqlite3` + small helpers suffice.

## Testing policy

- Pure domain modules MUST have Hypothesis property tests for their invariants
  (see requirements §9).
- Services and routers get example-based tests (pytest + FastAPI TestClient).
- Tests must run offline and leave no stray files (use temp dirs/in-memory DB).

## Commands

- Backend deps: `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`
- Run backend: `uvicorn app.main:app --reload` (from `backend/`, port 8000)
- Run tests: `pytest` (from `backend/`)
- Frontend: `cd frontend && npm install && npm run dev` (port 5173)

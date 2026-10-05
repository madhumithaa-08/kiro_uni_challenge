# DSA Vault

A local-first personal tracker and notes tool for Data Structures & Algorithms
practice. Capture a solution **once** — DSA Vault detects the language, analyzes
time/space complexity, files the code under its topic, generates an explanation,
tracks your daily streak, and builds spaced-repetition flashcards so you actually
remember what you solved.

Built with [Kiro](https://kiro.dev) for the **Kiro University Challenge 2026**.

> Replaces the "paste my LeetCode solution into Notepad and lose track in a week"
> habit with an organized, analyzed, revisable personal archive.

---

## What it does

- **Capture once, automate the rest.** Paste a solution → language detection →
  static complexity analysis → topic filing → explanation draft → flashcards.
- **Organized codebase on disk.** Every solution is written to
  `vault/<topic>/<slug>.<ext>`, so your repo doubles as a browsable archive.
- **Progress & streaks.** Current/longest streak, total solved, per-topic coverage.
- **Spaced-repetition review.** SM-2-lite scheduling resurfaces cards when due.
- **Learning paths.** Pick a topic → get a prerequisite-ordered study path.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python 3.12, FastAPI, SQLite (stdlib), PyYAML |
| Testing | pytest + Hypothesis (property-based) |
| Frontend | React + Vite + TypeScript |
| Runtime | Local, macOS/Linux. No cloud services required. |

## Architecture

```
frontend (React/Vite/TS)  ──/api──▶  FastAPI backend
                                     ├─ routers/   (REST endpoints)
                                     ├─ services/  (use cases)
                                     ├─ domain/    (PURE logic — property-tested)
                                     ├─ repository/(SQLite)
                                     └─ vault.py   (writes vault/<topic>/<slug>)
                                            │
                        dsa_vault.db ◀──────┼──────▶ vault/   topics.yaml (DAG)
```

The `domain/` layer is pure (no I/O), which is what makes the property-based
tests meaningful — the invariants are tested directly against generated inputs.

## Run it locally

**Backend** (port 8000):
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend** (port 5173, proxies `/api` to the backend):
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

**Tests:**
```bash
cd backend && ./.venv/bin/python -m pytest -q      # 32 passed
```

**CLI** (also used by the hooks):
```bash
cd backend
./.venv/bin/python -m app.cli progress     # streak + totals
./.venv/bin/python -m app.cli due          # flashcards due today
./.venv/bin/python -m app.cli sync-index   # rebuild vault/INDEX.md
```

---

## How each Kiro University lesson was incorporated

> One line per lesson, as the entry form asks. File paths point to the artifact.

1. **Spec-driven development** — The whole project was specced before coding in
   [`.kiro/specs/dsa-vault/`](.kiro/specs/dsa-vault/): `requirements.md` (9
   EARS-style requirements), `design.md` (architecture, data model, API,
   sequence), and `tasks.md` (numbered tasks referencing requirements).

2. **Steering documents** — Project conventions in
   [`.kiro/steering/`](.kiro/steering/) (`product.md`, `tech.md`, `structure.md`)
   enforce the pure-domain layering, type hints, "no code execution," and the
   "honest over flashy" principle that shaped every file Kiro wrote.

3. **Hooks** — Two agent hooks in [`.kiro/hooks/`](.kiro/hooks/):
   `dsa-vault-sync-index` (PostFileSave on a `vault/` solution → rebuilds
   `vault/INDEX.md`) and `dsa-vault-daily-review` (SessionStart → surfaces due
   flashcards and streak). Backed by `backend/app/cli.py`.

4. **Property-based testing** — Hypothesis tests in
   [`backend/tests/`](backend/tests/) prove core invariants over hundreds of
   generated inputs: slug idempotency, scheduler due-date > review-date,
   streak ≤ active days, learning-path topological validity + cycle detection,
   per-topic counts == total. **32 tests pass.**

5. **Powers** — The analyzer + flashcard workflow is packaged as a reusable Kiro
   Power in [`powers/dsa-vault/`](powers/dsa-vault/) (`POWER.md` manifest +
   `steering/workflow.md`), following Kiro's installed-power format.

6. **MCP (Model Context Protocol)** — [`.kiro/settings/mcp.json`](.kiro/settings/mcp.json)
   configures a filesystem MCP server (`vault-fs`) scoped **read-only** to the
   `vault/` tree, so Kiro can read and search the organized solution archive.

7. **Custom agents** — [`.kiro/agents/complexity-reviewer.md`](.kiro/agents/complexity-reviewer.md)
   defines a scoped, read-only "Complexity & Best-Practices Reviewer" agent
   (`fs_write` denied; shell limited to the analyzer) that reports Big-O
   complexity and improvement suggestions for a solution.

**Bonus Lesson 2 (package a power):** satisfied by the Power in
`powers/dsa-vault/` (same artifact as Lesson 5/Powers above).

**Bonus Lesson 1 (Kiro Web / cloud session, paid plans):** performed by running
a Kiro session on the Web surface (not a repo artifact — ticked on the entry
form).

---

## Project layout

```
.kiro/
  specs/dsa-vault/   # Lesson: spec-driven development
  steering/          # Lesson: steering
  hooks/             # Lesson: hooks (+ kironomics campaign hook)
  agents/            # Lesson: custom agents
  settings/mcp.json  # Lesson: MCP
backend/             # FastAPI + SQLite + pure domain + Hypothesis tests
frontend/            # React + Vite + TypeScript UI
powers/dsa-vault/    # Lesson: packaged Kiro Power
vault/               # organized solutions by topic (data for the MCP server)
```

## Honesty / scope notes

- The complexity analyzer is a **transparent static heuristic** (loop-nesting +
  pattern signals). It never executes your code and reports **"unknown"** when it
  can't be sure rather than guessing. It can over-report on clever solutions
  (e.g. flood-fill looks like nested loops) — the custom agent is instructed to
  trust reasoning over the heuristic.
- **Capture is a fast manual/paste action**, not automatic scraping from judge
  platforms. True auto-sync (a browser extension) is intentional **future work**.

## License

MIT.

---

Built by [@madhumithaa-08](https://github.com/madhumithaa-08) with Kiro, as part
of the AWS User Group Madurai Kiro University build-along.

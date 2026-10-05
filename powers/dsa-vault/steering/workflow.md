# DSA Vault Power — Workflow

This steering guide defines how to use the DSA Vault Power to analyze a solution
and produce review flashcards.

## Step 1 — Read the solution

Accept the solution as a file path (e.g. `vault/arrays/0001-two-sum.py`), an open
editor file, or pasted code. Note the language and the problem title/topic if
given.

## Step 2 — Analyze complexity

Determine time and space complexity in Big-O. Reasoning checklist:

- Dominant operation and the input size `n` (plus `m`, `V`, `E` where relevant).
- Loop nesting depth → polynomial degree.
- Library calls: sorting ≥ O(n log n); hash set/dict membership O(1) average.
- Recursion: branching factor and depth; account for call-stack space.
- Auxiliary data structures and output size for space.

If signals conflict or the structure is unrecognizable, report **"unknown"** and
explain why. Never guess a precise bound you cannot justify.

Optionally cross-check against the reference analyzer shipped with the app:

```
cd backend && ./.venv/bin/python -c "from app.domain.complexity import analyze; print(analyze(open('<path>').read(), '<language>'))"
```

Treat it as a second opinion only. The heuristic counts loop nesting, so it can
over-report (e.g. flood-fill that visits each cell once still looks like nested
loops). Trust reasoning over the heuristic and note any disagreement.

## Step 3 — Suggest best practices

List concrete, actionable improvements: better data structures, removing
redundant work, early exits, idiomatic usage, and edge-case handling. Keep it to
a few high-value bullets. If the solution is already good, say so and why.

## Step 4 — Generate flashcards

Produce 2–4 flashcards (front/back) covering:

1. The core approach / key insight.
2. The time & space complexity (with the one-line justification).
3. The main improvement or pitfall (if any).
4. The topic and a sibling problem to recall.

Cards must be deterministic for the same input (no randomness) so a deck is
reproducible.

## Output format

```
Time:  O(...) — why
Space: O(...) — why
Suggestions:
  - ...
Flashcards:
  1. Q: ...
     A: ...
  2. Q: ...
     A: ...
```

Keep everything concise and student-friendly. Explain the "why"; skip filler.

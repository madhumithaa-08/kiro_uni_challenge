---
name: "dsa-vault"
displayName: "DSA Vault — analyze & remember solutions"
description: "Analyze DSA solutions for time/space complexity and best practices, then generate spaced-repetition flashcards to remember them."
keywords: ["dsa", "algorithms", "complexity", "big-o", "flashcards", "spaced-repetition", "study", "leetcode"]
author: "madhumithaa-08"
version: "1.0.0"
license: "MIT"
---

# DSA Vault Power

## Overview

The DSA Vault Power packages a focused study workflow for data-structures and
algorithms practice: given a solution, it (1) estimates **time and space
complexity** with a transparent static heuristic, (2) suggests concrete
**best-practice** improvements, and (3) generates **spaced-repetition
flashcards** so the key ideas are actually retained.

It is the reusable, installable form of the analyzer and flashcard engine that
powers the DSA Vault application. Point it at a solution file or paste code, and
it returns an analysis plus a set of review cards.

## When to use

- Right after solving a problem on LeetCode / HackerRank / CodeChef / GFG, to
  record *why* the solution works and how costly it is.
- When reviewing an old solution and you want a quick complexity sanity check.
- When building a personal revision deck from your solved problems.

## Available steering files

- **workflow.md** — the step-by-step analyze-then-flashcard workflow, the output
  format, and the honesty rules (say "unknown" rather than guessing).

Read it with: `kiroPowers` action="readSteering", powerName="dsa-vault",
steeringFile="workflow.md".

## What it does (capabilities)

1. **Complexity analysis** — loop-nesting + pattern heuristics (hashing → O(1)
   lookups, sorting → O(n log n), recursion → stack space). Static only; never
   executes the analyzed code.
2. **Best-practice suggestions** — language-aware tips (e.g. prefer sets for
   membership tests in loops, avoid quadratic string concatenation).
3. **Flashcard generation** — deterministic cards covering approach, complexity,
   improvements, and topic linkage, ready for a spaced-repetition schedule.

## How it relates to the DSA Vault app

The app (FastAPI backend) exposes the same logic over HTTP; this Power packages
the capability so it can be used directly inside Kiro without running the server.
The backend module `app/domain/complexity.py` is the reference implementation,
and `app/domain/generate.py` produces the flashcards.

## Honesty principle

The analyzer is a heuristic and can be wrong on clever solutions. The workflow
instructs the agent to cross-check with reasoning and to report **"unknown"**
when complexity genuinely cannot be determined, rather than inventing a value.

## License

MIT. Attribution: AWS User Group Madurai — Kiro University build-along.

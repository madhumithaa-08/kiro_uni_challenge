# Product — DSA Vault

DSA Vault is a local-first personal tracker and notes tool for Data Structures &
Algorithms practice. It exists to replace the "paste code into Notepad" habit
that goes stale after a week.

## Who it is for

Engineering students and early-career developers who grind problems on LeetCode,
HackerRank, CodeChef, and GeeksforGeeks and want their work organized, explained,
and retained — without manual bookkeeping.

## Core promise

Capture a solution **once**; the tool automates everything after:
- organizes the code by topic (both in-app and as an on-disk folder tree),
- analyzes time/space complexity and suggests best practices,
- generates an explanation and lets the user add personal notes,
- tracks daily progress and streaks,
- builds spaced-repetition flashcards for revision,
- recommends what to study next for a chosen topic.

## Product principles

1. **Local and private.** No accounts, no cloud, no telemetry. Everything lives
   on the user's machine and in their own git repository.
2. **Automate after capture.** The only manual step is capturing the solution.
   Analysis, organization, explanation, flashcards, and progress are automatic.
3. **Honest over flashy.** The complexity analyzer is a transparent static
   heuristic. When unsure, it says "unknown" rather than guessing.
4. **The repo is a feature.** The organized `vault/` tree is both a user benefit
   and a readable artifact others (and tools) can browse.
5. **Retention matters.** Capturing is pointless if nothing is remembered;
   spaced-repetition review is a first-class feature, not an add-on.

## Explicitly out of scope (this version)

- Automatic scraping/sync from judge platforms (future work; capture is manual).
- Multi-user, auth, hosting.
- Executing or sandboxing user code (analysis is static only).

## Tone for generated content

Explanations and suggestions should be concise, concrete, and student-friendly:
plain language, no filler, focused on the "why" behind the approach.

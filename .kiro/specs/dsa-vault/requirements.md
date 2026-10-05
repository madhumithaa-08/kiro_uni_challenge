# DSA Vault — Requirements

## Introduction

DSA Vault is a personal Data Structures & Algorithms tracker and notes tool for
students and engineers who practice on platforms like LeetCode, HackerRank,
CodeChef, and GeeksforGeeks. Today, practitioners copy their solutions into
scattered notes that quickly go stale. DSA Vault replaces that habit: you
capture a solution once, and the tool automatically organizes it by topic,
analyzes its complexity, generates an explanation, tracks your daily progress,
and builds spaced-repetition flashcards so key ideas stick.

The product is a full-stack application — a FastAPI + SQLite backend exposing a
REST API, and a React (Vite + TypeScript) frontend — that runs entirely on the
user's machine with no cloud dependency.

### Goals

- Make capturing a solved problem a single action, then automate everything after.
- Keep every solution organized by topic, both in a searchable app and as a
  browsable on-disk code tree committed to the repository.
- Help the user retain what they learn through spaced-repetition flashcards.
- Surface progress (streaks, counts, topic coverage) to sustain the habit.
- Recommend what to study next based on the user's chosen topic and history.

### Non-Goals (current version)

- Automatic scraping/sync from external judge platforms (LeetCode, etc.). This
  requires a browser extension or private APIs and is deferred to future work.
  Capture is a fast manual/CLI/UI action; everything after capture is automated.
- Multi-user accounts, authentication, or hosting. Single local user only.
- Executing or sandboxing submitted code. Analysis is static only.

### Glossary

- **Problem**: a single coding challenge (e.g., "Two Sum") the user has solved.
- **Solution**: the user's code for a problem, in one language, plus notes.
- **Topic**: a DSA category (arrays, graphs, dynamic-programming, ...).
- **Flashcard**: a question/answer pair derived from a problem for revision.
- **Streak**: count of consecutive calendar days with at least one activity.
- **Review**: a spaced-repetition session over flashcards that are due.

---

## Requirements

### Requirement 1 — Capture a solution

**User story:** As a student, I want to paste or upload a solution once, so that
I don't have to manually organize and annotate it.

#### Acceptance Criteria

1. WHEN the user submits a solution with code, title, platform, and topic THEN
   the system SHALL create a stored problem record with a unique identifier.
2. WHEN the user submits a solution without specifying the programming language
   THEN the system SHALL detect the language from the code and/or file extension.
3. IF a required field (code or title) is missing THEN the system SHALL reject
   the request and return a validation error naming the missing field.
4. WHEN a solution is captured THEN the system SHALL record the capture timestamp
   in the user's local date for progress tracking.
5. WHEN the same problem (same platform + problem slug) is captured again THEN
   the system SHALL update the existing record rather than create a duplicate.

### Requirement 2 — Organize solutions by topic on disk

**User story:** As a user, I want all my code organized into topic folders, so
that my repository doubles as a clean, browsable solution archive.

#### Acceptance Criteria

1. WHEN a solution is captured THEN the system SHALL write the code to a file
   under `vault/<topic-slug>/<problem-slug>.<ext>`.
2. WHERE a topic has no folder yet THE system SHALL create the topic folder.
3. WHEN a solution's code or topic changes THEN the system SHALL update the file
   on disk so the tree stays consistent with the database.
4. THE system SHALL use a filesystem-safe, lowercase, hyphenated slug for topic
   and problem folder/file names.
5. IF two different problems would map to the same file path THEN the system
   SHALL disambiguate the file name so neither solution is overwritten.

### Requirement 3 — Analyze complexity and best practices

**User story:** As a learner, I want the tool to estimate time/space complexity
and suggest best practices, so that I understand and improve my solutions.

#### Acceptance Criteria

1. WHEN a solution is captured THEN the system SHALL produce an estimated time
   complexity and space complexity in Big-O notation.
2. WHEN the analyzer cannot determine complexity with confidence THEN the system
   SHALL return "unknown" rather than a misleading estimate.
3. WHEN a solution is analyzed THEN the system SHALL return zero or more
   best-practice suggestions relevant to the detected language.
4. THE complexity analysis SHALL be static only and SHALL NOT execute the code.

### Requirement 4 — Explanations and personal notes

**User story:** As a user, I want each solution to carry an explanation and a
space for my own comments, so that I remember the key points.

#### Acceptance Criteria

1. WHEN a solution is captured THEN the system SHALL generate an initial
   explanation summarizing the approach.
2. THE system SHALL allow the user to edit the explanation and SHALL persist
   the user's edits.
3. THE system SHALL provide a free-text notes field per problem that the user
   can create and update at any time.
4. WHEN notes or explanation are updated THEN the system SHALL preserve all
   other fields of the record unchanged.

### Requirement 5 — Daily progress and streaks

**User story:** As a user, I want to see my streak and progress, so that I stay
motivated to practice daily.

#### Acceptance Criteria

1. THE system SHALL compute the current streak as the number of consecutive
   calendar days ending today that have at least one captured solution or review.
2. WHEN a day passes with no activity THEN the system SHALL reset the current
   streak to zero on the next active day.
3. THE current streak SHALL never exceed the number of days elapsed since the
   first recorded activity.
4. THE system SHALL report total problems solved and a per-topic breakdown.
5. THE system SHALL report the longest streak ever achieved.

### Requirement 6 — Flashcards and spaced-repetition review

**User story:** As a user, I want flashcards that resurface on a schedule, so
that I revise key points efficiently.

#### Acceptance Criteria

1. WHEN a solution is captured THEN the system SHALL create at least one
   flashcard derived from the problem (e.g., approach, complexity, pitfall).
2. THE system SHALL schedule each flashcard with a due date using a
   spaced-repetition algorithm.
3. WHEN the user starts a review THEN the system SHALL present only flashcards
   whose due date is on or before today.
4. WHEN the user grades a card recall as "good" THEN the system SHALL increase
   the interval; WHEN graded "again" THEN the system SHALL reset the interval.
5. THE next due date for a card SHALL always be strictly after the date it was
   last reviewed.

### Requirement 7 — Learning path and recommendations

**User story:** As a user, I want recommended next problems and a learning path
for a topic, so that I know what to study next.

#### Acceptance Criteria

1. THE system SHALL model topic prerequisites as a directed acyclic graph (DAG).
2. WHEN the user selects a topic THEN the system SHALL return an ordered learning
   path respecting prerequisite order (topological order).
3. IF a prerequisite cycle is ever introduced THEN the system SHALL reject it and
   report the offending edge rather than producing an invalid path.
4. WHEN the user requests recommendations for a topic THEN the system SHALL
   suggest problems the user has not yet solved, prioritized by that topic and
   its prerequisites.

### Requirement 8 — REST API and frontend

**User story:** As a user, I want a clean web UI backed by an API, so that I can
use the tool comfortably.

#### Acceptance Criteria

1. THE backend SHALL expose a REST API covering capture, retrieval, listing,
   progress, review, and recommendations.
2. THE frontend SHALL provide views for: dashboard (progress + due cards), add
   solution, browse/search problems, review session, and learn/recommendations.
3. WHEN the API returns an error THEN the frontend SHALL display a readable
   message rather than failing silently.
4. THE frontend and backend SHALL run locally on the user's macOS machine with
   documented start commands.

### Requirement 9 — Correctness guarantees (testable invariants)

**User story:** As a maintainer, I want core logic covered by property-based
tests, so that invariants hold across many generated inputs.

#### Acceptance Criteria

1. THE slug function SHALL be idempotent: slugging an already-slugged string
   SHALL return the same string.
2. THE streak computation SHALL never return a value greater than the count of
   distinct active days.
3. THE spaced-repetition scheduler SHALL never produce a due date earlier than
   the review date.
4. THE learning-path builder SHALL return every topic exactly once and SHALL
   never place a topic before one of its prerequisites.
5. THE per-topic solved counts SHALL always sum to the total solved count.

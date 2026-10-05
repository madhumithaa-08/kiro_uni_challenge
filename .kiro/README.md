# .kiro — Kiro University lesson artifacts

This folder contains the Kiro configuration that demonstrates each required
lesson for the Kiro University Challenge. Every item below is committed to this
public repo.

| Lesson | Artifact (path) |
|---|---|
| Spec-driven development | `.kiro/specs/dsa-vault/` (requirements.md, design.md, tasks.md) |
| Steering documents | `.kiro/steering/` (product.md, tech.md, structure.md) |
| Hooks (custom, not Kironomics) | `.kiro/hooks/dsa-vault-sync-index.json`, `.kiro/hooks/dsa-vault-daily-review.json` |
| Property-based testing | `backend/tests/` (Hypothesis), `hypothesis` in `backend/requirements.txt` |
| MCP (Model Context Protocol) | `.kiro/settings/mcp.json` (server `vault-fs`) |
| Custom agents | `.kiro/agents/complexity-reviewer.md` |
| Powers | `powers/dsa-vault/` (POWER.md + steering/workflow.md) |

## Custom hooks (these are the project's own, separate from the Kironomics
## tracking hook that the campaign setup installed)

- **dsa-vault-sync-index** — `PostFileSave` on a solution under `vault/`:
  rebuilds `vault/INDEX.md` so the browsable archive stays in sync.
- **dsa-vault-daily-review** — `SessionStart`: surfaces flashcards due today and
  the current streak.

The Kironomics hook (`.kiro/hooks/kironomics.json`) is only for campaign usage
tracking and is intentionally not counted as the project's hook.

## Custom agent

- **complexity-reviewer** (`.kiro/agents/complexity-reviewer.md`) — a scoped,
  read-only agent that reports time/space complexity and best-practice
  suggestions for a DSA solution. `fs_write` is denied; shell is limited to the
  project analyzer.

## MCP server

- **vault-fs** (`.kiro/settings/mcp.json`) — a filesystem MCP server scoped
  read-only to the `./vault` tree so Kiro can read and search the organized
  solution archive.

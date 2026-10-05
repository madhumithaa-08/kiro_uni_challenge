# DSA Vault Power

A packaged Kiro Power that bundles the DSA Vault **complexity analyzer** and
**flashcard generator** into a reusable study workflow.

## Contents

```
powers/dsa-vault/
├── POWER.md              # Power manifest (frontmatter) + overview
├── steering/
│   └── workflow.md       # the analyze → suggest → flashcard workflow
└── README.md             # this file
```

This follows Kiro's Power layout: a `POWER.md` with `name`, `displayName`,
`description`, `keywords`, and `author` in the frontmatter, plus a `steering/`
folder with workflow guidance. It mirrors the structure of installed powers
(e.g. the `strands` power at `~/.kiro/powers/installed/strands/`).

## What it does

- Estimates time/space complexity of a solution (static heuristic, no execution).
- Suggests best-practice improvements.
- Generates deterministic spaced-repetition flashcards.

The reference implementation lives in the app backend:
- `backend/app/domain/complexity.py` — the analyzer
- `backend/app/domain/generate.py` — the flashcard generator

## Installing it locally

To use it as an installed power, copy it into your Kiro powers directory:

```bash
mkdir -p ~/.kiro/powers/installed/dsa-vault
cp -R powers/dsa-vault/* ~/.kiro/powers/installed/dsa-vault/
```

Then reload Kiro. Read its workflow with:

```
kiroPowers action="readSteering" powerName="dsa-vault" steeringFile="workflow.md"
```

## License

MIT.

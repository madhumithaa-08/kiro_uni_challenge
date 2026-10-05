# Structure — DSA Vault

## Repository layout

```
kiro_uni_challenge/
├── .kiro/
│   ├── specs/dsa-vault/        # Lesson 1: requirements, design, tasks
│   ├── steering/               # Lesson 2: these convention docs
│   ├── hooks/                  # Lesson 3 (+ existing kironomics hook)
│   ├── agents/                 # Lesson 7: custom agent definition(s)
│   ├── settings/mcp.json       # Lesson 6: MCP server config
│   └── ugmdu.json              # campaign manifest (do not delete)
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app factory + health
│   │   ├── domain/             # PURE logic (property-tested)
│   │   │   ├── slugify.py
│   │   │   ├── language.py
│   │   │   ├── complexity.py
│   │   │   ├── scheduler.py
│   │   │   ├── streaks.py
│   │   │   └── learning_path.py
│   │   ├── repository/         # SQLite access
│   │   ├── services/           # use cases
│   │   ├── routers/            # REST endpoints
│   │   ├── schemas.py          # Pydantic request/response models
│   │   └── vault.py            # on-disk topic tree writer
│   ├── tests/                  # pytest + Hypothesis
│   ├── topics.yaml             # topic DAG (prerequisites)
│   └── requirements.txt
├── frontend/                   # React + Vite + TS
│   └── src/
│       ├── api/                # typed API client
│       ├── pages/              # Dashboard, Add, Problems, Review, Learn
│       └── components/
├── vault/                      # organized solutions: <topic>/<slug>.<ext>
└── README.md                   # run guide + lesson-by-lesson writeup
```

## Naming conventions

- Python modules & functions: `snake_case`. Classes: `PascalCase`.
- Topic slugs and problem slugs: lowercase, hyphenated, filesystem-safe
  (`dynamic-programming`, `0001-two-sum`).
- React components: `PascalCase` files; hooks `useXxx`.
- Tests mirror the module they cover: `tests/test_<module>.py`.

## File placement rules

- New pure logic → `backend/app/domain/` only (keep it I/O-free).
- Anything touching SQLite → `backend/app/repository/`.
- Anything touching the filesystem `vault/` tree → `backend/app/vault.py`.
- New endpoints → `backend/app/routers/`, with schemas in `schemas.py`.
- Never write app data into `.kiro/`; the vault lives at the repo root `vault/`.

## Important: .kiro must stay committed

The `.kiro/` folder is how the challenge is scored. Never add `.kiro` to
`.gitignore`. The `vault/` tree should also be committed — it is the data the
MCP server reads and part of the project's value.

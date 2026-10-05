"""Runtime configuration and shared paths.

Paths resolve relative to the repository root so the ``vault/`` tree and the
SQLite file sit at predictable locations. Overridable via env vars for tests.
"""

from __future__ import annotations

import os
from pathlib import Path

# backend/app/config.py -> repo root is two parents up from this file's dir.
_APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = _APP_DIR.parent
REPO_ROOT = BACKEND_DIR.parent


def db_path() -> Path:
    override = os.environ.get("DSA_VAULT_DB")
    if override:
        return Path(override)
    return BACKEND_DIR / "dsa_vault.db"


def vault_root() -> Path:
    override = os.environ.get("DSA_VAULT_ROOT")
    if override:
        return Path(override)
    return REPO_ROOT / "vault"


def topics_file() -> Path:
    override = os.environ.get("DSA_VAULT_TOPICS")
    if override:
        return Path(override)
    return BACKEND_DIR / "topics.yaml"

"""Shared dependencies: a single Database instance and the vault root."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from .config import db_path, vault_root
from .repository.db import Database


@lru_cache(maxsize=1)
def get_db() -> Database:
    return Database(db_path())


def get_vault_root() -> Path:
    root = vault_root()
    root.mkdir(parents=True, exist_ok=True)
    return root

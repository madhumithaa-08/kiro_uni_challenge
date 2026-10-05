"""Example-based API smoke tests (FastAPI TestClient).

Hermetic: points the app at a temp DB and temp vault via env vars before import.
"""

import importlib
import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture()
def client():
    tmp = tempfile.mkdtemp()
    os.environ["DSA_VAULT_DB"] = str(Path(tmp) / "test.db")
    os.environ["DSA_VAULT_ROOT"] = str(Path(tmp) / "vault")

    # Reload modules that cache paths so the env overrides take effect.
    from app import config, deps  # noqa: WPS433
    importlib.reload(config)
    importlib.reload(deps)
    deps.get_db.cache_clear()

    from app.main import create_app
    from fastapi.testclient import TestClient

    return TestClient(create_app())


def test_health(client) -> None:
    assert client.get("/api/health").json()["status"] == "ok"


def test_capture_and_retrieve(client) -> None:
    payload = {
        "title": "Valid Parentheses",
        "code": "def f(s):\n    stack = []\n    return not stack\n",
        "topic": "Stack",
        "platform": "leetcode",
        "problem_slug": "0020-valid-parentheses",
    }
    r = client.post("/api/solutions", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["language"] == "python"
    assert body["file_path"] == "stack/0020-valid-parentheses.py"

    got = client.get(f"/api/solutions/{body['id']}")
    assert got.status_code == 200
    assert got.json()["title"] == "Valid Parentheses"


def test_validation_rejects_missing_code(client) -> None:
    r = client.post("/api/solutions", json={"title": "x", "topic": "arrays"})
    assert r.status_code == 422


def test_unknown_solution_is_404(client) -> None:
    assert client.get("/api/solutions/99999").status_code == 404


def test_learn_path_cycle_free(client) -> None:
    r = client.get("/api/learn/path", params={"topic": "dynamic-programming"})
    assert r.status_code == 200
    path = r.json()["path"]
    assert path[-1] == "dynamic-programming"
    assert "recursion" in path


def test_learn_path_unknown_topic_404(client) -> None:
    assert client.get("/api/learn/path", params={"topic": "nonsense"}).status_code == 404

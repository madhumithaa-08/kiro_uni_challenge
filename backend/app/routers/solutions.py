"""Solution capture, listing, retrieval, and update endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from ..deps import get_db, get_vault_root
from ..schemas import SolutionCreate, SolutionOut, SolutionUpdate
from ..services.capture import capture_solution

router = APIRouter(prefix="/api/solutions", tags=["solutions"])


def _to_out(row: dict) -> SolutionOut:
    return SolutionOut(**{k: row[k] for k in SolutionOut.model_fields})


@router.post("", response_model=SolutionOut, status_code=201)
def create_solution(payload: SolutionCreate) -> SolutionOut:
    db = get_db()
    stored = capture_solution(
        db,
        get_vault_root(),
        title=payload.title,
        code=payload.code,
        topic=payload.topic,
        platform=payload.platform,
        language=payload.language,
        problem_slug=payload.problem_slug,
        notes=payload.notes,
    )
    return _to_out(stored)


@router.get("", response_model=list[SolutionOut])
def list_solutions(search: str | None = None, topic: str | None = None) -> list[SolutionOut]:
    db = get_db()
    return [_to_out(r) for r in db.list_problems(search=search, topic=topic)]


@router.get("/{solution_id}", response_model=SolutionOut)
def get_solution(solution_id: int) -> SolutionOut:
    db = get_db()
    row = db.get_problem(solution_id)
    if row is None:
        raise HTTPException(status_code=404, detail="solution not found")
    return _to_out(row)


@router.patch("/{solution_id}", response_model=SolutionOut)
def update_solution(solution_id: int, payload: SolutionUpdate) -> SolutionOut:
    db = get_db()
    if db.get_problem(solution_id) is None:
        raise HTTPException(status_code=404, detail="solution not found")
    updated = db.update_problem_fields(
        solution_id,
        {"explanation": payload.explanation, "notes": payload.notes},
    )
    assert updated is not None
    return _to_out(updated)


@router.delete("/{solution_id}", status_code=204, response_class=Response)
def delete_solution(solution_id: int) -> Response:
    db = get_db()
    problem = db.delete_problem(solution_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="solution not found")
    # Clean up file from vault if present
    file_path = problem.get("file_path")
    if file_path:
        vault_root = get_vault_root()
        full_path = vault_root / file_path
        if full_path.is_file():
            try:
                full_path.unlink()
            except OSError:
                pass
    return Response(status_code=204)


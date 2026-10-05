"""Progress endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from ..deps import get_db
from ..schemas import ProgressOut
from ..services.progress import get_progress

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("", response_model=ProgressOut)
def progress() -> ProgressOut:
    return ProgressOut(**get_progress(get_db()))


@router.get("/heatmap")
def heatmap() -> list[dict[str, str | int]]:
    db = get_db()
    return db.list_activity_history()

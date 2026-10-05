"""Flashcard review endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..deps import get_db
from ..schemas import FlashcardOut, GradeIn
from ..services.review import due_cards, grade_card

router = APIRouter(prefix="/api/review", tags=["review"])


@router.get("/due", response_model=list[FlashcardOut])
def get_due() -> list[FlashcardOut]:
    db = get_db()
    out = []
    for r in due_cards(db):
        out.append(
            FlashcardOut(
                id=r["id"],
                problem_id=r["problem_id"],
                problem_title=r["problem_title"],
                front=r["front"],
                back=r["back"],
                due_date=r["due_date"],
            )
        )
    return out


@router.post("/{card_id}/grade")
def grade(card_id: int, payload: GradeIn) -> dict:
    db = get_db()
    try:
        return grade_card(db, card_id, payload.grade)
    except KeyError:
        raise HTTPException(status_code=404, detail="flashcard not found")

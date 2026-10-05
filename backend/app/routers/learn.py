"""Learning path and recommendation endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..deps import get_db
from ..domain.learning_path import CycleError
from ..schemas import PathOut, RecommendationOut
from ..services.recommend import learning_path, recommend_topics
from ..topics import cached_topics

router = APIRouter(prefix="/api/learn", tags=["learn"])


@router.get("/path", response_model=PathOut)
def path(topic: str) -> PathOut:
    dag = cached_topics()
    try:
        return PathOut(topic=topic, path=learning_path(dag, topic))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"unknown topic: {topic}")
    except CycleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/recommend", response_model=RecommendationOut)
def recommend(topic: str) -> RecommendationOut:
    dag = cached_topics()
    db = get_db()
    try:
        return RecommendationOut(**recommend_topics(dag, db, topic))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"unknown topic: {topic}")
    except CycleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/topics", response_model=list[str])
def topics() -> list[str]:
    return sorted(cached_topics().keys())

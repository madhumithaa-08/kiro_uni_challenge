"""Pydantic request/response models (the API boundary only)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SolutionCreate(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    topic: str = Field(..., min_length=1)
    platform: str = "other"
    language: str | None = None
    problem_slug: str | None = None
    notes: str = ""


class SolutionUpdate(BaseModel):
    explanation: str | None = None
    notes: str | None = None


class ComplexityOut(BaseModel):
    time: str
    space: str
    suggestions: list[str] = []


class SolutionOut(BaseModel):
    id: int
    title: str
    platform: str
    problem_slug: str
    topic: str
    language: str
    code: str
    explanation: str
    notes: str
    time_complexity: str
    space_complexity: str
    file_path: str
    created_at: str
    updated_at: str


class TopicCount(BaseModel):
    topic: str
    count: int


class ProgressOut(BaseModel):
    current_streak: int
    longest_streak: int
    total_solved: int
    total_flashcards: int
    by_topic: list[TopicCount]


class FlashcardOut(BaseModel):
    id: int
    problem_id: int
    problem_title: str
    front: str
    back: str
    due_date: str


class GradeIn(BaseModel):
    grade: str = Field(..., pattern="^(again|good|easy)$")


class PathOut(BaseModel):
    topic: str
    path: list[str]


class RecommendationOut(BaseModel):
    topic: str
    recommended_topics: list[str]
    note: str

"""Deterministic generation of explanations and flashcards from a solution.

Pure module: no I/O. Deterministic for a given input (steering: no randomness in
core generation). See requirements 4.1 and 6.1.
"""

from __future__ import annotations

from dataclasses import dataclass

from .complexity import ComplexityResult


@dataclass(frozen=True)
class FlashcardSeed:
    front: str
    back: str


def build_explanation(
    title: str,
    topic: str,
    language: str,
    complexity: ComplexityResult,
) -> str:
    """Produce an initial, editable explanation for a captured solution."""
    lines = [
        f"# {title}",
        "",
        f"Topic: {topic}",
        f"Language: {language}",
        f"Estimated time complexity: {complexity.time}",
        f"Estimated space complexity: {complexity.space}",
        "",
        "## Approach",
        "Describe the core idea of the solution here. "
        "This draft was generated automatically — edit it to capture the key "
        "insight, the data structures used, and why they fit the problem.",
    ]
    if complexity.suggestions:
        lines.append("")
        lines.append("## Suggestions")
        for tip in complexity.suggestions:
            lines.append(f"- {tip}")
    return "\n".join(lines)


def build_flashcards(
    title: str,
    topic: str,
    complexity: ComplexityResult,
) -> list[FlashcardSeed]:
    """Create at least one flashcard derived from the problem (requirement 6.1).

    Deterministic: same inputs always yield the same cards in the same order.
    """
    cards = [
        FlashcardSeed(
            front=f"What is the core approach for \"{title}\"?",
            back="Recall the key idea and the main data structure used.",
        ),
        FlashcardSeed(
            front=f"Time & space complexity of your \"{title}\" solution?",
            back=f"Time: {complexity.time}; Space: {complexity.space}.",
        ),
    ]
    if complexity.suggestions:
        cards.append(
            FlashcardSeed(
                front=f"What could be improved in \"{title}\"?",
                back="; ".join(complexity.suggestions),
            )
        )
    cards.append(
        FlashcardSeed(
            front=f"Which topic does \"{title}\" belong to, and what is a sibling problem?",
            back=f"Topic: {topic}. Recall a related problem in the same topic.",
        )
    )
    return cards

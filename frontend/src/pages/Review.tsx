import { useEffect, useState } from "react";
import { api, type Flashcard } from "../api/client";

export default function Review() {
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [idx, setIdx] = useState(0);
  const [showBack, setShowBack] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .dueCards()
      .then(setCards)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const card = cards[idx];

  async function grade(g: "again" | "good" | "easy") {
    if (!card) return;
    try {
      await api.gradeCard(card.id, g);
    } catch (e: any) {
      setError(e.message);
      return;
    }
    setShowBack(false);
    setIdx((i) => i + 1);
  }

  if (loading) return <p className="muted">Loading…</p>;

  return (
    <div>
      <h1 className="page-title">Review</h1>
      {error && <div className="error">{error}</div>}

      {!card ? (
        <div className="card">
          {cards.length === 0 ? (
            <p className="muted">No cards due today. You're caught up — come back tomorrow.</p>
          ) : (
            <p className="success" style={{ margin: 0 }}>
              Session complete — you reviewed {cards.length} card(s). 🎉
            </p>
          )}
        </div>
      ) : (
        <>
          <p className="muted">
            Card {idx + 1} of {cards.length} · from “{card.problem_title}”
          </p>
          <div className="flashcard">
            <div className="front">{card.front}</div>
            {showBack && <div className="back">{card.back}</div>}
          </div>
          <div className="row" style={{ marginTop: 16 }}>
            {!showBack ? (
              <button onClick={() => setShowBack(true)}>Show answer</button>
            ) : (
              <>
                <button className="again" onClick={() => grade("again")}>
                  Again
                </button>
                <button className="good" onClick={() => grade("good")}>
                  Good
                </button>
                <button className="easy" onClick={() => grade("easy")}>
                  Easy
                </button>
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
}

import { useEffect, useState } from "react";
import { api, type Flashcard } from "../api/client";
import { IconTrophy, IconCheckCircle, IconCards, IconSparkles } from "../components/Icons";

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

  // Handle keyboard shortcuts
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (!card) return;
      if (e.code === "Space" && !showBack) {
        e.preventDefault();
        setShowBack(true);
      } else if (showBack) {
        if (e.key === "1") grade("again");
        if (e.key === "2") grade("good");
        if (e.key === "3") grade("easy");
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [card, showBack, idx]);

  if (loading) {
    return (
      <div className="card" style={{ padding: 40, textAlign: "center" }}>
        <p className="muted">Fetching today's due flashcards…</p>
      </div>
    );
  }

  const progressPercent = cards.length > 0 ? Math.round(((idx) / cards.length) * 100) : 100;

  return (
    <div style={{ maxWidth: 680, margin: "0 auto" }}>
      <h1 className="page-title">Spaced Repetition Review</h1>
      <p className="subtitle">
        Active recall strengthens your memory of algorithms and problem-solving patterns.
      </p>

      {error && <div className="error">{error}</div>}

      {!card ? (
        <div className="card" style={{ textAlign: "center", padding: "40px 24px" }}>
          {cards.length === 0 ? (
            <div>
              <div
                style={{
                  width: 60,
                  height: 60,
                  borderRadius: "50%",
                  background: "var(--accent-2-light)",
                  color: "var(--accent-2)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 16px",
                }}
              >
                <IconCheckCircle size={32} />
              </div>
              <h2 style={{ margin: "0 0 8px 0", color: "var(--text-heading)" }}>All caught up!</h2>
              <p className="muted" style={{ margin: 0 }}>
                No flashcards are due today. Take a break or add new solutions to expand your vault.
              </p>
            </div>
          ) : (
            <div>
              <div
                style={{
                  width: 60,
                  height: 60,
                  borderRadius: "50%",
                  background: "var(--accent-light)",
                  color: "var(--accent)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 16px",
                }}
              >
                <IconTrophy size={32} />
              </div>
              <h2 style={{ margin: "0 0 8px 0", color: "var(--text-heading)" }}>Session Complete! 🎉</h2>
              <p className="muted" style={{ margin: "0 0 20px 0" }}>
                You successfully reviewed {cards.length} flashcard{cards.length === 1 ? "" : "s"} today. Great work!
              </p>
              <div className="progress-bar-bg" style={{ height: 10, marginBottom: 24 }}>
                <div className="progress-bar-fill" style={{ width: "100%", background: "var(--accent-2)" }} />
              </div>
            </div>
          )}
        </div>
      ) : (
        <>
          <div className="row" style={{ marginBottom: 8 }}>
            <span className="row" style={{ gap: 6, fontSize: 13, fontWeight: 600, color: "var(--text-heading)" }}>
              <IconCards size={16} className="muted" />
              <span>Card {idx + 1} of {cards.length}</span>
            </span>
            <span className="spacer" />
            <span className="badge topic">
              Problem: {card.problem_title}
            </span>
          </div>

          <div className="progress-bar-bg">
            <div className="progress-bar-fill" style={{ width: `${progressPercent}%` }} />
          </div>

          <div className="flashcard-wrapper">
            <div className="flashcard">
              <div className="front">
                {card.front}
              </div>

              {showBack && (
                <div className="back">
                  <div className="row" style={{ justifyContent: "center", gap: 6, marginBottom: 8, fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5, color: "var(--accent-2)" }}>
                    <IconSparkles size={14} />
                    <span>Answer / Recall Note</span>
                  </div>
                  <div>{card.back}</div>
                </div>
              )}
            </div>
          </div>

          <div style={{ textAlign: "center", marginTop: 24 }}>
            {!showBack ? (
              <button
                onClick={() => setShowBack(true)}
                className="btn"
                style={{ minWidth: 200, padding: "14px 28px", fontSize: 15 }}
              >
                <span>Show Answer</span>
                <span style={{ fontSize: 11, opacity: 0.8, marginLeft: 4 }}>(Space)</span>
              </button>
            ) : (
              <div>
                <p className="muted" style={{ fontSize: 13, marginBottom: 12 }}>
                  How easily did you remember this?
                </p>
                <div className="row" style={{ justifyContent: "center", gap: 14 }}>
                  <button className="again" onClick={() => grade("again")} style={{ padding: "12px 24px" }}>
                    <span>1. Again</span>
                  </button>
                  <button className="good" onClick={() => grade("good")} style={{ padding: "12px 24px" }}>
                    <span>2. Good</span>
                  </button>
                  <button className="easy" onClick={() => grade("easy")} style={{ padding: "12px 24px" }}>
                    <span>3. Easy</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

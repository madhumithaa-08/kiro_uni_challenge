import { useEffect, useState } from "react";
import { api, type Recommendation } from "../api/client";

export default function Learn() {
  const [topics, setTopics] = useState<string[]>([]);
  const [topic, setTopic] = useState("");
  const [rec, setRec] = useState<Recommendation | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api
      .topics()
      .then((t) => {
        setTopics(t);
        if (t.length) setTopic(t[0]);
      })
      .catch((e) => setError(e.message));
  }, []);

  async function loadPath() {
    if (!topic) return;
    setLoading(true);
    setError(null);
    try {
      setRec(await api.recommend(topic));
    } catch (e: any) {
      setError(e.message);
      setRec(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="page-title">Learn</h1>
      <p className="muted">
        Pick a topic to get a prerequisite-ordered learning path. Study earlier
        topics first — they build toward your target.
      </p>

      {error && <div className="error">{error}</div>}

      <div className="row" style={{ marginBottom: 16 }}>
        <select value={topic} onChange={(e) => setTopic(e.target.value)} style={{ maxWidth: 260 }}>
          {topics.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        <button onClick={loadPath} disabled={loading}>
          {loading ? "Loading…" : "Show learning path"}
        </button>
      </div>

      {rec && (
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Path to “{rec.topic}”</h3>
          <div style={{ margin: "12px 0" }}>
            {rec.recommended_topics.map((t, i) => (
              <span key={t} className="path-step">
                <span className="badge topic">{t}</span>
                {i < rec.recommended_topics.length - 1 && <span className="path-arrow">→</span>}
              </span>
            ))}
          </div>
          <p className="muted" style={{ marginBottom: 0 }}>
            {rec.note}
          </p>
        </div>
      )}
    </div>
  );
}

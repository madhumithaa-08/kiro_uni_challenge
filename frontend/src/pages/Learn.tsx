import { useEffect, useState } from "react";
import { api, type Recommendation } from "../api/client";
import { IconLearn, IconCheckCircle, IconSparkles } from "../components/Icons";

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
        if (t.length) {
          setTopic(t[0]);
          fetchPath(t[0]);
        }
      })
      .catch((e) => setError(e.message));
  }, []);

  async function fetchPath(targetTopic: string) {
    if (!targetTopic) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.recommend(targetTopic);
      setRec(data);
    } catch (e: any) {
      setError(e.message);
      setRec(null);
    } finally {
      setLoading(false);
    }
  }

  function handleSelectTopic(t: string) {
    setTopic(t);
    fetchPath(t);
  }

  return (
    <div>
      <h1 className="page-title">Learning Paths</h1>
      <p className="subtitle">
        Pick a topic to generate a prerequisite-ordered study path. Master foundational concepts first to build up to your target topic.
      </p>

      {error && <div className="error">{error}</div>}

      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ margin: "0 0 12px 0", fontSize: 16, color: "var(--text-heading)" }}>
          Select Target Topic
        </h3>
        <div className="row wrap" style={{ gap: 8 }}>
          {topics.map((t) => (
            <button
              key={t}
              type="button"
              className={topic === t ? "btn" : "btn secondary"}
              onClick={() => handleSelectTopic(t)}
              style={{ padding: "8px 16px", fontSize: 13 }}
            >
              <span>{t}</span>
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="card" style={{ padding: 36, textAlign: "center" }}>
          <p className="muted">Generating topological learning path for “{topic}”…</p>
        </div>
      )}

      {rec && !loading && (
        <div className="card">
          <div className="row" style={{ marginBottom: 20 }}>
            <IconLearn size={24} style={{ color: "var(--accent)" }} />
            <div>
              <h3 style={{ margin: 0, fontSize: 20, color: "var(--text-heading)" }}>
                Prerequisite Path for “{rec.topic}”
              </h3>
              <p className="muted" style={{ margin: 0, fontSize: 13 }}>
                Study topics in this sequence for optimal understanding.
              </p>
            </div>
          </div>

          <div className="path-container">
            {rec.recommended_topics.map((t, idx) => {
              const isTarget = t === rec.topic;
              return (
                <div key={t}>
                  <div
                    className="path-step-card"
                    style={{
                      borderColor: isTarget ? "var(--accent)" : "var(--border)",
                      background: isTarget ? "var(--accent-light)" : "var(--panel)",
                    }}
                  >
                    <div
                      className="step-num"
                      style={{
                        background: isTarget ? "var(--accent)" : "var(--panel-2)",
                        color: isTarget ? "#ffffff" : "var(--text)",
                      }}
                    >
                      {idx + 1}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div className="row">
                        <span style={{ fontWeight: 700, fontSize: 16, color: "var(--text-heading)" }}>
                          {t}
                        </span>
                        {isTarget && (
                          <span className="badge topic">
                            Target Goal
                          </span>
                        )}
                      </div>
                      <span className="muted" style={{ fontSize: 12 }}>
                        {isTarget
                          ? "Final target topic in this study plan"
                          : `Prerequisite step ${idx + 1}`}
                      </span>
                    </div>
                    <IconCheckCircle size={18} className={isTarget ? "accent" : "muted"} />
                  </div>

                  {idx < rec.recommended_topics.length - 1 && (
                    <div className="path-arrow-down" style={{ margin: "6px 0 6px 36px" }}>
                      <span className="muted" style={{ fontSize: 18 }}>↓</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {rec.note && (
            <div
              style={{
                marginTop: 24,
                padding: 16,
                background: "var(--panel-2)",
                border: "1px solid var(--border)",
                borderRadius: "var(--radius)",
                display: "flex",
                gap: 12,
                alignItems: "flex-start",
              }}
            >
              <IconSparkles size={20} style={{ color: "var(--warn)", flexShrink: 0, marginTop: 2 }} />
              <div>
                <div style={{ fontWeight: 600, fontSize: 14, color: "var(--text-heading)" }}>
                  Study Advice
                </div>
                <div className="muted" style={{ fontSize: 13, marginTop: 2 }}>
                  {rec.note}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

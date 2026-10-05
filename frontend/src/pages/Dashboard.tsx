import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type Progress, type Flashcard } from "../api/client";
import { ActivityHeatmap } from "../components/ActivityHeatmap";
import {
  IconFlame,
  IconTrophy,
  IconCheckCircle,
  IconCards,
  IconArrowRight,
  IconSparkles,
} from "../components/Icons";

export default function Dashboard() {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [due, setDue] = useState<Flashcard[]>([]);
  const [heatmapData, setHeatmapData] = useState<{ day: string; count: number }[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.progress(), api.dueCards(), api.activityHeatmap()])
      .then(([p, d, h]) => {
        setProgress(p);
        setDue(d);
        setHeatmapData(h);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="card" style={{ padding: 40, textAlign: "center" }}>
        <p className="muted">Loading your DSA Vault workspace…</p>
      </div>
    );
  }

  if (error) {
    return <div className="error">Could not load dashboard: {error}</div>;
  }

  const totalTopicProblems = progress?.by_topic.reduce((acc, curr) => acc + curr.count, 0) || 1;

  return (
    <div>
      <div className="welcome-banner">
        <div>
          <h1 className="welcome-title">Welcome back! 👋</h1>
          <p className="muted" style={{ margin: 0, fontSize: 14 }}>
            Keep up your practice momentum. Capture solutions & review flashcards daily.
          </p>
        </div>
        <Link to="/add" className="btn">
          <IconSparkles size={16} />
          <span>Add Solution</span>
        </Link>
      </div>

      <div className="grid cols-4">
        <div className="stat-card">
          <div className="stat-icon flame">
            <IconFlame size={22} />
          </div>
          <div className="stat-info">
            <div className="value">{progress?.current_streak ?? 0}</div>
            <div className="label">Current Streak (days)</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon trophy">
            <IconTrophy size={22} />
          </div>
          <div className="stat-info">
            <div className="value">{progress?.longest_streak ?? 0}</div>
            <div className="label">Longest Streak</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon solved">
            <IconCheckCircle size={22} />
          </div>
          <div className="stat-info">
            <div className="value">{progress?.total_solved ?? 0}</div>
            <div className="label">Problems Solved</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon cards">
            <IconCards size={22} />
          </div>
          <div className="stat-info">
            <div className="value">{due.length}</div>
            <div className="label">Cards Due Today</div>
          </div>
        </div>
      </div>

      <ActivityHeatmap data={heatmapData} />

      <div className="grid cols-2" style={{ marginTop: 24 }}>
        <div className="card">
          <div className="row" style={{ marginBottom: 16 }}>
            <h3 style={{ margin: 0, fontSize: 18, color: "var(--text-heading)" }}>Topics Covered</h3>
            <span className="spacer" />
            <span className="muted" style={{ fontSize: 13 }}>
              {progress?.by_topic.length ?? 0} topic(s)
            </span>
          </div>

          {progress && progress.by_topic.length > 0 ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {progress.by_topic.map((t) => {
                const percentage = Math.round((t.count / totalTopicProblems) * 100);
                return (
                  <div key={t.topic} style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                    <div className="row">
                      <span className="badge topic" style={{ fontSize: 13 }}>
                        {t.topic}
                      </span>
                      <span className="spacer" />
                      <span className="muted" style={{ fontSize: 13, fontWeight: 600 }}>
                        {t.count} problem{t.count === 1 ? "" : "s"}
                      </span>
                    </div>
                    <div className="progress-bar-bg" style={{ margin: "2px 0 6px" }}>
                      <div className="progress-bar-fill" style={{ width: `${Math.max(percentage, 8)}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="muted">
              No problems saved yet. <Link to="/add">Add your first solution →</Link>
            </p>
          )}
        </div>

        <div className="card" style={{ display: "flex", flexDirection: "column" }}>
          <h3 style={{ margin: "0 0 12px 0", fontSize: 18, color: "var(--text-heading)" }}>
            Review Spaced Repetition
          </h3>

          {due.length > 0 ? (
            <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <p style={{ margin: "0 0 16px 0", lineHeight: 1.6 }}>
                You have <strong style={{ color: "var(--accent)" }}>{due.length}</strong> flashcard
                {due.length === 1 ? "" : "s"} ready for review. Daily spaced repetition helps retain algorithmic patterns.
              </p>
              <Link to="/review" className="btn good" style={{ width: "100%" }}>
                <span>Start Reviewing</span>
                <IconArrowRight size={16} />
              </Link>
            </div>
          ) : (
            <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <div style={{ padding: "16px 0" }}>
                <p style={{ color: "var(--accent-2)", fontWeight: 600, margin: "0 0 4px 0" }}>
                  🎉 All caught up!
                </p>
                <p className="muted" style={{ margin: 0, fontSize: 14 }}>
                  No flashcards due right now. Solve new problems to generate automatic flashcards or check back tomorrow.
                </p>
              </div>
              <Link to="/problems" className="btn secondary" style={{ width: "100%" }}>
                <span>Browse Problems</span>
                <IconArrowRight size={16} />
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

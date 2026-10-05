import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type Progress, type Flashcard } from "../api/client";

export default function Dashboard() {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [due, setDue] = useState<Flashcard[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.progress(), api.dueCards()])
      .then(([p, d]) => {
        setProgress(p);
        setDue(d);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted">Loading…</p>;
  if (error) return <div className="error">Could not load dashboard: {error}</div>;

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>
      <div className="grid cols-4">
        <div className="card stat">
          <div className="value">{progress?.current_streak ?? 0}</div>
          <div className="label">current streak (days)</div>
        </div>
        <div className="card stat">
          <div className="value">{progress?.longest_streak ?? 0}</div>
          <div className="label">longest streak</div>
        </div>
        <div className="card stat">
          <div className="value">{progress?.total_solved ?? 0}</div>
          <div className="label">problems solved</div>
        </div>
        <div className="card stat">
          <div className="value">{due.length}</div>
          <div className="label">cards due today</div>
        </div>
      </div>

      <div className="grid cols-2" style={{ marginTop: 16 }}>
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Topics covered</h3>
          {progress && progress.by_topic.length > 0 ? (
            <div className="row wrap">
              {progress.by_topic.map((t) => (
                <span key={t.topic} className="badge topic">
                  {t.topic} · {t.count}
                </span>
              ))}
            </div>
          ) : (
            <p className="muted">
              No problems yet. <Link to="/add">Add your first solution →</Link>
            </p>
          )}
        </div>
        <div className="card">
          <h3 style={{ marginTop: 0 }}>Review</h3>
          {due.length > 0 ? (
            <p>
              You have <strong>{due.length}</strong> flashcard(s) due.{" "}
              <Link to="/review">Start reviewing →</Link>
            </p>
          ) : (
            <p className="muted">You're caught up on reviews. Nice.</p>
          )}
        </div>
      </div>
    </div>
  );
}

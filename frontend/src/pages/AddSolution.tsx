import { FormEvent, useEffect, useState } from "react";
import { api, type Solution } from "../api/client";

export default function AddSolution() {
  const [topics, setTopics] = useState<string[]>([]);
  const [title, setTitle] = useState("");
  const [topic, setTopic] = useState("arrays");
  const [platform, setPlatform] = useState("leetcode");
  const [slug, setSlug] = useState("");
  const [code, setCode] = useState("");
  const [notes, setNotes] = useState("");
  const [saved, setSaved] = useState<Solution | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.topics().then(setTopics).catch(() => setTopics(["arrays"]));
  }, []);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSaved(null);
    setBusy(true);
    try {
      const result = await api.createSolution({
        title,
        code,
        topic,
        platform,
        problem_slug: slug || null,
        notes,
      });
      setSaved(result);
      setTitle("");
      setSlug("");
      setCode("");
      setNotes("");
    } catch (e: any) {
      setError(e.message ?? "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h1 className="page-title">Add Solution</h1>
      <p className="muted">
        Paste a solution once. DSA Vault detects the language, analyzes complexity,
        files it under its topic, and builds flashcards automatically.
      </p>

      {error && <div className="error">{error}</div>}
      {saved && (
        <div className="success">
          Saved <strong>{saved.title}</strong> → <code>{saved.file_path}</code> ·{" "}
          {saved.language} · {saved.time_complexity} time / {saved.space_complexity} space.
          3+ flashcards created.
        </div>
      )}

      <form onSubmit={onSubmit} className="card">
        <div className="grid cols-2">
          <div>
            <label>Title *</label>
            <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Two Sum" required />
          </div>
          <div>
            <label>Problem slug (optional)</label>
            <input value={slug} onChange={(e) => setSlug(e.target.value)} placeholder="0001-two-sum" />
          </div>
          <div>
            <label>Topic</label>
            <select value={topic} onChange={(e) => setTopic(e.target.value)}>
              {topics.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Platform</label>
            <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
              <option value="leetcode">LeetCode</option>
              <option value="hackerrank">HackerRank</option>
              <option value="codechef">CodeChef</option>
              <option value="geeksforgeeks">GeeksforGeeks</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
        <label>Code *</label>
        <textarea value={code} onChange={(e) => setCode(e.target.value)} placeholder="Paste your solution here…" required />
        <label>Your notes (optional)</label>
        <input value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Key insight you want to remember…" />
        <div className="row" style={{ marginTop: 16 }}>
          <button type="submit" disabled={busy}>
            {busy ? "Analyzing…" : "Capture solution"}
          </button>
        </div>
      </form>
    </div>
  );
}

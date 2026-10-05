import { FormEvent, useEffect, useState } from "react";
import { api, type Solution } from "../api/client";
import { IconSparkles, IconCheckCircle, IconCode } from "../components/Icons";

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
      setError(e.message ?? "Something went wrong while saving solution");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h1 className="page-title">Add Solution</h1>
      <p className="subtitle">
        Paste a solution once. DSA Vault detects the programming language, performs static complexity analysis,
        files your code under its topic, and builds spaced-repetition flashcards automatically.
      </p>

      {error && <div className="error">{error}</div>}

      {saved && (
        <div className="success" style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
          <IconCheckCircle size={22} style={{ flexShrink: 0, marginTop: 2 }} />
          <div>
            <div style={{ fontWeight: 700, fontSize: 16 }}>Solution saved successfully!</div>
            <div style={{ marginTop: 4, lineHeight: 1.5 }}>
              Saved <strong>{saved.title}</strong> to <code>{saved.file_path}</code>
            </div>
            <div className="row wrap" style={{ marginTop: 8 }}>
              <span className="badge topic">{saved.topic}</span>
              <span className="badge platform">{saved.platform}</span>
              <span className="badge">{saved.language}</span>
              <span className="badge cx">Time: {saved.time_complexity}</span>
              <span className="badge cx">Space: {saved.space_complexity}</span>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={onSubmit} className="card">
        <div className="grid cols-2" style={{ gap: 24 }}>
          <div>
            <h3 style={{ margin: "0 0 14px 0", fontSize: 17, color: "var(--text-heading)" }}>
              Problem Metadata
            </h3>

            <label>Title *</label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Two Sum"
              required
            />

            <div className="grid cols-2" style={{ gap: 12, margin: 0 }}>
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

            <label>Problem Slug (optional)</label>
            <input
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              placeholder="e.g. 0001-two-sum"
            />

            <label>Your Notes (optional)</label>
            <input
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Key insight or intuition to remember…"
            />
          </div>

          <div style={{ display: "flex", flexDirection: "column" }}>
            <div className="row" style={{ marginBottom: 6 }}>
              <IconCode size={18} className="muted" />
              <h3 style={{ margin: 0, fontSize: 17, color: "var(--text-heading)" }}>
                Code Solution *
              </h3>
            </div>
            <textarea
              style={{ flex: 1, minHeight: 220 }}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="// Paste your algorithm solution here...
function twoSum(nums, target) {
  const map = new Map();
  for (let i = 0; i < nums.length; i++) {
    const diff = target - nums[i];
    if (map.has(diff)) return [map.get(diff), i];
    map.set(nums[i], i);
  }
  return [];
}"
              required
            />
          </div>
        </div>

        <div className="row" style={{ marginTop: 24, paddingTop: 16, borderTop: "1px solid var(--border-subtle)" }}>
          <span className="muted" style={{ fontSize: 13 }}>
            Complexity & flashcards will be auto-generated.
          </span>
          <span className="spacer" />
          <button type="submit" disabled={busy} className="btn">
            <IconSparkles size={16} />
            <span>{busy ? "Analyzing & Saving…" : "Capture Solution"}</span>
          </button>
        </div>
      </form>
    </div>
  );
}

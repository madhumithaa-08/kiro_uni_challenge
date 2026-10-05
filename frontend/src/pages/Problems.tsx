import { useEffect, useState } from "react";
import { api, type Solution } from "../api/client";
import { IconSearch, IconCopy, IconCheckCircle, IconCode, IconSparkles } from "../components/Icons";

export default function Problems() {
  const [items, setItems] = useState<Solution[]>([]);
  const [search, setSearch] = useState("");
  const [topicFilter, setTopicFilter] = useState("");
  const [platformFilter, setPlatformFilter] = useState("");
  const [topics, setTopics] = useState<string[]>([]);
  const [selected, setSelected] = useState<Solution | null>(null);
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api.topics().then(setTopics).catch(() => {});
  }, []);

  function load() {
    api
      .listSolutions(search || undefined, topicFilter || undefined)
      .then((data) => {
        let filtered = data;
        if (platformFilter) {
          filtered = filtered.filter((s) => s.platform.toLowerCase() === platformFilter.toLowerCase());
        }
        setItems(filtered);
        if (filtered.length > 0) {
          if (!selected || !filtered.some((s) => s.id === selected.id)) {
            setSelected(filtered[0]);
            setNotes(filtered[0].notes);
          }
        } else {
          setSelected(null);
        }
      })
      .catch((e) => setError(e.message));
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicFilter, platformFilter]);

  function open(s: Solution) {
    setSelected(s);
    setNotes(s.notes);
    setCopied(false);
  }

  async function saveNotes() {
    if (!selected) return;
    setSaving(true);
    try {
      const updated = await api.updateSolution(selected.id, { notes });
      setSelected(updated);
      load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!selected) return;
    if (!window.confirm(`Are you sure you want to delete "${selected.title}" from your vault?`)) {
      return;
    }
    setDeleting(true);
    try {
      await api.deleteSolution(selected.id);
      setSelected(null);
      load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setDeleting(false);
    }
  }

  function handleCopyCode() {
    if (!selected) return;
    navigator.clipboard.writeText(selected.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div>
      <h1 className="page-title">Problems Archive</h1>
      <p className="subtitle">Browse, search, manage, and review your collected algorithms and custom notes.</p>

      {error && <div className="error">{error}</div>}

      <div className="grid cols-3" style={{ gridTemplateColumns: "1fr 180px 180px", gap: 12, marginBottom: 20 }}>
        <div style={{ position: "relative" }}>
          <input
            style={{ paddingLeft: 38 }}
            placeholder="Search title, notes, code…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && load()}
          />
          <IconSearch
            size={18}
            style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "var(--muted)" }}
          />
        </div>

        <select value={topicFilter} onChange={(e) => setTopicFilter(e.target.value)}>
          <option value="">All Topics</option>
          {topics.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>

        <select value={platformFilter} onChange={(e) => setPlatformFilter(e.target.value)}>
          <option value="">All Platforms</option>
          <option value="leetcode">LeetCode</option>
          <option value="hackerrank">HackerRank</option>
          <option value="codechef">CodeChef</option>
          <option value="geeksforgeeks">GeeksforGeeks</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="grid cols-2" style={{ gridTemplateColumns: "340px 1fr", gap: 24 }}>
        <div>
          <div className="muted" style={{ fontSize: 13, marginBottom: 10, fontWeight: 600 }}>
            {items.length} problem{items.length === 1 ? "" : "s"} found
          </div>
          {items.length === 0 && (
            <div className="card" style={{ padding: 24, textAlign: "center" }}>
              <p className="muted" style={{ margin: 0 }}>No solutions matching filters.</p>
            </div>
          )}
          {items.map((s) => (
            <div
              key={s.id}
              className={`list-item ${selected?.id === s.id ? "selected" : ""}`}
              onClick={() => open(s)}
            >
              <h3>{s.title}</h3>
              <div className="row wrap" style={{ gap: 6 }}>
                <span className="badge topic">{s.topic}</span>
                <span className="badge platform">{s.platform}</span>
                <span className="badge cx">O({s.time_complexity})</span>
              </div>
            </div>
          ))}
        </div>

        <div>
          {selected ? (
            <div className="card">
              <div className="row" style={{ alignItems: "flex-start", marginBottom: 12 }}>
                <div>
                  <h2 style={{ margin: "0 0 6px 0", fontSize: 22, color: "var(--text-heading)" }}>
                    {selected.title}
                  </h2>
                  <div className="row wrap" style={{ gap: 6 }}>
                    <span className="badge topic">{selected.topic}</span>
                    <span className="badge platform">{selected.platform}</span>
                    <span className="badge">{selected.language}</span>
                    <span className="badge cx">Time: {selected.time_complexity}</span>
                    <span className="badge cx">Space: {selected.space_complexity}</span>
                  </div>
                </div>
                <span className="spacer" />
                <div className="row" style={{ gap: 8 }}>
                  <button type="button" className="secondary" onClick={handleCopyCode} style={{ padding: "8px 14px", fontSize: 13 }}>
                    {copied ? <IconCheckCircle size={15} style={{ color: "var(--accent-2)" }} /> : <IconCopy size={15} />}
                    <span>{copied ? "Copied!" : "Copy code"}</span>
                  </button>
                  <button type="button" className="again" onClick={handleDelete} disabled={deleting} style={{ padding: "8px 14px", fontSize: 13 }}>
                    <span>{deleting ? "Deleting…" : "Delete"}</span>
                  </button>
                </div>
              </div>

              <div style={{ marginTop: 20 }}>
                <div className="code-header">
                  <span className="row" style={{ gap: 6 }}>
                    <IconCode size={16} />
                    <span>Code Solution</span>
                  </span>
                  <span>{selected.language}</span>
                </div>
                <pre>{selected.code}</pre>
              </div>

              <div style={{ marginTop: 20 }}>
                <div className="code-header">
                  <span className="row" style={{ gap: 6 }}>
                    <IconSparkles size={16} />
                    <span>Explanation & Complexity</span>
                  </span>
                </div>
                <div
                  style={{
                    background: "var(--panel-2)",
                    border: "1px solid var(--border)",
                    borderRadius: "var(--radius)",
                    padding: 16,
                    fontSize: 14,
                    lineHeight: 1.6,
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {selected.explanation || "No static explanation available."}
                </div>
              </div>

              <div style={{ marginTop: 20 }}>
                <label style={{ fontSize: 14, color: "var(--text-heading)" }}>Personal Notes</label>
                <textarea
                  style={{ minHeight: 90 }}
                  placeholder="Add your key intuition or reminders for this problem…"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
                <div className="row" style={{ marginTop: 12 }}>
                  <span className="spacer" />
                  <button onClick={saveNotes} disabled={saving} className="btn">
                    <span>{saving ? "Saving…" : "Save notes"}</span>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="card" style={{ padding: 40, textAlign: "center" }}>
              <p className="muted">Select a problem from the list to view its code, explanation, and notes.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

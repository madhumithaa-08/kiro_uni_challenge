import { useEffect, useState } from "react";
import { api, type Solution } from "../api/client";

export default function Problems() {
  const [items, setItems] = useState<Solution[]>([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<Solution | null>(null);
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  function load() {
    api
      .listSolutions(search || undefined)
      .then(setItems)
      .catch((e) => setError(e.message));
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function open(s: Solution) {
    setSelected(s);
    setNotes(s.notes);
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

  return (
    <div>
      <h1 className="page-title">Problems</h1>
      {error && <div className="error">{error}</div>}

      <div className="row" style={{ marginBottom: 16 }}>
        <input
          placeholder="Search by title or notes…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && load()}
        />
        <button className="secondary" onClick={load}>
          Search
        </button>
      </div>

      <div className="grid cols-2">
        <div>
          {items.length === 0 && <p className="muted">No solutions yet.</p>}
          {items.map((s) => (
            <div key={s.id} className="list-item" onClick={() => open(s)}>
              <h3>{s.title}</h3>
              <span className="badge topic">{s.topic}</span>
              <span className="badge">{s.platform}</span>
              <span className="badge cx">{s.time_complexity}</span>
            </div>
          ))}
        </div>
        <div>
          {selected ? (
            <div className="card">
              <h2 style={{ marginTop: 0 }}>{selected.title}</h2>
              <div className="row wrap">
                <span className="badge topic">{selected.topic}</span>
                <span className="badge">{selected.language}</span>
                <span className="badge cx">time {selected.time_complexity}</span>
                <span className="badge cx">space {selected.space_complexity}</span>
              </div>
              <h4>Code</h4>
              <pre>{selected.code}</pre>
              <h4>Explanation</h4>
              <pre style={{ whiteSpace: "pre-wrap" }}>{selected.explanation}</pre>
              <label>Your notes</label>
              <textarea
                style={{ minHeight: 80 }}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
              <div className="row" style={{ marginTop: 10 }}>
                <button onClick={saveNotes} disabled={saving}>
                  {saving ? "Saving…" : "Save notes"}
                </button>
              </div>
            </div>
          ) : (
            <p className="muted">Select a problem to view its code, explanation, and notes.</p>
          )}
        </div>
      </div>
    </div>
  );
}

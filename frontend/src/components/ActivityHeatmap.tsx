import { useMemo } from "react";

interface ActivityHeatmapProps {
  data: { day: string; count: number }[];
}

export function ActivityHeatmap({ data }: ActivityHeatmapProps) {
  const activityMap = useMemo(() => {
    const map = new Map<string, number>();
    for (const item of data) {
      map.set(item.day, item.count);
    }
    return map;
  }, [data]);

  const grid = useMemo(() => {
    const days: { dateStr: string; dayOfWeek: number; count: number }[] = [];
    const today = new Date();
    // 52 weeks = 364 days
    for (let i = 364; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      const count = activityMap.get(dateStr) || 0;
      days.push({
        dateStr,
        dayOfWeek: d.getDay(), // 0: Sun, 1: Mon, ...
        count,
      });
    }
    return days;
  }, [activityMap]);

  function getLevelClass(count: number): string {
    if (count === 0) return "heat-level-0";
    if (count === 1) return "heat-level-1";
    if (count === 2) return "heat-level-2";
    return "heat-level-3";
  }

  return (
    <div className="card" style={{ marginTop: 20 }}>
      <div className="row" style={{ marginBottom: 12 }}>
        <h3 style={{ margin: 0, fontSize: 17, color: "var(--text-heading)" }}>
          Practice Habit Heatmap (Past Year)
        </h3>
        <span className="spacer" />
        <div className="row" style={{ gap: 4, fontSize: 11, color: "var(--muted)" }}>
          <span>Less</span>
          <span className="heat-box heat-level-0" />
          <span className="heat-box heat-level-1" />
          <span className="heat-box heat-level-2" />
          <span className="heat-box heat-level-3" />
          <span>More</span>
        </div>
      </div>

      <div style={{ overflowX: "auto", paddingBottom: 6 }}>
        <div
          style={{
            display: "grid",
            gridTemplateRows: "repeat(7, 12px)",
            gridAutoFlow: "column",
            gridAutoColumns: "12px",
            gap: 3,
            minWidth: 700,
          }}
        >
          {grid.map((day) => (
            <div
              key={day.dateStr}
              className={`heat-box ${getLevelClass(day.count)}`}
              title={`${day.dateStr}: ${day.count} activity item(s)`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

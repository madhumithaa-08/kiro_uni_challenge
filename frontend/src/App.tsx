import { useEffect, useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import AddSolution from "./pages/AddSolution";
import Problems from "./pages/Problems";
import Review from "./pages/Review";
import Learn from "./pages/Learn";
import {
  IconDashboard,
  IconPlusCircle,
  IconProblems,
  IconReview,
  IconLearn,
  IconVault,
  IconSun,
  IconMoon,
} from "./components/Icons";

export default function App() {
  const [theme, setTheme] = useState<"light" | "dark">(() => {
    return (localStorage.getItem("dsa-vault-theme") as "light" | "dark") || "light";
  });

  useEffect(() => {
    localStorage.setItem("dsa-vault-theme", theme);
    if (theme === "dark") {
      document.body.classList.add("dark-theme");
    } else {
      document.body.classList.remove("dark-theme");
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <div className={`app ${theme === "dark" ? "dark-theme" : ""}`}>
      <aside className="sidebar">
        <div className="brand-wrapper">
          <div className="brand-icon">
            <IconVault size={22} />
          </div>
          <div>
            <div className="brand">
              DSA<span>Vault</span>
            </div>
          </div>
        </div>
        <div className="tagline">capture once, remember forever</div>

        <nav className="nav">
          <NavLink to="/" end>
            <IconDashboard size={18} />
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/add">
            <IconPlusCircle size={18} />
            <span>Add Solution</span>
          </NavLink>
          <NavLink to="/problems">
            <IconProblems size={18} />
            <span>Problems</span>
          </NavLink>
          <NavLink to="/review">
            <IconReview size={18} />
            <span>Review</span>
          </NavLink>
          <NavLink to="/learn">
            <IconLearn size={18} />
            <span>Learn</span>
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <button type="button" className="theme-toggle-btn" onClick={toggleTheme}>
            <span className="row" style={{ gap: 8 }}>
              {theme === "light" ? <IconSun size={16} /> : <IconMoon size={16} />}
              <span>{theme === "light" ? "Cozy Light" : "Cozy Dark"}</span>
            </span>
            <span className="muted" style={{ fontSize: 11 }}>Switch</span>
          </button>
        </div>
      </aside>

      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/add" element={<AddSolution />} />
          <Route path="/problems" element={<Problems />} />
          <Route path="/review" element={<Review />} />
          <Route path="/learn" element={<Learn />} />
        </Routes>
      </main>
    </div>
  );
}

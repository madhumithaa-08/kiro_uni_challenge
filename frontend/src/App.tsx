import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import AddSolution from "./pages/AddSolution";
import Problems from "./pages/Problems";
import Review from "./pages/Review";
import Learn from "./pages/Learn";

export default function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          DSA<span>Vault</span>
        </div>
        <div className="tagline">capture once, remember forever</div>
        <nav className="nav">
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/add">Add Solution</NavLink>
          <NavLink to="/problems">Problems</NavLink>
          <NavLink to="/review">Review</NavLink>
          <NavLink to="/learn">Learn</NavLink>
        </nav>
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

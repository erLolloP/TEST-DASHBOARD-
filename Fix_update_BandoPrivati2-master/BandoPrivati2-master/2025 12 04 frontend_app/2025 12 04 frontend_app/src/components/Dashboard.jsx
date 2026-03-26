import React, { useState } from "react";
import { apiJson } from "../api";

const formatCurrency = (value) =>
  new Intl.NumberFormat("it-IT", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(value);

export default function Dashboard({ accessLevel }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function refreshDashboard() {
    setLoading(true);
    setError("");
    try {
      const data = await apiJson("/data/dashboard", {
        method: "GET",
        accessLevel,
      });
      setStats(data);
    } catch (err) {
      setError(err.message || "Errore durante il caricamento dashboard.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>Dashboard bando</h2>

      <button
        className="button secondary"
        onClick={refreshDashboard}
        disabled={loading}
      >
        {loading ? "Aggiornamento..." : "Aggiorna dashboard"}
      </button>

      {error && <p style={{ color: "red", marginTop: 8 }}>{error}</p>}

      {stats && (
        <div className="dashboard-grid">
          <div className="dashboard-box">
            <p className="dashboard-label">Numero strutture aderenti</p>
            <p className="dashboard-value">{stats.total_strutture}</p>
          </div>

          <div className="dashboard-box">
            <p className="dashboard-label">Residuo fondi</p>
            <p className="dashboard-value">{formatCurrency(stats.residuo_fondi)}</p>
          </div>

          <div className="dashboard-box dashboard-box-wide">
            <p className="dashboard-label">Conteggio compilazioni per tipologia documentale</p>
            <ul className="dashboard-list">
              {Object.entries(stats.fornitori_unici_per_tipologia).map(([tipologia, count]) => (
                <li key={tipologia}>
                  <strong>{tipologia}:</strong> {count}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

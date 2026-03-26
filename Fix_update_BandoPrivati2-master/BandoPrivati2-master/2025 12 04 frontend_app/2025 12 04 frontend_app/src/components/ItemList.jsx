// ItemList.jsx content
import React, { useState } from "react";
import { apiJson, deleteItemById } from "../api";

export default function ItemList({ accessLevel }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [deletingPartitaIva, setDeletingPartitaIva] = useState(null);

  async function loadItems() {
    setLoading(true);
    setError("");
    try {
      const data = await apiJson("/data", {
        method: "GET",
        accessLevel,
      });
      setItems(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(itemId) {
    setError("");
    setDeletingId(itemId);
    try {
      await deleteItemById(itemId);
      setItems((prev) => prev.filter((it) => it.id !== itemId));
    } catch (err) {
      setError(err.message || "Errore durante l'eliminazione.");
    } finally {
      setDeletingPartitaIva(null);
    }
  }

  return (
    <div className="card">
      <h2>Lista strutture (GET /data)</h2>

      <button
        className="button secondary"
        onClick={loadItems}
        disabled={loading}
      >
        {loading ? "Caricamento..." : "Ricarica elenco"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {items.length > 0 && (
        <div style={{ maxHeight: 400, overflow: "auto", marginTop: 8 }}>
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Denominazione</th>
                <th>P.IVA</th>
                <th>Provincia</th>
                <th>Comune</th>
                <th>Created</th>
                <th>Azioni</th>
              </tr>
            </thead>
            <tbody>
              {items.map((it) => (
                <tr key={it.id}>
                  <td>{it.id}</td>
                  <td>{it.Anagrafica_denominazione}</td>
                  <td>{it.Anagrafica_partitaIva}</td>
                  <td>{it.Anagrafica_provincia}</td>
                  <td>{it.Anagrafica_comune}</td>
                  <td>{it.created_at}</td>
                  <td>
                    {accessLevel === "admin" ? (
                      <button
                        className="button danger"
                        onClick={() => handleDelete(it.Anagrafica_partitaIva)}
                        disabled={deletingPartitaIva === it.Anagrafica_partitaIva}
                      >
                        {deletingPartitaIva === it.Anagrafica_partitaIva
                          ? "Elimino..."
                          : "Elimina"}
                      </button>
                    ) : (
                      "-"
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {items.length === 0 && !loading && <p>Nessun item caricato.</p>}
    </div>
  );
}

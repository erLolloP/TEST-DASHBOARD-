import React from "react";
import HeaderBar from "./components/HeaderBar";
import Dashboard from "./components/Dashboard";
import ItemList from "./components/ItemList";
import CsvImport from "./components/CsvImport";
import CsvUpdate from "./components/CsvUpdate";
import CsvExport from "./components/CsvExport";
import DeleteItem from "./components/DeleteItem";
import OAuthCallback from "./components/OAuthCallback";

export default function App() {
  const accessGranted = true;
  const accessLevel = accessGranted ? "admin" : "read";

  const isCallbackRoute = window.location.pathname.includes("/callback");

  if (isCallbackRoute) {
    return <OAuthCallback />;
  }

  return (
    <div>
      <HeaderBar
        accessLevel={accessLevel}
      />

      <div className="app-container">
        {!accessGranted && (
          <div className="card app-locked-banner">
            <h2>Accesso bloccato</h2>
            <p>
              Completa la verifica del codice fiscale tramite ARPA per abilitare le funzioni
              dell&apos;applicazione.
            </p>
          </div>
        )}

        <div className={accessGranted ? "app-content" : "app-content app-content-disabled"}>
          <Dashboard accessLevel={accessLevel} />

          <ItemList accessLevel={accessLevel} />

          <div className="row" style={{ marginTop: 16 }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <CsvExport accessLevel={accessLevel} />
            </div>
          </div>

          <div className="row" style={{ marginTop: 16 }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <CsvImport accessLevel={accessLevel} />
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <CsvUpdate accessLevel={accessLevel} />
            </div>
          </div>

          <div className="row" style={{ marginTop: 16 }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <DeleteItem />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

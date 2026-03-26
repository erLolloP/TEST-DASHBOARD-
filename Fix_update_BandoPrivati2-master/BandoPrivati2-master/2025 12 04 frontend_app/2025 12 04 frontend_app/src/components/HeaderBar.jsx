import React, { useEffect, useState } from "react";
import { buildAuthorizationUrl, getStoredTokens, logout } from "../oauth";

export default function HeaderBar({
  accessLevel,
}) {
  const [authPreparing, setAuthPreparing] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(() => Boolean(getStoredTokens()));

  useEffect(() => {
    const syncLoginState = () => setIsLoggedIn(Boolean(getStoredTokens()));
    window.addEventListener("storage", syncLoginState);
    return () => {
      window.removeEventListener("storage", syncLoginState);
    };
  }, []);

  const handleAuthRedirect = async () => {
    setAuthPreparing(true);
    try {
      const url = await buildAuthorizationUrl();
      window.location.assign(url);
    } finally {
      setAuthPreparing(false);
    }
  };

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
      setIsLoggedIn(false);
    } finally {
      setLoggingOut(false);
    }
  };

  return (
    <header>
      <div className="header-top">
        <h1>Gestione Bando FSE privati</h1>
        <div className="header-actions">
          <button
            className="button primary"
            onClick={handleAuthRedirect}
            disabled={authPreparing}
          >
            Accedi tramite ARPA
          </button>
          <button
            className="button danger"
            onClick={handleLogout}
            disabled={loggingOut || !isLoggedIn}
          >
            {loggingOut ? "Pulizia..." : "Logout"}
          </button>
        </div>
      </div>
    </header>
  );
}

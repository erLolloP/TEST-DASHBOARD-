# Deploy locale con Docker (Backend + Frontend) su PowerShell

Questa guida permette a chiunque di clonare la repository, avviare i due container (`backend` e `frontend`) e testare subito le funzionalità con un file dati di esempio.

## Prerequisiti

- **Windows + PowerShell 5/7**
- **Docker Desktop** avviato
- Porte libere:
  - `8000` per il backend FastAPI
  - `8080` per il frontend (Nginx)

## Struttura utile della repo

- Backend: `2025 12 04 backend_fixed_defschema/2025 12 04 backend_fixed_defschema`
- Frontend: `2025 12 04 frontend_app/2025 12 04 frontend_app`
- Dati test (fuori da frontend/backend):
  - `dati_test_import.xlsx` (file Excel)
  - `dati_test_import.csv` (stesso contenuto in CSV, pronto per l'import API)

---

## 1) Avvio container Backend (API + Postgres)

Apri PowerShell nella root repo e lancia:

```powershell
Set-Location "C:\path\to\BandoPrivati2\2025 12 04 backend_fixed_defschema\2025 12 04 backend_fixed_defschema"
docker compose up -d --build
```

Verifica rapida:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8000/healthz
Invoke-RestMethod http://localhost:8000/readyz
```

Swagger API:

```text
http://localhost:8000/docs
```

---

## 2) Build e run container Frontend

Apri una nuova PowerShell e lancia:

```powershell
Set-Location "C:\path\to\BandoPrivati2\2025 12 04 frontend_app\2025 12 04 frontend_app"
docker build -t bando-frontend:local .
docker run -d --name bando-frontend -p 8080:80 bando-frontend:local
```

Verifica:

```powershell
docker ps
```

Frontend disponibile su:

```text
http://localhost:8080
```

> Nota: il frontend legge la configurazione da `/config/config.json` e in questa repo il `backendUrl` è già impostato su `http://localhost:8000`.

---

## 3) Import dati di test

Per testare l'import del backend puoi usare direttamente il CSV di esempio dalla root repo (`dati_test_import.csv`).

### Opzione A - Da frontend

- Vai su `http://localhost:8080`
- Sezione import CSV
- Carica `dati_test_import.csv`

### Opzione B - Da PowerShell (chiamata API diretta)

```powershell
$csvPath = "C:\path\to\BandoPrivati2\dati_test_import.csv"
curl.exe -X POST "http://localhost:8000/data/import-csv" `
  -H "X-Access-Level: admin" `
  -F "file=@$csvPath;type=text/csv"
```

---

## 4) Uso del file Excel (`.xlsx`)

Il backend espone endpoint di import **CSV**. Il file `dati_test_import.xlsx` è fornito per test/manual review in Excel.

Se vuoi importarlo via API:

1. apri `dati_test_import.xlsx` in Excel
2. salva come `CSV UTF-8 (delimitato da virgole) (*.csv)`
3. importa il CSV con i passaggi del punto 3

---

## 5) Arresto e pulizia

### Backend

```powershell
Set-Location "C:\path\to\BandoPrivati2\2025 12 04 backend_fixed_defschema\2025 12 04 backend_fixed_defschema"
docker compose down
```

Per rimuovere anche il volume DB:

```powershell
docker compose down -v
```

### Frontend

```powershell
docker stop bando-frontend
docker rm bando-frontend
```


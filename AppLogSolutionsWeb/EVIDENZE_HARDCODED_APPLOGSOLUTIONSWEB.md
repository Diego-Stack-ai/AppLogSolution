# EVIDENZE HARDCODED - AppLogSolutionsWeb

Questo documento contiene l'estrazione **reale e grezza** delle occorrenze richieste, senza segnaposti generici.

## 2. Project ID, URL, bucket e regioni
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `.firebaserc` | 3 | `"default": "log-solution-60007",` | Logica / Config | main & cantiere |
| `.firebaserc` | 4 | `"cantiere": "log-solutions-cantiere"` | Logica / Config | cantiere |
| `.github/workflows/deploy.yml` | 26 | `run: firebase deploy --only hosting --project log-solution-60007` | Logica / Config | main & cantiere |
| `.gitignore` | 3 | `backend/config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json` | Logica / Config | main & cantiere |
| `.gitignore` | 4 | `backend/config/log-solution-60007-firebase-adminsdk-*.json` | Logica / Config | main & cantiere |
| `.gitignore` | 61 | `backend/config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json` | Logica / Config | main & cantiere |
| `.gitignore` | 62 | `backend/config/log-solution-60007-firebase-adminsdk-*.json` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 181 | `* **Inizializzazione**: `frontend/core/firebase-init.js` seleziona la configurazione Dev (`log-solutions-cantiere`) o Pr` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 350 | `Storage Bucket (log-solutions-cantiere / log-solution-60007)` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 365 | `* **Ambiente Sviluppo**: `log-solutions-cantiere`` | Logica / Config | cantiere |
| `ARCHITECTURE.md` | 366 | `* **Ambiente Produzione**: `log-solution-60007`` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 25 | `* **PRODUZIONE**: Project ID `log-solution-60007`` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 40 | `firebase deploy --only hosting --project log-solution-60007` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 41 | `firebase deploy --only functions --project log-solution-60007` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 42 | `firebase deploy --only firestore:rules --project log-solution-60007` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 43 | `firebase deploy --only storage --project log-solution-60007` | Logica / Config | main & cantiere |
| `README.md` | 61 | `* **PRODUZIONE**: `log-solution-60007` (Consultare la sezione 13 di [`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLog` | Logica / Config | main & cantiere |
| `analizza_storage.py` | 13 | `'storageBucket': 'log-solution-60007.firebasestorage.app'` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 7 | `app = firebase_admin.initialize_app(None, {'storageBucket': 'log-solutions-sviluppo.firebasestorage.app'})` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F01-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/VERONA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F10-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F10-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F17-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F17-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `build_inventory.py` | 7 | `app = firebase_admin.initialize_app(None, {'storageBucket': 'log-solutions-sviluppo.firebasestorage.app'})` | Logica / Config | main & cantiere |
| `check_cantiere.py` | 4 | `os.environ["GCLOUD_PROJECT"] = "log-solutions-cantiere"` | Logica / Config | cantiere |
| `check_cantiere.py` | 18 | `bucket = storage.bucket("log-solutions-cantiere.appspot.com")` | Logica / Config | cantiere |
| `check_cantiere_offline.py` | 2 | `os.environ["GCLOUD_PROJECT"] = "log-solutions-cantiere"` | Logica / Config | cantiere |
| `check_cantiere_offline.py` | 10 | `bucket = storage.bucket("log-solutions-cantiere.appspot.com")` | Logica / Config | cantiere |
| `check_cantiere_offline2.py` | 7 | `'storageBucket': 'log-solutions-cantiere.appspot.com'` | Logica / Config | cantiere |
| `check_deliveries.py` | 4 | `db = firestore.Client(project="log-solutions-cantiere")` | Logica / Config | cantiere |
| `clean_cattel_dryrun.py` | 16 | `app = firebase_admin.initialize_app(None, {'storageBucket': 'log-solutions-sviluppo.firebasestorage.app'})` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 22 | `if pid == "log-solution-60007":` | Logica / Config | main & cantiere |
| `deep_audit_25_07.py` | 15 | `app = firebase_admin.initialize_app(None, {'storageBucket': 'log-solutions-sviluppo.firebasestorage.app'})` | Logica / Config | main & cantiere |
| `deep_audit_25_07.py` | 22 | `if PROJECT_ID != "log-solutions-sviluppo" or BUCKET_NAME != "log-solutions-sviluppo.firebasestorage.app":` | Logica / Config | main & cantiere |
| `download_file.py` | 6 | `app = firebase_admin.initialize_app(cred, {'storageBucket': 'log-solution-60007.firebasestorage.app'})` | Logica / Config | main & cantiere |
| `dr_system/MANUALE_GESTIONE_UMANA_DR.md` | 112 | `2. Sostituisci il nome del progetto nel file `.firebaserc` (da `log-solution-60007` a `log-solution-rinato`).` | Logica / Config | main & cantiere |
| `dr_system/dr_orchestrator.py` | 62 | `cmd = f"gsutil -m rsync -r gs://log-solution-60007.appspot.com {GCS_BUCKET}/tmp/storage/"` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 1 | `2026/07/24-16:38:59.351 71d8 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 3 | `2026/07/24-16:38:59.793 71d8 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG.old` | 1 | `2026/07/24-16:38:44.105 1284 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\Defau` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG.old` | 2 | `2026/07/24-16:38:44.804 1284 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 1 | `2026/07/24-15:45:18.683 6f3c Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 2 | `2026/07/24-15:45:19.578 6f3c Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 1 | `2026/07/25-10:40:28.306 4544 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 2 | `2026/07/25-10:40:28.703 4544 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `e2e-tests/debug_playwright.py` | 7 | `context = await browser.new_context(base_url='https://log-solutions-sviluppo.web.app')` | Logica / Config | main & cantiere |
| `e2e-tests/playwright.config.js` | 24 | `baseURL: 'https://log-solutions-sviluppo.web.app',` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/orchestrate-test8.js` | 72 | `await page.goto('https://log-solutions-sviluppo.web.app/login.html');` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/orchestrate-test8.js` | 86 | `const securityOrigin = 'https://log-solutions-sviluppo.web.app';` | Variable Assignment | main & cantiere |
| `e2e-tests/scripts/poc-cdp.js` | 87 | `console.log("Navigazione in corso su https://log-solutions-sviluppo.web.app/ ...");` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/poc-cdp.js` | 89 | `await page.goto('https://log-solutions-sviluppo.web.app/', { waitUntil: 'networkidle' });` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/test10-continuity.js` | 17 | `await page.goto('https://log-solutions-sviluppo.web.app/login.html');` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/test10-continuity.js` | 26 | `await context.route('https://log-solutions-sviluppo.web.app/sw.js', async route => {` | JS Function | main & cantiere |
| `e2e-tests/test_login.py` | 8 | `await page.goto('https://log-solutions-sviluppo.web.app/login.html')` | Logica / Config | main & cantiere |
| `e2e-tests/tests/auth/auth.spec.js` | 27 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/auth/auth.spec.js` | 48 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/auth/auth.spec.js` | 66 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa-rollback.spec.js` | 9 | `await page.goto('https://log-solutions-sviluppo.web.app/');` | Logica / Config | main & cantiere |
| `e2e-tests/tests/pwa/pwa-update-fallback.spec.js` | 12 | `await page.goto('https://log-solutions-sviluppo.web.app/');` | Logica / Config | main & cantiere |
| `e2e-tests/tests/pwa/pwa-update-fallback.spec.js` | 37 | `await page.goto('https://log-solutions-sviluppo.web.app/');` | Logica / Config | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 52 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 77 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 103 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 129 | `const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-sviluppo.web.app' ` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/smoke/smoke.spec.js` | 6 | `// - apra https://log-solutions-sviluppo.web.app;` | Logica / Config | main & cantiere |
| `fast_audit.py` | 7 | `app = firebase_admin.initialize_app(None, {'storageBucket': 'log-solutions-sviluppo.firebasestorage.app'})` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 31 | `const isLocal = window.location.hostname === 'localhost' \|\| window.location.hostname === '127.0.0.1';` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 25 | `environment: window.location.hostname === 'localhost' \|\| window.location.hostname === '127.0.0.1' ? 'development' : 'p` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 33 | `if (hostname.includes('log-solutions-sviluppo') \|\| hostname.includes('--sviluppo') \|\| hostname.includes('localhost')` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 72 | `url.includes('localhost') \|\|` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 73 | `url.includes('127.0.0.1') \|\|` | Logica / Config | main & cantiere |
| `frontend/centro_costi.html` | 143 | `const functions = getFunctions(app, "europe-west1"); // Manteniamo la region usata di solito` | Variable Assignment | main & cantiere |
| `frontend/core/auth-service.js` | 10 | `const isLocal = window.location.hostname === 'localhost' \|\| window.location.hostname === '127.0.0.1';` | Variable Assignment | main & cantiere |
| `frontend/elaborazione.html` | 391 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | main |
| `frontend/elaborazione.html` | 414 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | cantiere |
| `frontend/fatturazione.html` | 1589 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | main & cantiere |
| `frontend/firebase-config-env.js` | 5 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/firebase-config-env.js` | 6 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/firebase-config-env.js` | 7 | `storageBucket: "log-solution-60007.firebasestorage.app",` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 6 | `authDomain: "log-solution-60007.web.app",` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 7 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 8 | `storageBucket: "log-solution-60007.firebasestorage.app",` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 15 | `authDomain: "log-solutions-cantiere.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 16 | `projectId: "log-solutions-cantiere",` | Logica / Config | cantiere |
| `frontend/firebase-config.js` | 17 | `storageBucket: "log-solutions-cantiere.firebasestorage.app",` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 24 | `const isDevEnvironment = window.location.hostname.includes('log-solutions-cantiere') \|\|` | Variable Assignment | cantiere |
| `frontend/firebase-config.js` | 25 | `window.location.hostname === 'localhost' \|\|` | Logica / Config | main |
| `frontend/firebase-config.js` | 26 | `window.location.hostname === 'localhost' \|\|` | Logica / Config | main & cantiere |
| `frontend/firebase-config.js` | 27 | `window.location.hostname === '127.0.0.1';` | Logica / Config | cantiere |
| `frontend/firebase-config.js` | 32 | `console.log("[Firebase Config] ATTENZIONE: Connesso all'AMBIENTE CANTIERE (log-solutions-cantiere)");` | Logica / Config | cantiere |
| `frontend/firebase-config.js` | 33 | `console.log("[Firebase Config] Connesso alla PRODUZIONE PRINCIPALE (log-solution-60007)");` | Logica / Config | main |
| `frontend/firebase-config.js` | 34 | `console.log("[Firebase Config] Connesso alla PRODUZIONE PRINCIPALE (log-solution-60007)");` | Logica / Config | cantiere |
| `frontend/impostazioni.html` | 1364 | `const functions = getFunctions(app, 'europe-west1');` | Variable Assignment | main & cantiere |
| `frontend/impostazioni.html` | 1442 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | main & cantiere |
| `frontend/link_viaggi.html` | 222 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | main & cantiere |
| `frontend/mappa_zone.html` | 1380 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | main & cantiere |
| `frontend/mappa_zone.html` | 3866 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 4017 | `const functions = getFunctions(app, "europe-west1");` | Variable Assignment | cantiere |
| `frontend/mappe_autisti/GranChef V01_B_Zone_GranChef_V01_B_09-06-2026.html` | 170 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_B_Zone_GranChef_V01_B_09-06-2026.html` | 171 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_B_Zone_GranChef_V01_B_09-06-2026.html` | 172 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_03-06-2026.html` | 170 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_03-06-2026.html` | 171 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_03-06-2026.html` | 172 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_09-06-2026.html` | 170 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_09-06-2026.html` | 171 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_09-06-2026.html` | 172 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V02_Zone_GranChef_V02_03-06-2026.html` | 230 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V02_Zone_GranChef_V02_03-06-2026.html` | 231 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V02_Zone_GranChef_V02_03-06-2026.html` | 232 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V03_Zone_GranChef_V03_03-06-2026.html` | 280 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V03_Zone_GranChef_V03_03-06-2026.html` | 281 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V03_Zone_GranChef_V03_03-06-2026.html` | 282 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V04_Zone_GranChef_V04_03-06-2026.html` | 200 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V04_Zone_GranChef_V04_03-06-2026.html` | 201 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V04_Zone_GranChef_V04_03-06-2026.html` | 202 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V05_Zone_GranChef_V05_03-06-2026.html` | 150 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V05_Zone_GranChef_V05_03-06-2026.html` | 151 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V05_Zone_GranChef_V05_03-06-2026.html` | 152 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V06_Zone_GranChef_V06_03-06-2026.html` | 240 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V06_Zone_GranChef_V06_03-06-2026.html` | 241 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V06_Zone_GranChef_V06_03-06-2026.html` | 242 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Ayoub_Zone_GranChef_V03_09-06-2026_-_Dopo_la_divisone_bolle.html` | 293 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Ayoub_Zone_GranChef_V03_09-06-2026_-_Dopo_la_divisone_bolle.html` | 294 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Ayoub_Zone_GranChef_V03_09-06-2026_-_Dopo_la_divisone_bolle.html` | 295 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Baye_Zone_GranChef_V02_09-06-2026_-_Dopo_la_divisone_bolle.html` | 297 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Baye_Zone_GranChef_V02_09-06-2026_-_Dopo_la_divisone_bolle.html` | 298 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Baye_Zone_GranChef_V02_09-06-2026_-_Dopo_la_divisone_bolle.html` | 299 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Costantin_Zone_GranChef_V01_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 167 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Costantin_Zone_GranChef_V01_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 168 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Costantin_Zone_GranChef_V01_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 169 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_01-06-2026.html` | 278 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_01-06-2026.html` | 279 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_01-06-2026.html` | 280 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_08-06-2026.html` | 278 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_08-06-2026.html` | 279 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_08-06-2026.html` | 280 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_04-06-2026.html` | 271 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_04-06-2026.html` | 272 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_04-06-2026.html` | 273 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_08-06-2026.html` | 227 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_08-06-2026.html` | 228 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_08-06-2026.html` | 229 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_11-06-2026.html` | 215 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_11-06-2026.html` | 216 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_11-06-2026.html` | 217 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026.html` | 261 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026.html` | 262 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026.html` | 263 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026_-_Copia.html` | 261 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026_-_Copia.html` | 262 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026_-_Copia.html` | 263 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_13-06-2026.html` | 261 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_13-06-2026.html` | 262 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_13-06-2026.html` | 263 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_16-06-2026.html` | 261 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_16-06-2026.html` | 262 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_16-06-2026.html` | 263 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_04-06-2026.html` | 245 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_04-06-2026.html` | 246 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_04-06-2026.html` | 247 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_08-06-2026.html` | 266 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_08-06-2026.html` | 267 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_08-06-2026.html` | 268 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_GranChef_V02_12-06-2026_-_Copia.html` | 251 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_GranChef_V02_12-06-2026_-_Copia.html` | 252 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_GranChef_V02_12-06-2026_-_Copia.html` | 253 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_05-06-2026.html` | 274 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_05-06-2026.html` | 275 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_05-06-2026.html` | 276 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_08-06-2026.html` | 215 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_08-06-2026.html` | 216 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_08-06-2026.html` | 217 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_16-06-2026.html` | 271 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_16-06-2026.html` | 272 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_16-06-2026.html` | 273 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_B_12-06-2026.html` | 251 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_B_12-06-2026.html` | 252 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_B_12-06-2026.html` | 253 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V03_11-06-2026.html` | 218 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V03_11-06-2026.html` | 219 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V03_11-06-2026.html` | 220 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_11-06-2026.html` | 215 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_11-06-2026.html` | 216 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_11-06-2026.html` | 217 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026.html` | 248 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026.html` | 249 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026.html` | 250 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 196 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 197 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 198 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_16-06-2026.html` | 290 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_16-06-2026.html` | 291 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_16-06-2026.html` | 292 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V02_B_01-06-2026.html` | 278 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V02_B_01-06-2026.html` | 279 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V02_B_01-06-2026.html` | 280 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_04-06-2026.html` | 232 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_04-06-2026.html` | 233 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_04-06-2026.html` | 234 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_05-06-2026.html` | 248 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_05-06-2026.html` | 249 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_05-06-2026.html` | 250 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_08-06-2026.html` | 290 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_08-06-2026.html` | 291 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_08-06-2026.html` | 292 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_B_08-06-2026.html` | 272 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_B_08-06-2026.html` | 273 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_B_08-06-2026.html` | 274 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 235 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 236 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 237 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_16-06-2026.html` | 258 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_16-06-2026.html` | 259 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_16-06-2026.html` | 260 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_B_12-06-2026.html` | 235 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_B_12-06-2026.html` | 236 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_B_12-06-2026.html` | 237 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V02_01-06-2026.html` | 278 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V02_01-06-2026.html` | 279 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V02_01-06-2026.html` | 280 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V03_B_08-06-2026.html` | 257 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V03_B_08-06-2026.html` | 258 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V03_B_08-06-2026.html` | 259 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 167 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 168 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 169 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_16-06-2026.html` | 206 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_16-06-2026.html` | 207 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_16-06-2026.html` | 208 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Orjito_Zone_GranChef_V01_B_09-06-2026_-_Dopo_la_divisone_bolle.html` | 225 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Orjito_Zone_GranChef_V01_B_09-06-2026_-_Dopo_la_divisone_bolle.html` | 226 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Orjito_Zone_GranChef_V01_B_09-06-2026_-_Dopo_la_divisone_bolle.html` | 227 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Titti_Zone_GranChef_V03_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 271 | `authDomain: "log-solution-60007.firebaseapp.com",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Titti_Zone_GranChef_V03_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 272 | `projectId: "log-solution-60007",` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Titti_Zone_GranChef_V03_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 273 | `storageBucket: "log-solution-60007.appspot.com",` | Logica / Config | main & cantiere |

*(Mostrati primi 300 risultati su 606 reali per questa categoria)*

## 3. Occorrenze tenant
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `.gitignore` | 13 | `**/FRUTTA/` | Logica / Config | main & cantiere |
| `.gitignore` | 14 | `**/LATTE/` | Logica / Config | main & cantiere |
| `.gitignore` | 71 | `**/FRUTTA/` | Logica / Config | main & cantiere |
| `.gitignore` | 72 | `**/LATTE/` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 20 | `9. [Pipeline Specifiche: DNR Frutta e Latte](#9-pipeline-specifiche-dnr-frutta-e-latte) `[STATO ATTUALE CONFERMATO]`` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 21 | `10. [Pipeline Specifiche: CATTEL, GRAN CHEF e Altri](#10-pipeline-specifiche-cattel-gran-chef-e-altri) `[STATO ATTUALE C` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 87 | `I committenti (**DNR, CATTEL, GRAN CHEF, BAUER, HOTEL**, ecc.) sono i clienti commerciali di Loge Solution. I committent` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 92 | `* **DNR è un committente cliente come gli altri e NON è il tenant radice o proprietario dell'app**.` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 100 | `* `tenantId`: Identificativo del committente (`"DNR"`, `"CATTEL"`, `"GRAN CHEF"`).` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 101 | `* `sourceChannel`: Canale documentale sorgente (`"FRUTTA"`, `"LATTE"`, `"EXCEL_CATTEL"`).` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 103 | `* `zonaLogistica`: Area geografica distributiva (`"ZONA 1"`, `"CATTEL MESTRE"`).` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 105 | `3. **Canali DNR**: `DNR_FRUTTA` e `DNR_LATTE` sono rappresentati come `tenantId = "DNR"` con `sourceChannel = "FRUTTA"` ` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 106 | `4. **Divieto Fallback Automatico**: Se un dato arriva senza `tenantId`, deve essere bloccato o posto in quarantena (`pro` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 119 | `\| **Anagrafica Punti DNR** \| DNR \| Tenant-Specifico \| `clienti/DNR/raccolta clienti`. Codici cliente e note DNR. \|` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 120 | `\| **Anagrafica Punti Cattel**\| CATTEL \| Tenant-Specifico \| `clienti/CATTEL/raccolta clienti`. Codici cliente Cattel.` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 121 | `\| **Anagrafica GranChef** \| GRAN CHEF \| Tenant-Specifico \| `clienti/GRAN CHEF/raccolta clienti`. Codici GranChef. \|` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 136 | `DNR["Committente DNR` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 138 | `CTL["Committente CATTEL` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 140 | `GC["Committente GRAN CHEF` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 160 | `DNR --> INGEST` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 227 | `## 9. PIPELINE SPECIFICHE: DNR FRUTTA E LATTE `[STATO ATTUALE CONFERMATO]`` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 229 | `1. **Input**: PDF cumulativi per i canali `FRUTTA` (es. Progetto Scuole) o `LATTE`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 232 | `4. **Merge Fermata Fisica (Regola Commerciale DNR)**:` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 239 | `## 10. PIPELINE SPECIFICHE: CATTEL, GRAN CHEF E ALTRI `[STATO ATTUALE CONFERMATO]`` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 241 | `* **CATTEL**: Ingestione file Excel multi-foglio via `_processa_excel_cattel_core_logic`. Ogni foglio rappresenta un gir` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 242 | `* **GRAN CHEF**: Ingestione liste consegne GranChef. Raggruppamento per codice cliente GranChef.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 249 | ``[DEBITO TECNICO]`: Attualmente, se Cattel e GranChef servono lo stesso ristorante allo stesso indirizzo, esistono due d` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 262 | `"tenantId": "CATTEL",` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 284 | `1. **`ORIGINAL_DDT`**: Documento PDF originale estratto dai file sorgente (es. DNR).` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 332 | `├── DNR/` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 337 | `├── CATTEL/` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 340 | `└── GRAN CHEF/` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 352 | `├── split_ddt/{data}/          [PDF estratti dai job DNR]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 353 | `├── REPORTS/{data}/            [Report fisici DNR (Asimmetria Legacy)]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 354 | `├── CATTEL/REPORTS/{data}/     [Report fisici CATTEL]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 355 | `├── GRAN CHEF/REPORTS/{data}/  [Report fisici GRAN CHEF]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 421 | `* **Fase E — Uniformazione Storage**: Migrazione dei report DNR sotto `DNR/REPORTS/{data}/`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 432 | `4. **🟠 ALTO — Asimmetria Storage DNR**: DNR salva nella root `REPORTS/` anziché sotto `DNR/REPORTS/`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 433 | `5. **🟠 ALTO — Fallback Hardcoded DNR**: Presenza di `\|\| 'DNR'` nel backend Python e nel frontend JS.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 442 | `* **Contesto**: DNR era trattato come tenant radice con privilegi strutturali nel codice.` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 443 | `* **Decisione**: DNR è ridimensionato a committente normale e paritetico. `DNR_FRUTTA` e `DNR_LATTE` diventano `tenantId` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 444 | `* **Alternative Considerate**: Mantenere DNR come radice o dividere DNR in due tenant separati (scartate perché violano ` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 445 | `* **Conseguenze**: Necessità di normalizzazione nei parser e rimozione dei fallback `\|\| 'DNR'`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 456 | `\| **Committente / Tenant** \| Cliente aziendale che commissiona i trasporti (DNR, Cattel, GranChef, Bauer). \| `[CHIARO` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 457 | `\| **tenantId** \| Identificativo univoco del committente (es. `"DNR"`, `"CATTEL"`). \| `[CHIARO]` \|` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 458 | `\| **sourceChannel** \| Canale documentale sorgente (es. `"FRUTTA"`, `"LATTE"`, `"EXCEL_CATTEL"`). \| `[CHIARO]` \|` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 459 | `\| **zonaLogistica** \| Area geografica o giro distributivo (es. `"ZONA 1"`, `"CATTEL MESTRE"`). \| `[CHIARO]` \|` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 10 | `- Tenant coinvolti in Produzione: CATTEL, GRAN CHEF` | Tenant Setup | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 11 | `- Tenant coinvolti in Sviluppo: CATTEL, GRAN CHEF` | Tenant Setup | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 48 | `- ID: 25-07-2026_GC_NFlzc9QY6bTwU2arBZHJ (GRAN CHEF) - Titolo: 'Gran Chef 01' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 49 | `- ID: 25-07-2026_GC_cnMvVgZRMCgMtbIQKK7O (GRAN CHEF) - Titolo: 'Gran Chef 02' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 50 | `- ID: 25-07-2026_CATTEL_FL142GN_Daniel  Puscas (CATTEL) - Titolo: 'Cattel FL142GN' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 51 | `- ID: 25-07-2026_CATTEL_LOG01_Ahmed Shahbaz (CATTEL) - Titolo: 'Cattel LOG01' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 52 | `- ID: 25-07-2026_CATTEL_LOG02_Sufyan Ahmed (CATTEL) - Titolo: 'Cattel LOG02' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 55 | `- ID: 25-07-2026_GRAN_CHEF_GC_VDtEBPNlWfJgHR5Oiuo8_01_6330df99e3a3 (GRAN CHEF) - Titolo: 'GRAN CHEF 02' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 56 | `- ID: 25-07-2026_GRAN_CHEF_GC_eGy732K2cDvyhcqlBDK8_01_922f7e3dc350 (GRAN CHEF) - Titolo: 'GRAN CHEF 01' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 57 | `- ID: 25-07-2026_CATTEL_0000_01_bda95be14aaa (CATTEL) - Titolo: '0000 - NON ASSEGNATO' - Punti: 0 / 0` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 61 | `- LockID: 04b738137acccda5fd21e49a - Titolo: GRAN CHEF 01 - Job: eGy732K2cDvyhcqlBDK8` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 62 | `- LockID: cd2aacb766cffbf64a096cd8 - Titolo: GRAN CHEF 02 - Job: VDtEBPNlWfJgHR5Oiuo8` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 1 | `# Memoria Storica: Disaccoppiamento DNR e Isolamento Totale Tenant` | Tenant Setup | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 6 | `Attualmente il sistema utilizza in modo improprio il committente "DNR" trattandolo come una sorta di tenant "radice" (ro` | Tenant Setup | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 9 | `Nel codice frontend e nelle funzioni, DNR è spesso hardcoded in questo modo:` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 10 | `1. Come **Fallback globale**: `const activeTenant = localStorage.getItem('activeTenant') \|\| 'DNR';`.` | Variable Assignment | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 11 | `2. Come **Percorso di Salvataggio Forzato**: Molte schermate di impostazioni o pianificazione salvano o leggono dati pun` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 12 | `3. Come **Padrone dei Reports**: Su Google Cloud Storage i file vengono salvati nella root se il tenant è DNR, o in sott` | Tenant Setup | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 13 | `Tutto questo causa il riversamento (o "risucchio") di viaggi e dati di vari committenti all'interno della cartella DNR, ` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 18 | `- **Flussi di Importazione**: Indagare sugli script di importazione (es. file Excel dei viaggi o dei KPI) per vedere se ` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 19 | `- **Creazione Pianificazione**: Analizzare il momento esatto in cui un dispatcher crea o assegna un viaggio, per evitare` | Tenant Setup | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 20 | `- **Smistamento alla Nascita**: Assicurarsi che qualsiasi dato in entrata sia obbligato a dichiarare il suo *vero* tenan` | Tenant Setup | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 23 | `Una volta avviato questo cantiere, bisognerà intervenire sui seguenti file per rimuovere i riferimenti a DNR:` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 52 | `\| **Committente / Tenant** \| Cliente aziendale (es. DNR, Cattel, GranChef, Bauer) che affida le merci ed i punti di co` | Tenant Setup | main & cantiere |
| `DOMAIN_MODEL.md` | 53 | `\| **tenantId** \| Identificativo stringa univoco del committente (`"DNR"`, `"CATTEL"`, `"GRAN CHEF"`). \| Client Tenant` | Tenant Setup | main & cantiere |
| `DOMAIN_MODEL.md` | 54 | `\| **sourceChannel** \| Canale documentale sorgente del committente (`"FRUTTA"`, `"LATTE"`, `"EXCEL_CATTEL"`). \| Client` | Tenant Setup | main & cantiere |
| `DOMAIN_MODEL.md` | 60 | `\| **Zona Logistica** \| Area distributiva o raggruppamento logico iniziale di consegne (es. `"ZONA 1"`, `"CATTEL MESTRE` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 73 | `1. **Pariteticità dei Tenant**: DNR non è il tenant radice o proprietario dell'app, ma un committente cliente come gli a` | Tenant Setup | main & cantiere |
| `DOMAIN_MODEL.md` | 74 | `2. **Canali DNR**: `DNR_FRUTTA` e `DNR_LATTE` non sono due tenant distinti, ma rappresentano `tenantId = "DNR"` con `sou` | Tenant Setup | main & cantiere |
| `DOMAIN_MODEL.md` | 92 | `* **DNR**: Genera `ORIGINAL_DDT` estratti dai PDF cumulativi.` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 111 | `3. **Divieto Fallback DNR**: Se un dato arriva senza `tenantId`, non deve mai essere assegnato automaticamente a DNR, ma` | Tenant Setup | main & cantiere |
| `PROJECT_MANIFEST.md` | 363 | `* **Scopo del Capitolo**: Raccontare la nascita dell'infrastruttura, dalle prime soluzioni locali accentrate su un unico` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 403 | `* **Scopo del Capitolo**: Descrivere la filosofia di isolamento e pariteticità dei committenti (DNR, Cattel, GranChef, B` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 483 | `* **Scopo del Capitolo**: Definire l’identità aziendale dei clienti di Loge Solution (DNR, Cattel, GranChef, Bauer), la ` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 23 | `viaggi = db.collection('clienti').document('CATTEL').collection('viaggi ddt').where('data_lavoro', '==', '25-07-2026').s` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 27 | `doc = db.collection('clienti').document('CATTEL').collection('viaggi ddt').document(trip_id).get()` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 32 | `jobs = db.collection('clienti').document('CATTEL').collection('processing_jobs').where('dataViaggi', '==', '25-07-2026')` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 35 | `doc = db.collection('clienti').document('CATTEL').collection('processing_jobs').document('jgsbJytUKVtXWx0nKwRd').get()` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 40 | `locks = db.collection('clienti').document('CATTEL').collection('trip_title_locks').stream()` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 49 | `if 'CATTEL' in b.name and '25-07-2026' in b.name and 'REPORTS' not in b.name and 'input_pdf_fornitore' not in b.name:` | Logica / Config | main & cantiere |
| `audit_script.py` | 22 | `TENANTS = ['DNR', 'GRAN CHEF', 'CATTEL', 'BAUER', 'Cattel', 'PROGETTO SCUOLE']` | Tenant Setup | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_RvfDgA7vTgPOCWFev6bf", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_IUnudti8E1xuOJbcny4h", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_HmOYhzXBoEmSLHJrj7yx", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_yBowXvD09AGG9nRuYXNP", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_ST1cCLlNAoPwDcCnsfz9", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_IpdDOAYHXbateOKF7fDr", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_WB8HvCPskBeYXE0fgQ2K", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_PMSf3j9KkMAfKIb6g4Hs", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_ATokDLgLMW8wcDJ2coTI", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_9OSUtpWGlGgyayqREaXt", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_SX0TeTXxrKxpfH0LUzLx", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_gMQl9Okd6dKZEKDWolXT", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_EJfUFNhevPekJgIyZSjZ", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_5rQbqVkltvci6YvwItlB", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_Yvl68iTFs9xxpXd1ou1P", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_bVSo0d6mC1XLm7RP45Si", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_Cdrw8xhdaGtbt2YnkkY3", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_ms9z66rr63d7n67Smorq", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/30-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_tCi3HZk0LI2yeJBZTBGP", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `build_inventory.py` | 23 | `viaggio_ref = db.collection('clienti').document('CATTEL').collection('viaggi ddt').document(trip_id)` | Logica / Config | main & cantiere |
| `build_inventory.py` | 29 | `jobs = db.collection('clienti').document('CATTEL').collection('processing_jobs').stream()` | Logica / Config | main & cantiere |
| `build_inventory.py` | 36 | `locks = db.collection('clienti').document('CATTEL').collection('trip_title_locks').stream()` | Logica / Config | main & cantiere |
| `build_inventory.py` | 45 | `if 'CATTEL' in b.name and '25-07-2026' in b.name:` | Logica / Config | main & cantiere |
| `check_cantiere.py` | 24 | `jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\` | Logica / Config | cantiere |
| `check_cantiere_offline.py` | 15 | `jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\` | Logica / Config | cantiere |
| `check_cantiere_offline2.py` | 15 | `jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\` | Logica / Config | cantiere |
| `check_cantiere_offline2.py` | 69 | `if etichetta == 'CATTEL':` | Logica / Config | cantiere |
| `check_cantiere_offline2.py` | 71 | `if etichetta == 'GRAND_CHEF':` | Logica / Config | cantiere |
| `check_deliveries.py` | 5 | `doc = db.collection("clienti").document("DAC").collection("reports_logistici").document("01-08-2026").get()` | Logica / Config | cantiere |
| `check_fields.py` | 7 | `doc = next(db.collection('clienti').document('DNR').collection('viaggi ddt').limit(1).stream())` | Logica / Config | main & cantiere |
| `check_fields2.py` | 7 | `viaggi = db.collection('clienti').document('DNR').collection('viaggi ddt').stream()` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 37 | `"clienti/CATTEL/viaggi ddt/25-07-2026_CATTEL_0000_01_bda95be14aaa",` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 38 | `"clienti/CATTEL/trip_title_locks/65c48b90050d571b38947b8f",` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 39 | `"clienti/CATTEL/processing_jobs/jgsbJytUKVtXWx0nKwRd"` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 43 | `("split_ddt/25-07-2026/CATTEL/1701002166-1791002678_25-07-2026.pdf", 1785091167790938),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 44 | `("split_ddt/25-07-2026/CATTEL/1701002166-1791002775_25-07-2026.pdf", 1785091168399077),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 45 | `("split_ddt/25-07-2026/CATTEL/1701006035-1791002895_25-07-2026.pdf", 1785091161665773),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 46 | `("split_ddt/25-07-2026/CATTEL/1701006224-1791003002_25-07-2026.pdf", 1785091158623274),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 47 | `("split_ddt/25-07-2026/CATTEL/1701009992-0_25-07-2026.pdf", 1785091160457987),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 48 | `("split_ddt/25-07-2026/CATTEL/1701010117-1791006103_25-07-2026.pdf", 1785091167190148),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 49 | `("split_ddt/25-07-2026/CATTEL/1701010720-0_25-07-2026.pdf", 1785091163506742),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 50 | `("split_ddt/25-07-2026/CATTEL/1701011001-0_25-07-2026.pdf", 1785091165375817),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 51 | `("split_ddt/25-07-2026/CATTEL/1701011323-0_25-07-2026.pdf", 1785091162272307),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 52 | `("split_ddt/25-07-2026/CATTEL/1701012821-0_25-07-2026.pdf", 1785091161057526),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 53 | `("split_ddt/25-07-2026/CATTEL/1701012866-1791007265_25-07-2026.pdf", 1785091162880820),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 54 | `("split_ddt/25-07-2026/CATTEL/1701013049-1791006800_25-07-2026.pdf", 1785091159236572),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 55 | `("split_ddt/25-07-2026/CATTEL/1701078754-0_25-07-2026.pdf", 1785091165978803),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 56 | `("split_ddt/25-07-2026/CATTEL/1701078766-0_25-07-2026.pdf", 1785091166584952),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 57 | `("split_ddt/25-07-2026/CATTEL/1701081272-0_25-07-2026.pdf", 1785091164117202),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 58 | `("split_ddt/25-07-2026/CATTEL/1701081272-1791001159_25-07-2026.pdf", 1785091164753144),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 59 | `("split_ddt/25-07-2026/CATTEL/1701081397-0_25-07-2026.pdf", 1785091169612392),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 60 | `("split_ddt/25-07-2026/CATTEL/1701082502-0_25-07-2026.pdf", 1785091159851505),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 61 | `("split_ddt/25-07-2026/CATTEL/1701084326-0_25-07-2026.pdf", 1785091170249923),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 62 | `("split_ddt/25-07-2026/CATTEL/1701088880-0_25-07-2026.pdf", 1785091169001565),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 63 | `("split_ddt/25-07-2026/CATTEL/ddt_estratti_jgsbJytUKVtXWx0nKwRd.json", 1785091170405308)` | Logica / Config | main & cantiere |
| `core_genera_completo_giornata.py` | 1 | `def core_genera_completo_giornata(data_consegna, tenant='DNR'):` | Python Function Def | cantiere |
| `core_genera_completo_giornata.py` | 5 | `path_base = f'{tenant}/REPORTS/{data_consegna}' if tenant != 'DNR' else f'REPORTS/{data_consegna}'` | Tenant Setup | cantiere |
| `core_genera_completo_giornata.py` | 34 | `for doc in db.collection('clienti').document('DNR').collection('rientri ddt').stream():` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 69 | `match = next((d for d in deliveries_all if str(d.get('codice_consegna')).strip().lower() == cf and d.get('tipo') in ('FR` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 79 | `match = next((d for d in deliveries_all if str(d.get('codice_consegna')).strip().lower() == cl and d.get('tipo') in ('LA` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 122 | `doc_ref = get_db().collection('clienti').document('DNR').collection('viaggi ddt').document(viaggio_id)` | Logica / Config | cantiere |
| `count_gc.py` | 18 | `if 'GC' in str(d.get('id_zona', '')) or 'GRAN CHEF' in str(d.get('nome_giro', '')).upper():` | Logica / Config | main & cantiere |
| `count_gc.py` | 21 | `print(f"Tenant '{cliente.id}': {c} viaggi a Luglio (di cui {gc_count} sembrano associati a GRAN CHEF tramite id_zona/nom` | Tenant Setup | main & cantiere |
| `create_user.js` | 13 | `const dipendenteRef = db.collection('clienti').doc('DNR').collection('dipendenti').doc(uid);` | Variable Assignment | cantiere |
| `deep_audit_25_07.py` | 172 | `for t in ["CATTEL", "GRAN_CHEF", "GRAND_CHEF", "DNR", "BAUER", "GRAN CHEF"]:` | Logica / Config | main & cantiere |
| `extract_more.py` | 15 | `TENANTS = ['DNR', 'GRAN CHEF', 'CATTEL']` | Tenant Setup | main & cantiere |
| `extract_viaggi.py` | 15 | `TENANTS = ['DNR', 'GRAN CHEF', 'CATTEL', 'BAUER', 'Cattel', 'PROGETTO SCUOLE']` | Tenant Setup | main & cantiere |
| `find_dev_data.py` | 9 | `print("--- INVENTARIO CATTEL DEV (25-07-2026) ---")` | Logica / Config | main & cantiere |
| `find_dev_data.py` | 13 | `jobs = db.collection('processing_jobs').where('tenant', '==', 'CATTEL').where('dataViaggi', '==', '25-07-2026').stream()` | Tenant Setup | main & cantiere |
| `find_dev_data.py` | 20 | `viaggi = db.collection('viaggi_camion').where('tenant', '==', 'CATTEL').where('data', '==', '25-07-2026').stream()` | Tenant Setup | main & cantiere |
| `find_dev_data.py` | 27 | `locks = db.collection('title_locks').where('tenant', '==', 'CATTEL').where('data', '==', '25-07-2026').stream()` | Tenant Setup | main & cantiere |
| `firestore.rules` | 90 | `// Regole per il nuovo sistema Tenant (DNR)` | Tenant Setup | main & cantiere |
| `firestore.rules.backup` | 53 | `// Regole per il nuovo sistema Tenant (DNR)` | Tenant Setup | main & cantiere |
| `fix_anomalie.py` | 12 | `r"\1\2const activeTenant = localStorage.getItem('activeTenant') \|\| 'DNR';\n\2\3",` | Variable Assignment | cantiere |
| `fix_anomalie.py` | 16 | `# 2. Replace hardcoded DNR in onSnapshot paths with activeTenant` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 18 | `r"collection\(db, 'clienti', 'DNR', 'nuovi codici consegna'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 24 | `r"collection\(db, 'clienti', 'DNR', 'nuovi articoli rilevati'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 30 | `r"collection\(db, 'clienti', 'DNR', 'nuovi orari mancanti'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 37 | `r"window\.salvaNuovoCliente = async \(id, tenant = 'DNR'\) => \{",` | JS Function | cantiere |
| `fix_anomalie.py` | 44 | `r"doc\(db, 'clienti', 'DNR', 'codici articoli', newCode\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 49 | `r"doc\(db, 'clienti', 'DNR', 'nuovi articoli rilevati', originalId\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 56 | `r"collection\(db, 'clienti', 'DNR', 'raccolta clienti'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 61 | `r"doc\(db, 'clienti', 'DNR', 'raccolta clienti', docIdToUpdate\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 66 | `r"doc\(db, 'clienti', 'DNR', 'nuovi orari mancanti', idFromPdf\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 73 | `r"window\.eliminaAnomalia = async \(collectionName, id, tenant = 'DNR'\) => \{",` | JS Function | cantiere |
| `fix_anomalie.py` | 78 | `# 7. In the 'orari' fallback logic, ensure we don't save to DNR` | Logica / Config | cantiere |
| `fix_anomalie.py` | 80 | `r"tipologia_grado: \(window\.defaultAnomalyData && window\.defaultAnomalyData\[id\]\) \? window\.defaultAnomalyData\[id\` | Logica / Config | cantiere |
| `frontend/analizza_navette.html` | 43 | `const reportsRef = collection(db, 'clienti', 'DNR', 'reports_logistici');` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 25 | `activeTenant: localStorage.getItem('activeTenant') \|\| 'DNR' // Tenant di default` | Tenant Setup | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 339 | `// Listener per Clienti (Punti di Consegna DNR - Progetto Scuole)` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 340 | `const unsubCustomers = onSnapshot(collection(db, "clienti", "DNR", "raccolta clienti"), { includeMetadataChanges: true }` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 363 | `// Listener per Articoli DNR - Progetto Scuole` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 364 | `const unsubArticoli = onSnapshot(collection(db, "customers", "DNR", "anagrafica_articoli"), { includeMetadataChanges: tr` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 417 | `const unsub = onSnapshot(collection(db, "clienti/DNR/" + tipo), { includeMetadataChanges: true }, (snapshot) => {` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 457 | `collection(db, "clienti", "DNR", "resi_e_ritiri"),` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 507 | `await updateDoc(doc(db, "clienti", "DNR", "resi_e_ritiri", docId), { visto_da_ufficio: true });` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 592 | `// Funzione di salvataggio/creazione remoto per i clienti (Progetto Scuole DNR)` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 601 | `const docRef = doc(collection(db, "clienti", "DNR", "raccolta clienti"));` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 604 | `const docRef = doc(db, "clienti", "DNR", "raccolta clienti", id);` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 248 | `nomi = ["PROGETTO SCUOLE", "CATTEL", "GRAN CHEF", "BAUER"];` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 387 | `if (formattedDate && (clienteNome.toUpperCase() === 'GRAN CHEF' \|\| clienteNome.toUpperCase() === 'GRAND CHEF' \|\| cli` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 551 | `if (client === 'BAUER' \|\| client === 'GRAN CHEF' \|\| client === 'GRAND CHEF' \|\| client === 'PROGETTO SCUOLE') {` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 558 | `if (client === 'BAUER' \|\| client === 'GRAN CHEF' \|\| client === 'GRAND CHEF' \|\| client === 'PROGETTO SCUOLE') {` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 161 | `<small style="color:#64748b; margin-top:8px; display:block;">Inserisci il Codice Cliente (es. DNR) e l'indirizzo email a` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 229 | `const tenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 341 | `const tenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 352 | `const tenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 377 | `const tenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 433 | `const tenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 458 | `<input type="text" class="client-code-input" placeholder="Codice Cliente (es. DNR)" value="${code}" style="flex:1; paddi` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 509 | `const tenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main & cantiere |
| `frontend/check_names.html` | 26 | `const luoghiSnap = await getDocs(collection(db, "clienti/DNR/fatturazione_navette_carichi"));` | Variable Assignment | main & cantiere |
| `frontend/check_navette.html` | 35 | `const snapCarichi = await getDocs(collection(db, "clienti/DNR/navette_anagrafica_carichi"));` | Variable Assignment | main & cantiere |
| `frontend/check_navette.html` | 43 | `const snapClienti = await getDocs(collection(db, "clienti/DNR/navette_anagrafica_clienti"));` | Variable Assignment | main & cantiere |
| `frontend/core/firebase-init.js` | 41 | `activeTenant: localStorage.getItem('activeTenant') \|\| 'DNR' // Tenant di default` | Tenant Setup | main & cantiere |
| `frontend/elaborazione.html` | 90 | `/* Nuova Zona DAC */` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 276 | `<!-- Zona FRUTTA -->` | Logica / Config | main |
| `frontend/elaborazione.html` | 285 | `<!-- Zona LATTE -->` | Logica / Config | main |
| `frontend/elaborazione.html` | 290 | `<!-- Zona FRUTTA -->` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 299 | `<!-- Zona LATTE -->` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 303 | `<!-- Zona CATTEL -->` | Logica / Config | main |
| `frontend/elaborazione.html` | 317 | `<!-- Zona CATTEL -->` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 329 | `<!-- Zona DAC -->` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 332 | `<h3>Excel DAC</h3>` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 494 | `setupMultiFileSelect('file-chef', 'zone-chef', 'container-chef', filesChef, 'GRAND_CHEF');` | Logica / Config | main |
| `frontend/elaborazione.html` | 495 | `setupMultiFileSelect('file-cattel', 'zone-cattel', 'container-cattel', filesCattel, 'CATTEL');` | Logica / Config | main |
| `frontend/elaborazione.html` | 509 | `const q = query(collection(db, "progetti"), where("nome", "==", "CATTEL"));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 518 | `setupMultiFileSelect('file-chef', 'zone-chef', 'container-chef', filesChef, 'GRAND_CHEF');` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 519 | `setupMultiFileSelect('file-cattel', 'zone-cattel', 'container-cattel', filesCattel, 'CATTEL');` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 520 | `setupMultiFileSelect('file-dac', 'zone-dac', 'container-dac', filesDac, 'DAC');` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 522 | `title: 'Credenziali Portale CATTEL',` | Logica / Config | main |
| `frontend/elaborazione.html` | 534 | `const q = query(collection(db, "progetti"), where("nome", "==", "CATTEL"));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 540 | `💡 Per modificare queste credenziali, vai in <b>Impostazioni Sistema ➔ Gestione Clienti & Viaggi ➔ CATTEL</b>.` | Logica / Config | main |
| `frontend/elaborazione.html` | 547 | `title: 'Credenziali Portale CATTEL',` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 559 | `if (t === "GRAND_CHEF" \|\| t === "GRAND CHEF" \|\| t === "GRAN CHEF") {` | Logica / Config | main |
| `frontend/elaborazione.html` | 560 | `return ['clienti', 'GRAN CHEF'];` | Logica / Config | main |
| `frontend/elaborazione.html` | 562 | `if (t === "CATTEL") {` | Logica / Config | main |
| `frontend/elaborazione.html` | 563 | `return ['clienti', 'CATTEL'];` | Logica / Config | main |
| `frontend/elaborazione.html` | 565 | `💡 Per modificare queste credenziali, vai in <b>Impostazioni Sistema ➔ Gestione Clienti & Viaggi ➔ CATTEL</b>.` | Logica / Config | main & cantiere |
| `frontend/elaborazione.html` | 584 | `if (t === "GRAND_CHEF" \|\| t === "GRAND CHEF" \|\| t === "GRAN CHEF") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 585 | `return ['clienti', 'GRAN CHEF'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 587 | `if (t === "CATTEL") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 588 | `return ['clienti', 'CATTEL'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 590 | `if (t === "DAC") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 591 | `return ['clienti', 'DAC'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 593 | `return ['clienti', 'DNR'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 599 | `if (tnUpper === "FRUTTA") {` | Logica / Config | main |
| `frontend/elaborazione.html` | 600 | `competenzaVal = "DNR_FRUTTA";` | Logica / Config | main |
| `frontend/elaborazione.html` | 601 | `} else if (tnUpper === "LATTE") {` | Logica / Config | main |
| `frontend/elaborazione.html` | 602 | `competenzaVal = "DNR_LATTE";` | Logica / Config | main |
| `frontend/elaborazione.html` | 603 | `} else if (tnUpper === "GRAND_CHEF" \|\| tnUpper === "GRAND CHEF" \|\| tnUpper === "GRAN CHEF") {` | Logica / Config | main |
| `frontend/elaborazione.html` | 604 | `competenzaVal = "GRAN_CHEF";` | Logica / Config | main |
| `frontend/elaborazione.html` | 605 | `} else if (tnUpper === "CATTEL") {` | Logica / Config | main |
| `frontend/elaborazione.html` | 606 | `competenzaVal = "CATTEL";` | Logica / Config | main |
| `frontend/elaborazione.html` | 627 | `if (tnUpper === "FRUTTA") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 628 | `competenzaVal = "DNR_FRUTTA";` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 629 | `} else if (tnUpper === "LATTE") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 630 | `competenzaVal = "DNR_LATTE";` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 631 | `} else if (tnUpper === "GRAND_CHEF" \|\| tnUpper === "GRAND CHEF" \|\| tnUpper === "GRAN CHEF") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 632 | `competenzaVal = "GRAN_CHEF";` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 633 | `} else if (tnUpper === "CATTEL") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 634 | `competenzaVal = "CATTEL";` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 635 | `} else if (tnUpper === "DAC") {` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 636 | `competenzaVal = "DAC";` | Logica / Config | main & cantiere |
| `frontend/elaborazione.html` | 666 | `window.eliminaJob = async (jobId, storagePath, tenant = 'DNR', skipConfirm = false) => {` | JS Function | cantiere |
| `frontend/elaborazione.html` | 679 | `// Svuota DNR` | Logica / Config | main |
| `frontend/elaborazione.html` | 680 | `const snapDNR = await window.getDocsConFallback(collection(db, 'clienti', 'DNR', 'processing_jobs'));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 682 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'DNR', true));` | Logica / Config | main |
| `frontend/elaborazione.html` | 685 | `// Svuota GRAN CHEF` | Logica / Config | main |
| `frontend/elaborazione.html` | 686 | `const snapGC = await window.getDocsConFallback(collection(db, 'clienti', 'GRAN CHEF', 'processing_jobs'));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 688 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'GRAN CHEF', true));` | Logica / Config | main |
| `frontend/elaborazione.html` | 691 | `// Svuota CATTEL` | Logica / Config | main |
| `frontend/elaborazione.html` | 692 | `const snapCattel = await window.getDocsConFallback(collection(db, 'clienti', 'CATTEL', 'processing_jobs'));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 694 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'CATTEL', true));` | Logica / Config | main |
| `frontend/elaborazione.html` | 709 | `// Svuota DNR` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 710 | `const snapDNR = await window.getDocsConFallback(collection(db, 'clienti', 'DNR', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 712 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'DNR', true));` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 715 | `// Svuota GRAN CHEF` | Logica / Config | main & cantiere |
| `frontend/elaborazione.html` | 716 | `const snapGC = await window.getDocsConFallback(collection(db, 'clienti', 'GRAN CHEF', 'processing_jobs'));` | Variable Assignment | main & cantiere |
| `frontend/elaborazione.html` | 717 | `activeJobsCattel.forEach(j => merged.push({ ...j, tenant: 'CATTEL' }));` | JS Function | main |
| `frontend/elaborazione.html` | 718 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'GRAN CHEF', true));` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 721 | `// Svuota CATTEL` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 722 | `const snapCattel = await window.getDocsConFallback(collection(db, 'clienti', 'CATTEL', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 724 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'CATTEL', true));` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 727 | `// Svuota DAC` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 728 | `const snapDac = await window.getDocsConFallback(collection(db, 'clienti', 'DAC', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 730 | `promises.push(window.eliminaJob(doc.id, doc.data().storage_path, 'DAC', true));` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 749 | `combinedMsg += `<div style='color:#0f172a; font-size:15px; font-weight:800; text-transform:uppercase; margin-bottom:10px` | Tenant Setup | main |
| `frontend/elaborazione.html` | 753 | `activeJobsDNR.forEach(j => merged.push({ ...j, tenant: 'DNR' }));` | JS Function | cantiere |
| `frontend/elaborazione.html` | 754 | `activeJobsGC.forEach(j => merged.push({ ...j, tenant: 'GRAN CHEF' }));` | JS Function | cantiere |
| `frontend/elaborazione.html` | 755 | `activeJobsCattel.forEach(j => merged.push({ ...j, tenant: 'CATTEL' }));` | JS Function | cantiere |
| `frontend/elaborazione.html` | 756 | `activeJobsDac.forEach(j => merged.push({ ...j, tenant: 'DAC' }));` | JS Function | cantiere |
| `frontend/elaborazione.html` | 783 | `<span style="font-size: 10px; background: ${data.tenant === 'GRAN CHEF' ? '#fef3c7' : (data.tenant === 'CATTEL' ? '#e0f2` | Tenant Setup | main |
| `frontend/elaborazione.html` | 788 | `combinedMsg += `<div style='color:#0f172a; font-size:15px; font-weight:800; text-transform:uppercase; margin-bottom:10px` | Tenant Setup | cantiere |
| `frontend/elaborazione.html` | 798 | `<button onclick="window.eliminaJob('${data.id}', '${data.storage_path}', '${data.tenant \|\| 'DNR'}')" style="background` | Tenant Setup | main |
| `frontend/elaborazione.html` | 822 | `<span style="font-size: 10px; background: ${data.tenant === 'GRAN CHEF' ? '#fef3c7' : (data.tenant === 'CATTEL' ? '#e0f2` | Tenant Setup | cantiere |
| `frontend/elaborazione.html` | 834 | `// Sottoscrizione DNR` | Logica / Config | main |
| `frontend/elaborazione.html` | 835 | `subscribeToProcessingJobs('DNR', 10, (snapshot) => {` | JS Function | main |
| `frontend/elaborazione.html` | 837 | `<button onclick="window.eliminaJob('${data.id}', '${data.storage_path}', '${data.tenant \|\| 'DNR'}')" style="background` | Tenant Setup | cantiere |
| `frontend/elaborazione.html` | 843 | `subscribeToProcessingJobs('GRAN CHEF', 10, (snapshot) => {` | JS Function | main |
| `frontend/elaborazione.html` | 850 | `// Sottoscrizione CATTEL` | Logica / Config | main |
| `frontend/elaborazione.html` | 851 | `subscribeToProcessingJobs('CATTEL', 10, (snapshot) => {` | JS Function | main |
| `frontend/elaborazione.html` | 873 | `// Sottoscrizione DNR` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 874 | `subscribeToProcessingJobs('DNR', 10, (snapshot) => {` | JS Function | cantiere |
| `frontend/elaborazione.html` | 882 | `subscribeToProcessingJobs('GRAN CHEF', 10, (snapshot) => {` | JS Function | cantiere |
| `frontend/elaborazione.html` | 889 | `// Sottoscrizione CATTEL` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 890 | `subscribeToProcessingJobs('CATTEL', 10, (snapshot) => {` | JS Function | cantiere |
| `frontend/elaborazione.html` | 897 | `// Sottoscrizione DAC` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 898 | `subscribeToProcessingJobs('DAC', 10, (snapshot) => {` | JS Function | cantiere |
| `frontend/elaborazione.html` | 1075 | `const activeTenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | main |
| `frontend/elaborazione.html` | 1122 | `const activeTenant = localStorage.getItem('activeTenant') \|\| 'DNR';` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 1230 | `tipologie_caricate.push('FRUTTA');` | Logica / Config | main |

*(Mostrati primi 300 risultati su 1647 reali per questa categoria)*

## 4. Collection Firestore
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `ARCHITECTURE.md` | 87 | `I committenti (**DNR, CATTEL, GRAN CHEF, BAUER, HOTEL**, ecc.) sono i clienti commerciali di Loge Solution. I committent` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 89 | `* Forniscono le anagrafiche dei propri clienti finali e i punti di destinazione;` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 106 | `4. **Divieto Fallback Automatico**: Se un dato arriva senza `tenantId`, deve essere bloccato o posto in quarantena (`pro` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 119 | `\| **Anagrafica Punti DNR** \| DNR \| Tenant-Specifico \| `clienti/DNR/raccolta clienti`. Codici cliente e note DNR. \|` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 120 | `\| **Anagrafica Punti Cattel**\| CATTEL \| Tenant-Specifico \| `clienti/CATTEL/raccolta clienti`. Codici cliente Cattel.` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 121 | `\| **Anagrafica GranChef** \| GRAN CHEF \| Tenant-Specifico \| `clienti/GRAN CHEF/raccolta clienti`. Codici GranChef. \|` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 249 | ``[DEBITO TECNICO]`: Attualmente, se Cattel e GranChef servono lo stesso ristorante allo stesso indirizzo, esistono due d` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 277 | `* `[DEBITO TECNICO]`: Attualmente i viaggi sono memorizzati in Firestore sotto `clienti/{tenant}/viaggi ddt`. Questo imp` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 331 | `└── clienti/                   [Sottocollezioni Tenant-Specifiche]` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 333 | `│   ├── raccolta clienti` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 334 | `│   ├── viaggi ddt` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 338 | `│   ├── raccolta clienti` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 339 | `│   └── viaggi ddt` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 341 | `├── raccolta clienti` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 342 | `└── viaggi ddt` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 410 | `3. **Quarantena Anomalie**: Spostare i record ambigui in `processing_jobs_quarantine` richiedendo l'intervento umano;` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 31 | `Non abbiamo visibilità diretta sulla singola collection "deliveries" in quanto i dati risiedono aggregati nei file `spli` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 66 | `- La discrepanza si rileva primariamente durante la conversione da Parser/Split JSON a `viaggi ddt`. Sviluppo raggruppa ` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 87 | `L'ambiente di Cantiere evidenzia conteggi inferiori sia nei viaggi che nei punti aggregati totali. Questo significa che ` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 11 | `2. Come **Percorso di Salvataggio Forzato**: Molte schermate di impostazioni o pianificazione salvano o leggono dati pun` | Logica / Config | main & cantiere |
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 25 | `- [ ] `gestione.html` (isolare codici articoli, rientri, anagrafiche)` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 37 | `│    - Anagrafica clienti commerciali dei committenti                              │` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 75 | `3. **Isolamento Anagrafico**: Ciascun committente possiede il proprio sotto-albero anagrafico in Firestore (`clienti/{te` | Tenant Setup | main & cantiere |
| `DOMAIN_MODEL.md` | 111 | `3. **Divieto Fallback DNR**: Se un dato arriva senza `tenantId`, non deve mai essere assegnato automaticamente a DNR, ma` | Tenant Setup | main & cantiere |
| `PROJECT_MANIFEST.md` | 28 | `* [M-018 — Clienti](#m-018--clienti) `[DA COMPILARE]`` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 219 | `* L'entità *Punto di Consegna* assume una dignità geografica distinta rispetto alle anagrafiche dei clienti commerciali,` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 483 | `* **Scopo del Capitolo**: Definire l’identità aziendale dei clienti di Loge Solution (DNR, Cattel, GranChef, Bauer), la ` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 31 | `PARTIAL_SOURCE_PARAM:"javax.faces.source",BEHAVIOR_EVENT_PARAM:"javax.faces.behavior.event",PARTIAL_EVENT_PARAM:"javax.f` | Logica / Config | main & cantiere |
| `ROADMAP_OTTIMIZZAZIONE_FRONTEND.md` | 58 | `*   `mappa.html` -> solo coordinate clienti.` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 23 | `viaggi = db.collection('clienti').document('CATTEL').collection('viaggi ddt').where('data_lavoro', '==', '25-07-2026').s` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 27 | `doc = db.collection('clienti').document('CATTEL').collection('viaggi ddt').document(trip_id).get()` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 32 | `jobs = db.collection('clienti').document('CATTEL').collection('processing_jobs').where('dataViaggi', '==', '25-07-2026')` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 35 | `doc = db.collection('clienti').document('CATTEL').collection('processing_jobs').document('jgsbJytUKVtXWx0nKwRd').get()` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 40 | `locks = db.collection('clienti').document('CATTEL').collection('trip_title_locks').stream()` | Logica / Config | main & cantiere |
| `audit_script.py` | 38 | `tenant_ref = db.collection('clienti').document(t)` | Tenant Setup | main & cantiere |
| `audit_script.py` | 41 | `jobs_query = tenant_ref.collection('processing_jobs').order_by('createdAt', direction=firestore.Query.DESCENDING).limit(` | Tenant Setup | main & cantiere |
| `audit_script.py` | 53 | `jobs_query = tenant_ref.collection('processing_jobs').limit(100).stream()` | Tenant Setup | main & cantiere |
| `build_inventory.py` | 14 | `'processing_jobs': [],` | Logica / Config | main & cantiere |
| `build_inventory.py` | 23 | `viaggio_ref = db.collection('clienti').document('CATTEL').collection('viaggi ddt').document(trip_id)` | Logica / Config | main & cantiere |
| `build_inventory.py` | 29 | `jobs = db.collection('clienti').document('CATTEL').collection('processing_jobs').stream()` | Logica / Config | main & cantiere |
| `build_inventory.py` | 33 | `inventory['processing_jobs'].append({'path': j.reference.path, 'data': d})` | Logica / Config | main & cantiere |
| `build_inventory.py` | 36 | `locks = db.collection('clienti').document('CATTEL').collection('trip_title_locks').stream()` | Logica / Config | main & cantiere |
| `build_inventory.py` | 62 | `if coll.id not in ['viaggi', 'processing_jobs', 'trip_title_locks', 'mappe_viaggi']:` | Logica / Config | main & cantiere |
| `check_cantiere.py` | 24 | `jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\` | Logica / Config | cantiere |
| `check_cantiere_offline.py` | 15 | `jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\` | Logica / Config | cantiere |
| `check_cantiere_offline2.py` | 15 | `jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\` | Logica / Config | cantiere |
| `check_deliveries.py` | 5 | `doc = db.collection("clienti").document("DAC").collection("reports_logistici").document("01-08-2026").get()` | Logica / Config | cantiere |
| `check_fields.py` | 7 | `doc = next(db.collection('clienti').document('DNR').collection('viaggi ddt').limit(1).stream())` | Logica / Config | main & cantiere |
| `check_fields2.py` | 7 | `viaggi = db.collection('clienti').document('DNR').collection('viaggi ddt').stream()` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 37 | `"clienti/CATTEL/viaggi ddt/25-07-2026_CATTEL_0000_01_bda95be14aaa",` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 38 | `"clienti/CATTEL/trip_title_locks/65c48b90050d571b38947b8f",` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 39 | `"clienti/CATTEL/processing_jobs/jgsbJytUKVtXWx0nKwRd"` | Logica / Config | main & cantiere |
| `cleanup_apps.py` | 10 | `"gestione_nuovi_clienti.html",` | Logica / Config | main & cantiere |
| `cleanup_duplicates.py` | 10 | `"gestione_nuovi_clienti.html",` | Logica / Config | main & cantiere |
| `core_genera_completo_giornata.py` | 34 | `for doc in db.collection('clienti').document('DNR').collection('rientri ddt').stream():` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 122 | `doc_ref = get_db().collection('clienti').document('DNR').collection('viaggi ddt').document(viaggio_id)` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 202 | `db.collection('clienti').document(tenant).collection('reports_logistici').document(data_consegna).set(report_meta)` | Tenant Setup | cantiere |
| `core_genera_completo_giornata.py` | 205 | `viaggi_ref = db.collection('clienti').document(tenant).collection('viaggi ddt')` | Tenant Setup | cantiere |
| `count_gc.py` | 7 | `clienti = db.collection('clienti').stream()` | Logica / Config | main & cantiere |
| `count_gc.py` | 9 | `for cliente in clienti:` | Logica / Config | main & cantiere |
| `count_gc.py` | 10 | `viaggi = db.collection('clienti').document(cliente.id).collection('viaggi ddt').stream()` | Logica / Config | main & cantiere |
| `create_user.js` | 13 | `const dipendenteRef = db.collection('clienti').doc('DNR').collection('dipendenti').doc(uid);` | Variable Assignment | cantiere |
| `deep_audit_25_07.py` | 99 | `if 'processing_jobs' in coll_name: category = 'PROCESSING_JOB'` | Logica / Config | main & cantiere |
| `deep_audit_25_07.py` | 120 | `tenant = doc_data.get('tenant', path.split('/')[1] if path.startswith('clienti/') and len(path.split('/')) > 2 else 'N/A` | Tenant Setup | main & cantiere |
| `extract_more.py` | 25 | `tenant_ref = db.collection('clienti').document(t)` | Tenant Setup | main & cantiere |
| `extract_viaggi.py` | 25 | `tenant_ref = db.collection('clienti').document(t)` | Tenant Setup | main & cantiere |
| `extract_viaggi.py` | 29 | `jobs_query = tenant_ref.collection('processing_jobs').stream()` | Tenant Setup | main & cantiere |
| `extract_viaggi.py` | 42 | `viaggi = tenant_ref.collection('viaggi ddt').stream()` | Tenant Setup | main & cantiere |
| `extract_viaggi.py` | 51 | `print(f"Error reading viaggi ddt for {t}: {e}")` | Logica / Config | main & cantiere |
| `fast_audit.py` | 12 | `collections_to_check = ['clienti', 'processing_jobs', 'viaggi', 'mappe', 'title_locks', 'pianificazioni', 'storico_lavor` | Logica / Config | main & cantiere |
| `find_dev_data.py` | 13 | `jobs = db.collection('processing_jobs').where('tenant', '==', 'CATTEL').where('dataViaggi', '==', '25-07-2026').stream()` | Tenant Setup | main & cantiere |
| `firestore.rules` | 78 | `match /clienti_fatturazione/{docId} {` | Logica / Config | main & cantiere |
| `firestore.rules` | 95 | `match /clienti/{tenant}/{collection=**} {` | Tenant Setup | main & cantiere |
| `firestore.rules.backup` | 58 | `match /clienti/{tenant}/{collection=**} {` | Tenant Setup | main & cantiere |
| `fix_anomalie.py` | 18 | `r"collection\(db, 'clienti', 'DNR', 'nuovi codici consegna'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 19 | `r"collection(db, 'clienti', activeTenant, 'nuovi codici consegna')",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 24 | `r"collection\(db, 'clienti', 'DNR', 'nuovi articoli rilevati'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 25 | `r"collection(db, 'clienti', activeTenant, 'nuovi articoli rilevati')",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 30 | `r"collection\(db, 'clienti', 'DNR', 'nuovi orari mancanti'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 31 | `r"collection(db, 'clienti', activeTenant, 'nuovi orari mancanti')",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 44 | `r"doc\(db, 'clienti', 'DNR', 'codici articoli', newCode\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 45 | `r"doc(db, 'clienti', activeTenant, 'codici articoli', newCode)",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 49 | `r"doc\(db, 'clienti', 'DNR', 'nuovi articoli rilevati', originalId\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 50 | `r"doc(db, 'clienti', activeTenant, 'nuovi articoli rilevati', originalId)",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 54 | `# 5. Fix doc(...) for raccolta clienti updates in orari` | Logica / Config | cantiere |
| `fix_anomalie.py` | 56 | `r"collection\(db, 'clienti', 'DNR', 'raccolta clienti'\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 57 | `r"collection(db, 'clienti', activeTenant, 'raccolta clienti')",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 61 | `r"doc\(db, 'clienti', 'DNR', 'raccolta clienti', docIdToUpdate\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 62 | `r"doc(db, 'clienti', activeTenant, 'raccolta clienti', docIdToUpdate)",` | Tenant Setup | cantiere |
| `fix_anomalie.py` | 66 | `r"doc\(db, 'clienti', 'DNR', 'nuovi orari mancanti', idFromPdf\)",` | Logica / Config | cantiere |
| `fix_anomalie.py` | 67 | `r"doc(db, 'clienti', activeTenant, 'nuovi orari mancanti', idFromPdf)",` | Tenant Setup | cantiere |
| `fix_app_import.py` | 10 | `"gestione_nuovi_clienti.html",` | Logica / Config | main & cantiere |
| `fix_db_import.py` | 17 | `"gestione_nuovi_clienti.html",` | Logica / Config | main & cantiere |
| `frontend/analizza_navette.html` | 43 | `const reportsRef = collection(db, 'clienti', 'DNR', 'reports_logistici');` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 21 | `lista_clienti: [],` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 86 | `const isAdminOnlyPage = ['clienti.html', 'impostazioni.html', 'visualizzazione.html', 'mappa_consegne.html', 'dashboard.` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 340 | `const unsubCustomers = onSnapshot(collection(db, "clienti", "DNR", "raccolta clienti"), { includeMetadataChanges: true }` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 341 | `const clienti = [];` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 344 | `clienti.push({` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 357 | `window.appData.lista_clienti = clienti; // Popola correttamente clienti.html` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 402 | `// Listener per Progetti (clienti con viaggi associati)` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 417 | `const unsub = onSnapshot(collection(db, "clienti/DNR/" + tipo), { includeMetadataChanges: true }, (snapshot) => {` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 430 | `setupScalettaListener('scaletta_clienti', 'lista_scaletta_clienti');` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 436 | `setupScalettaListener('navetta_clienti', 'lista_navetta_clienti');` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 457 | `collection(db, "clienti", "DNR", "resi_e_ritiri"),` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 507 | `await updateDoc(doc(db, "clienti", "DNR", "resi_e_ritiri", docId), { visto_da_ufficio: true });` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 592 | `// Funzione di salvataggio/creazione remoto per i clienti (Progetto Scuole DNR)` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 601 | `const docRef = doc(collection(db, "clienti", "DNR", "raccolta clienti"));` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/firebase-auth-sync.js` | 604 | `const docRef = doc(db, "clienti", "DNR", "raccolta clienti", id);` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 51 | `lista_clienti: [],` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 230 | `const resiRef = collection(db, "clienti", tenant, "resi_e_ritiri");` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 342 | `const docRef = doc(db, "clienti", tenant, "resi_e_ritiri", id);` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 353 | `const docRef = doc(db, "clienti", tenant, "resi_e_ritiri", id);` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 391 | `await deleteDoc(doc(db, "clienti", tenant, "resi_e_ritiri", id));` | Tenant Setup | main & cantiere |
| `frontend/centrale_resi.html` | 429 | `clienti: {}` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 434 | `const docRef = doc(db, "clienti", tenant, "configurazioni", "email_settings");` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 446 | `const clients = emailSettings.clienti \|\| {};` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 492 | `let clientiJson = {};` | Variable Assignment | main & cantiere |
| `frontend/centrale_resi.html` | 498 | `clientiJson[code] = email;` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 505 | `emailSettings.clienti = clientiJson;` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 510 | `await setDoc(doc(db, "clienti", tenant, "configurazioni", "email_settings"), emailSettings);` | Tenant Setup | main & cantiere |
| `frontend/centrale_resi.html` | 527 | `// Pre-compila le email destinatari se troviamo i clienti` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 529 | `const emails = clientCodes.map(code => emailSettings.clienti[code]).filter(Boolean);` | JS Function | main & cantiere |
| `frontend/check_names.html` | 26 | `const luoghiSnap = await getDocs(collection(db, "clienti/DNR/fatturazione_navette_carichi"));` | Variable Assignment | main & cantiere |
| `frontend/check_names.html` | 30 | `const clientiSnap = await getDocs(collection(db, "clienti_fatturazione"));` | Variable Assignment | main & cantiere |
| `frontend/check_names.html` | 31 | `const clienti = new Set();` | Variable Assignment | main & cantiere |
| `frontend/check_names.html` | 32 | `clientiSnap.forEach(d => { if(d.data().nome) clienti.add(d.data().nome.trim().toUpperCase()); });` | JS Function | main & cantiere |
| `frontend/check_names.html` | 38 | `text += "\n--- CLIENTI FATTURAZIONE (clienti_fatturazione) ---\n";` | Logica / Config | main & cantiere |
| `frontend/check_names.html` | 39 | `text += `Totale elementi: ${clienti.size}\n`;` | Logica / Config | main & cantiere |
| `frontend/check_names.html` | 40 | `Array.from(clienti).sort().forEach(n => text += `- ${n}\n`);` | JS Function | main & cantiere |
| `frontend/check_names.html` | 42 | `const soloLuoghi = Array.from(luoghi).filter(x => !clienti.has(x)).sort();` | JS Function | main & cantiere |
| `frontend/check_names.html` | 43 | `const soloClienti = Array.from(clienti).filter(x => !luoghi.has(x)).sort();` | JS Function | main & cantiere |
| `frontend/check_names.html` | 44 | `const inEntrambi = Array.from(luoghi).filter(x => clienti.has(x)).sort();` | JS Function | main & cantiere |
| `frontend/check_navette.html` | 35 | `const snapCarichi = await getDocs(collection(db, "clienti/DNR/navette_anagrafica_carichi"));` | Variable Assignment | main & cantiere |
| `frontend/check_navette.html` | 43 | `const snapClienti = await getDocs(collection(db, "clienti/DNR/navette_anagrafica_clienti"));` | Variable Assignment | main & cantiere |
| `frontend/core/firebase-init.js` | 37 | `lista_clienti: [],` | Logica / Config | main & cantiere |
| `frontend/dashboard.html` | 80 | `<p>Assegna in anticipo furgoni e clienti agli autisti tramite il nuovo filtro intelligente.</p>` | Logica / Config | main & cantiere |
| `frontend/dashboard.html` | 139 | `<a href="javascript:void(0)" onclick="window.navigateWithState('fatturazione_clienti.html')" class="nav-card theme-amber` | Logica / Config | main & cantiere |
| `frontend/elaborazione.html` | 259 | `<button class="glass-btn" onclick="window.navigateWithState('gestione_anomalie.html')" style="flex: 1; justify-content: ` | Logica / Config | main |
| `frontend/elaborazione.html` | 273 | `<button class="glass-btn" onclick="window.navigateWithState('gestione_anomalie.html')" style="flex: 1; justify-content: ` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 560 | `return ['clienti', 'GRAN CHEF'];` | Logica / Config | main |
| `frontend/elaborazione.html` | 563 | `return ['clienti', 'CATTEL'];` | Logica / Config | main |
| `frontend/elaborazione.html` | 565 | `return ['clienti', 'DNR'];` | Logica / Config | main |
| `frontend/elaborazione.html` | 585 | `return ['clienti', 'GRAN CHEF'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 588 | `return ['clienti', 'CATTEL'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 591 | `return ['clienti', 'DAC'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 593 | `return ['clienti', 'DNR'];` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 595 | `const jobsRef = collection(db, ...tenantPath, 'processing_jobs');` | Variable Assignment | main |
| `frontend/elaborazione.html` | 623 | `const jobsRef = collection(db, ...tenantPath, 'processing_jobs');` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 661 | `await deleteDoc(doc(db, 'clienti', tenant, 'processing_jobs', jobId));` | Tenant Setup | main |
| `frontend/elaborazione.html` | 680 | `const snapDNR = await window.getDocsConFallback(collection(db, 'clienti', 'DNR', 'processing_jobs'));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 686 | `const snapGC = await window.getDocsConFallback(collection(db, 'clienti', 'GRAN CHEF', 'processing_jobs'));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 691 | `await deleteDoc(doc(db, 'clienti', tenant, 'processing_jobs', jobId));` | Tenant Setup | cantiere |
| `frontend/elaborazione.html` | 692 | `const snapCattel = await window.getDocsConFallback(collection(db, 'clienti', 'CATTEL', 'processing_jobs'));` | Variable Assignment | main |
| `frontend/elaborazione.html` | 710 | `const snapDNR = await window.getDocsConFallback(collection(db, 'clienti', 'DNR', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 716 | `const snapGC = await window.getDocsConFallback(collection(db, 'clienti', 'GRAN CHEF', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 722 | `const snapCattel = await window.getDocsConFallback(collection(db, 'clienti', 'CATTEL', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 728 | `const snapDac = await window.getDocsConFallback(collection(db, 'clienti', 'DAC', 'processing_jobs'));` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 742 | `let n_c = data.nuovi_clienti \|\| 0;` | Variable Assignment | main |
| `frontend/elaborazione.html` | 752 | `let listC = data.nuovi_clienti_list ? data.nuovi_clienti_list.join(', ') : '';` | Variable Assignment | main |
| `frontend/elaborazione.html` | 781 | `let n_c = data.nuovi_clienti \|\| 0;` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 789 | `${data.nuovi_clienti ? `<span style="background:#fee2e2; color:#ef4444; padding:2px 6px; border-radius:4px; font-weight:` | Logica / Config | main |
| `frontend/elaborazione.html` | 791 | `let listC = data.nuovi_clienti_list ? data.nuovi_clienti_list.join(', ') : '';` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 828 | `${data.nuovi_clienti ? `<span style="background:#fee2e2; color:#ef4444; padding:2px 6px; border-radius:4px; font-weight:` | Logica / Config | cantiere |
| `frontend/fatturazione.html` | 361 | `// Popolamento dinamico clienti da Firestore` | Logica / Config | main & cantiere |
| `frontend/fatturazione.html` | 382 | `} catch(e) { console.error("Errore popolamento clienti:", e); }` | Logica / Config | main & cantiere |
| `frontend/fatturazione.html` | 483 | `const viaggiRef = collection(db, 'clienti', activeTenant, 'viaggi ddt');` | Variable Assignment | main & cantiere |
| `frontend/fatturazione.html` | 711 | `const viaggiRef = collection(db, 'clienti', activeTenant, 'viaggi ddt');` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_clienti.html` | 158 | `📦 Liste per le <strong>Sedi Magazzino</strong>: utilizzate dai magazzinieri. I magazzini inseriti qui non verranno inclu` | Logica / Config | main & cantiere |
| `frontend/fatturazione_clienti.html` | 177 | `🚐 Liste per la <strong>Navetta</strong> e <strong>Navetta Autisti</strong>: configura qui i punti e i clienti abilitando` | Logica / Config | main & cantiere |
| `frontend/fatturazione_clienti.html` | 223 | `<button type="button" class="btn-primary" style="padding: 8px; font-size: 13px; border-radius: 6px; width: 100%; justify` | Logica / Config | main & cantiere |
| `frontend/fatturazione_clienti.html` | 244 | `<!-- Lista dei clienti esistenti popolata via JS -->` | Logica / Config | main & cantiere |
| `frontend/fatturazione_clienti.html` | 524 | `await updateDoc(doc(db, "clienti_fatturazione", editingClientId), data);` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 526 | `await addDoc(collection(db, "clienti_fatturazione"), data);` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 539 | `onSnapshot(collection(db, "clienti_fatturazione"), (snap) => {` | JS Function | main |
| `frontend/fatturazione_clienti.html` | 543 | `window.appData.lista_clienti_fatturazione = [];` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 553 | `window.appData.lista_clienti_fatturazione.push({ id: cid, nome: c.nome });` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 629 | `const d = await getDoc(doc(db, "clienti_fatturazione", id));` | Variable Assignment | main |
| `frontend/fatturazione_clienti.html` | 632 | `await updateDoc(doc(db, "clienti_fatturazione", editingClientId), data);` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 634 | `await addDoc(collection(db, "clienti_fatturazione"), data);` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 647 | `onSnapshot(collection(db, "clienti_fatturazione"), (snap) => {` | JS Function | cantiere |
| `frontend/fatturazione_clienti.html` | 651 | `window.appData.lista_clienti_fatturazione = [];` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 660 | `await deleteDoc(doc(db, "clienti_fatturazione", id));` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 661 | `window.appData.lista_clienti_fatturazione.push({ id: cid, nome: c.nome });` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 667 | `await updateDoc(doc(db, "clienti_fatturazione", id), {` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 696 | `<button type="button" style="background: none; border: none; color: #ef4444; padding: 4px; cursor: pointer; display: fle` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 711 | `await addDoc(collection(db, "clienti/DNR/" + collectionPath), { nome: nome });` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 733 | `} else if (tipo === 'clienti') {` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 734 | `items = window.appData?.anagrafica_clienti \|\| [];` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 736 | `collectionPath = 'fatturazione_navette_clienti';` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 737 | `const d = await getDoc(doc(db, "clienti_fatturazione", id));` | Variable Assignment | cantiere |
| `frontend/fatturazione_clienti.html` | 759 | `if (tipo === 'clienti' \|\| tipo === 'carichi') {` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 760 | `const clientiPrincipali = window.appData?.lista_clienti_fatturazione \|\| [];` | Variable Assignment | main |
| `frontend/fatturazione_clienti.html` | 764 | `clientiPrincipali.sort((a,b)=>(a.nome\|\|'').localeCompare(b.nome\|\|'')).forEach(cp => {` | JS Function | main |
| `frontend/fatturazione_clienti.html` | 770 | `await deleteDoc(doc(db, "clienti_fatturazione", id));` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 777 | `await updateDoc(doc(db, "clienti_fatturazione", id), {` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 803 | `<button type="button" style="background: none; border: none; color: #ef4444; padding: 2px; cursor: pointer; display: fle` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 806 | `<button type="button" style="background: none; border: none; color: #ef4444; padding: 4px; cursor: pointer; display: fle` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 821 | `await addDoc(collection(db, "clienti/DNR/" + collectionPath), { nome: nome });` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 843 | `} else if (tipo === 'clienti') {` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 844 | `items = window.appData?.anagrafica_clienti \|\| [];` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 846 | `collectionPath = 'fatturazione_navette_clienti';` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 855 | `await updateDoc(doc(db, "clienti/DNR/" + collectionPath, id), dataToUpdate);` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 869 | `if (tipo === 'clienti' \|\| tipo === 'carichi') {` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 870 | `const clientiPrincipali = window.appData?.lista_clienti_fatturazione \|\| [];` | Variable Assignment | cantiere |
| `frontend/fatturazione_clienti.html` | 874 | `clientiPrincipali.sort((a,b)=>(a.nome\|\|'').localeCompare(b.nome\|\|'')).forEach(cp => {` | JS Function | cantiere |
| `frontend/fatturazione_clienti.html` | 894 | `await addDoc(collection(db, "clienti/DNR/" + collectionPath), payload);` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 910 | `await updateDoc(doc(db, "clienti/DNR/" + collectionPath, id), {` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 913 | `<button type="button" style="background: none; border: none; color: #ef4444; padding: 2px; cursor: pointer; display: fle` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 931 | `['partenze', 'carichi', 'clienti', 'destinazioni'].forEach(t => window.renderUnifiedNavetteList(t));` | JS Function | main |
| `frontend/fatturazione_clienti.html` | 965 | `await updateDoc(doc(db, "clienti/DNR/" + collectionPath, id), dataToUpdate);` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 1004 | `await addDoc(collection(db, "clienti/DNR/" + collectionPath), payload);` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 1020 | `await updateDoc(doc(db, "clienti/DNR/" + collectionPath, id), {` | Logica / Config | cantiere |
| `frontend/fatturazione_clienti.html` | 1041 | `['partenze', 'carichi', 'clienti', 'destinazioni'].forEach(t => window.renderUnifiedNavetteList(t));` | JS Function | cantiere |
| `frontend/fatturazione_v2.html` | 66 | `<option value="">Caricamento clienti...</option>` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 164 | `const snap = await getDocs(collection(db, "clienti/DNR/fatturazione_navette_carichi"));` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 204 | `const snap = await getDocs(collection(db, "clienti_fatturazione"));` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 211 | `const snapClienti = await getDocs(collection(db, "clienti/DNR/fatturazione_navette_clienti"));` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 213 | `const snapCarichi = await getDocs(collection(db, "clienti/DNR/fatturazione_navette_carichi"));` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 251 | `console.error("Errore caricamento clienti:", e);` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 285 | `const progSnap = await getDocs(collection(db, "clienti_fatturazione"));` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 435 | `// Fetch viaggi ddt: filtriamo in memoria come nel vecchio sistema per max compatibilità` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 436 | `const viaggiRef = collection(db, 'clienti', activeTenant, 'viaggi ddt');` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 446 | `// Nei viaggi ddt, il cliente corrisponde al tenant in cui ci troviamo (activeTenant)` | Tenant Setup | main & cantiere |
| `frontend/fatturazione_v2.html` | 455 | `const q = query(collection(db, 'clienti', activeTenant, 'kpi_isolati'),` | Variable Assignment | main & cantiere |
| `frontend/fatturazione_v2.html` | 942 | `const kpiRef = collection(db, 'clienti', activeTenant, 'kpi_isolati');` | Variable Assignment | main & cantiere |
| `frontend/gestione.html` | 295 | `<button class="tab-btn active" onclick="switchTab('clienti')">` | Logica / Config | main & cantiere |
| `frontend/gestione.html` | 376 | `let currentTab = 'clienti';` | Variable Assignment | main |
| `frontend/gestione.html` | 377 | `let currentTab = 'clienti';` | Variable Assignment | cantiere |
| `frontend/gestione.html` | 397 | `btnMap.style.display = (tab === 'clienti') ? 'flex' : 'none';` | Logica / Config | main |
| `frontend/gestione.html` | 398 | `btnMap.style.display = (tab === 'clienti') ? 'flex' : 'none';` | Logica / Config | cantiere |
| `frontend/gestione.html` | 401 | `brandSelect.style.display = (tab === 'clienti') ? 'inline-block' : 'none';` | Logica / Config | main |
| `frontend/gestione.html` | 402 | `brandSelect.style.display = (tab === 'clienti') ? 'inline-block' : 'none';` | Logica / Config | cantiere |
| `frontend/gestione.html` | 405 | `rubricaAlert.style.display = (tab === 'clienti') ? 'flex' : 'none';` | Logica / Config | main |
| `frontend/gestione.html` | 406 | `rubricaAlert.style.display = (tab === 'clienti') ? 'flex' : 'none';` | Logica / Config | cantiere |
| `frontend/gestione.html` | 416 | `if(currentTab === 'clienti') {` | Logica / Config | main |
| `frontend/gestione.html` | 417 | `if(currentTab === 'clienti') {` | Logica / Config | cantiere |
| `frontend/gestione.html` | 423 | `getDocsFromCache(query(collection(db, 'clienti/DNR/raccolta clienti'))).then(snapshot => {` | JS Function | main |
| `frontend/gestione.html` | 425 | `getDocsFromCache(query(collection(db, 'clienti/DNR/raccolta clienti'))).then(snapshot => {` | JS Function | cantiere |
| `frontend/gestione.html` | 435 | `getDocsFromCache(query(collection(db, 'clienti/GRAN CHEF/raccolta clienti'))).then(snapshot => {` | JS Function | main |
| `frontend/gestione.html` | 437 | `getDocsFromCache(query(collection(db, 'clienti/GRAN CHEF/raccolta clienti'))).then(snapshot => {` | JS Function | cantiere |
| `frontend/gestione.html` | 444 | `getDocsFromCache(query(collection(db, 'clienti/CATTEL/raccolta clienti'))).then(snapshot => {` | JS Function | main |
| `frontend/gestione.html` | 446 | `getDocsFromCache(query(collection(db, 'clienti/CATTEL/raccolta clienti'))).then(snapshot => {` | JS Function | cantiere |
| `frontend/gestione.html` | 453 | `const unsubDNR = subscribeToAnagrafica('clienti/DNR/raccolta clienti', (snapshot) => {` | JS Function | main |
| `frontend/gestione.html` | 455 | `getDocsFromCache(query(collection(db, 'clienti/DAC/raccolta clienti'))).then(snapshot => {` | JS Function | cantiere |
| `frontend/gestione.html` | 464 | `const unsubDNR = subscribeToAnagrafica('clienti/DNR/raccolta clienti', (snapshot) => {` | JS Function | cantiere |
| `frontend/gestione.html` | 466 | `console.error("Errore caricamento clienti DNR:", error);` | Logica / Config | main |
| `frontend/gestione.html` | 471 | `const unsubGC = subscribeToAnagrafica('clienti/GRAN CHEF/raccolta clienti', (snapshot) => {` | JS Function | main |
| `frontend/gestione.html` | 477 | `console.error("Errore caricamento clienti DNR:", error);` | Logica / Config | cantiere |
| `frontend/gestione.html` | 481 | `console.error("Errore caricamento clienti GRAN CHEF:", error);` | Logica / Config | main |
| `frontend/gestione.html` | 482 | `const unsubGC = subscribeToAnagrafica('clienti/GRAN CHEF/raccolta clienti', (snapshot) => {` | JS Function | cantiere |
| `frontend/gestione.html` | 486 | `const unsubCattel = subscribeToAnagrafica('clienti/CATTEL/raccolta clienti', (snapshot) => {` | JS Function | main |
| `frontend/gestione.html` | 492 | `console.error("Errore caricamento clienti GRAN CHEF:", error);` | Logica / Config | cantiere |
| `frontend/gestione.html` | 496 | `console.error("Errore caricamento clienti CATTEL:", error);` | Logica / Config | main |
| `frontend/gestione.html` | 497 | `const unsubCattel = subscribeToAnagrafica('clienti/CATTEL/raccolta clienti', (snapshot) => {` | JS Function | cantiere |
| `frontend/gestione.html` | 502 | `if(currentTab === 'articoli') collPath = 'clienti/DNR/codici articoli';` | Logica / Config | main |
| `frontend/gestione.html` | 503 | `if(currentTab === 'rientri') collPath = 'clienti/DNR/rientri ddt';` | Logica / Config | main |
| `frontend/gestione.html` | 507 | `console.error("Errore caricamento clienti CATTEL:", error);` | Logica / Config | cantiere |
| `frontend/gestione.html` | 512 | `const unsubDac = subscribeToAnagrafica('clienti/DAC/raccolta clienti', (snapshot) => {` | JS Function | cantiere |
| `frontend/gestione.html` | 521 | `if(currentTab === 'clienti') {` | Logica / Config | main |
| `frontend/gestione.html` | 522 | `console.error("Errore caricamento clienti DAC:", error);` | Logica / Config | cantiere |
| `frontend/gestione.html` | 529 | `if(currentTab === 'articoli') collPath = `clienti/${activeTenant}/codici articoli`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 530 | `if(currentTab === 'rientri') collPath = `clienti/${activeTenant}/rientri ddt`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 548 | `if(currentTab === 'clienti') {` | Logica / Config | cantiere |
| `frontend/gestione.html` | 664 | `if(currentTab === 'clienti') {` | Logica / Config | main |
| `frontend/gestione.html` | 691 | `if(currentTab === 'clienti') {` | Logica / Config | cantiere |
| `frontend/gestione.html` | 833 | `if(currentTab === 'clienti') {` | Logica / Config | main |
| `frontend/gestione.html` | 851 | `collPath = `clienti/${tenant}/raccolta clienti`;` | Tenant Setup | main |
| `frontend/gestione.html` | 854 | `collPath = 'clienti/DNR/codici articoli';` | Logica / Config | main |
| `frontend/gestione.html` | 858 | `collPath = 'clienti/DNR/rientri ddt';` | Logica / Config | main |
| `frontend/gestione.html` | 861 | `if(currentTab === 'clienti') {` | Logica / Config | cantiere |
| `frontend/gestione.html` | 883 | `collPath = `clienti/${tenant}/raccolta clienti`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 884 | `if(currentTab === 'clienti') {` | Logica / Config | main |
| `frontend/gestione.html` | 887 | `collPath = `clienti/${activeTenant}/codici articoli`;` | Tenant Setup | main & cantiere |
| `frontend/gestione.html` | 889 | `if(currentTab === 'articoli') collPath = 'clienti/DNR/codici articoli';` | Logica / Config | main |
| `frontend/gestione.html` | 890 | `if(currentTab === 'rientri') collPath = 'clienti/DNR/rientri ddt';` | Logica / Config | main |
| `frontend/gestione.html` | 892 | `collPath = `clienti/${activeTenant}/rientri ddt`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 907 | `if (currentTab === 'clienti' && brand) {` | Logica / Config | main |
| `frontend/gestione.html` | 918 | `if(currentTab === 'clienti') {` | Logica / Config | cantiere |
| `frontend/gestione.html` | 921 | `collPath = `clienti/${tenant}/raccolta clienti`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 924 | `if(currentTab === 'articoli') collPath = `clienti/${activeTenant}/codici articoli`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 925 | `if(currentTab === 'rientri') collPath = `clienti/${activeTenant}/rientri ddt`;` | Tenant Setup | cantiere |
| `frontend/gestione.html` | 942 | `if (currentTab === 'clienti' && brand) {` | Logica / Config | cantiere |
| `frontend/gestione.html` | 987 | `if(currentTab === 'clienti') {` | Logica / Config | main |
| `frontend/gestione.html` | 1022 | `if(currentTab === 'clienti') {` | Logica / Config | cantiere |
| `frontend/gestione_anomalie.html` | 69 | `<button class="tab active" onclick="switchTab('clienti')">` | Logica / Config | main & cantiere |
| `frontend/gestione_anomalie.html` | 70 | `<span class="material-icons-round">storefront</span> Nuovi Clienti <span id="badge-clienti" style="background:#ef4444; c` | Logica / Config | main & cantiere |
| `frontend/gestione_anomalie.html` | 81 | `<div id="tab-clienti" class="tab-content active">` | Logica / Config | main & cantiere |
| `frontend/gestione_anomalie.html` | 82 | `<div id="list-clienti">` | Logica / Config | main & cantiere |
| `frontend/gestione_anomalie.html` | 116 | `window.getDocsConFallback(collection(db, 'clienti', 'DNR', 'raccolta clienti')),` | Logica / Config | main |
| `frontend/gestione_anomalie.html` | 117 | `window.getDocsConFallback(collection(db, 'clienti', 'GRAN CHEF', 'raccolta clienti')),` | Logica / Config | main |
| `frontend/gestione_anomalie.html` | 118 | `window.getDocsConFallback(collection(db, 'clienti', activeTenant, 'raccolta clienti')),` | Tenant Setup | main & cantiere |
| `frontend/gestione_anomalie.html` | 119 | `window.getDocsConFallback(collection(db, 'clienti', 'GRAN CHEF', 'raccolta clienti')),` | Logica / Config | cantiere |
| `frontend/gestione_anomalie.html` | 120 | `window.getDocsConFallback(collection(db, 'clienti', 'CATTEL', 'raccolta clienti')),` | Logica / Config | cantiere |
| `frontend/gestione_anomalie.html` | 121 | `window.getDocsConFallback(collection(db, 'clienti', 'DAC', 'raccolta clienti'))` | Logica / Config | cantiere |
| `frontend/gestione_anomalie.html` | 126 | `console.error("Errore durante il caricamento dei clienti master:", error);` | Logica / Config | main |
| `frontend/gestione_anomalie.html` | 130 | `console.error("Errore durante il caricamento dei clienti master:", error);` | Logica / Config | cantiere |
| `frontend/gestione_anomalie.html` | 144 | `const list = document.getElementById('list-clienti');` | Variable Assignment | main |
| `frontend/gestione_anomalie.html` | 145 | `const badge = document.getElementById('badge-clienti');` | Variable Assignment | main |
| `frontend/gestione_anomalie.html` | 149 | `const list = document.getElementById('list-clienti');` | Variable Assignment | cantiere |

*(Mostrati primi 300 risultati su 824 reali per questa categoria)*

## 5. Percorsi Storage
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `.gitignore` | 11 | `**/CONSEGNE/` | Logica / Config | main & cantiere |
| `.gitignore` | 69 | `**/CONSEGNE/` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 231 | `3. **Salvataggio Storage**: Salva i DDT estratti in `split_ddt/{data_consegna}/`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 241 | `* **CATTEL**: Ingestione file Excel multi-foglio via `_processa_excel_cattel_core_logic`. Ogni foglio rappresenta un gir` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 352 | `├── split_ddt/{data}/          [PDF estratti dai job DNR]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 353 | `├── REPORTS/{data}/            [Report fisici DNR (Asimmetria Legacy)]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 354 | `├── CATTEL/REPORTS/{data}/     [Report fisici CATTEL]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 355 | `├── GRAN CHEF/REPORTS/{data}/  [Report fisici GRAN CHEF]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 356 | `├── caches/                    [Cache JSON matrici distanze]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 357 | `├── caches_backup/             [Backup immutabili con timestamp]` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 421 | `* **Fase E — Uniformazione Storage**: Migrazione dei report DNR sotto `DNR/REPORTS/{data}/`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 432 | `4. **🟠 ALTO — Asimmetria Storage DNR**: DNR salva nella root `REPORTS/` anziché sotto `DNR/REPORTS/`.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 475 | `* **[`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/Gestio` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 30 | `### FASE 5 & 6 — RISULTATI DEI PARSER E INVENTARIO CONSEGNE` | Logica / Config | main & cantiere |
| `AUDIT_REPORT_25_07.md` | 31 | `Non abbiamo visibilità diretta sulla singola collection "deliveries" in quanto i dati risiedono aggregati nei file `spli` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 79 | `## 4. TASSONOMIA DOCUMENTI E CONSEGNE` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 87 | `├──► ORIGINAL_DDT (PDF Estratto memorizzato in split_ddt/)` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 65 | `3. **Backup Cloud Storage**: Protezione tramite snapshot immutabili con timestamp nella directory `caches_backup/` gesti` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 346 | `* **[`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/Gestio` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 397 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLo` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 501 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLo` | Logica / Config | main & cantiere |
| `README.md` | 49 | `* [`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/Gestione` | Logica / Config | main & cantiere |
| `analizza_storage.py` | 27 | `# Raggruppa per cartella principale (es. split_ddt, REPORTS, ecc)` | Logica / Config | main & cantiere |
| `audit_post_clean.py` | 49 | `if 'CATTEL' in b.name and '25-07-2026' in b.name and 'REPORTS' not in b.name and 'input_pdf_fornitore' not in b.name:` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F01-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F02-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 70 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F03-07-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F04-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/VERONA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F05-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F09-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F10-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F10-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F11-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F12-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F16-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F17-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F17-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F18-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F19-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F23-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F25-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 69 | `<a href="https://firebasestorage.googleapis.com/v0/b/log-solution-60007.firebasestorage.app/o/REPORTS%2F26-06-2026%2FDIS` | Logica / Config | main & cantiere |
| `check_cantiere.py` | 46 | `meta_path = f"split_ddt/{data_elab}/{etichetta}/ddt_estratti_{job_id}.json"` | Logica / Config | cantiere |
| `check_cantiere_offline.py` | 36 | `meta_path = f"split_ddt/{data_elab}/{etichetta}/ddt_estratti_{job_id}.json"` | Logica / Config | cantiere |
| `check_cantiere_offline2.py` | 44 | `meta_path = f"split_ddt/{data_elab}/{etichetta}/ddt_estratti_{job_id}.json"` | Logica / Config | cantiere |
| `clean_cattel_dryrun.py` | 43 | `("split_ddt/25-07-2026/CATTEL/1701002166-1791002678_25-07-2026.pdf", 1785091167790938),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 44 | `("split_ddt/25-07-2026/CATTEL/1701002166-1791002775_25-07-2026.pdf", 1785091168399077),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 45 | `("split_ddt/25-07-2026/CATTEL/1701006035-1791002895_25-07-2026.pdf", 1785091161665773),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 46 | `("split_ddt/25-07-2026/CATTEL/1701006224-1791003002_25-07-2026.pdf", 1785091158623274),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 47 | `("split_ddt/25-07-2026/CATTEL/1701009992-0_25-07-2026.pdf", 1785091160457987),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 48 | `("split_ddt/25-07-2026/CATTEL/1701010117-1791006103_25-07-2026.pdf", 1785091167190148),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 49 | `("split_ddt/25-07-2026/CATTEL/1701010720-0_25-07-2026.pdf", 1785091163506742),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 50 | `("split_ddt/25-07-2026/CATTEL/1701011001-0_25-07-2026.pdf", 1785091165375817),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 51 | `("split_ddt/25-07-2026/CATTEL/1701011323-0_25-07-2026.pdf", 1785091162272307),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 52 | `("split_ddt/25-07-2026/CATTEL/1701012821-0_25-07-2026.pdf", 1785091161057526),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 53 | `("split_ddt/25-07-2026/CATTEL/1701012866-1791007265_25-07-2026.pdf", 1785091162880820),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 54 | `("split_ddt/25-07-2026/CATTEL/1701013049-1791006800_25-07-2026.pdf", 1785091159236572),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 55 | `("split_ddt/25-07-2026/CATTEL/1701078754-0_25-07-2026.pdf", 1785091165978803),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 56 | `("split_ddt/25-07-2026/CATTEL/1701078766-0_25-07-2026.pdf", 1785091166584952),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 57 | `("split_ddt/25-07-2026/CATTEL/1701081272-0_25-07-2026.pdf", 1785091164117202),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 58 | `("split_ddt/25-07-2026/CATTEL/1701081272-1791001159_25-07-2026.pdf", 1785091164753144),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 59 | `("split_ddt/25-07-2026/CATTEL/1701081397-0_25-07-2026.pdf", 1785091169612392),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 60 | `("split_ddt/25-07-2026/CATTEL/1701082502-0_25-07-2026.pdf", 1785091159851505),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 61 | `("split_ddt/25-07-2026/CATTEL/1701084326-0_25-07-2026.pdf", 1785091170249923),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 62 | `("split_ddt/25-07-2026/CATTEL/1701088880-0_25-07-2026.pdf", 1785091169001565),` | Logica / Config | main & cantiere |
| `clean_cattel_dryrun.py` | 63 | `("split_ddt/25-07-2026/CATTEL/ddt_estratti_jgsbJytUKVtXWx0nKwRd.json", 1785091170405308)` | Logica / Config | main & cantiere |
| `core_genera_completo_giornata.py` | 5 | `path_base = f'{tenant}/REPORTS/{data_consegna}' if tenant != 'DNR' else f'REPORTS/{data_consegna}'` | Tenant Setup | cantiere |
| `core_genera_completo_giornata.py` | 19 | `prefix_search = f'split_ddt/{data_consegna}/'` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 85 | `storage_path = f'split_ddt/{data_consegna}/{tipo_ddt}/{pdf_name}'` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 111 | `full_blob = bucket.blob(f'REPORTS/{data_consegna}/DISTINTE_VIAGGIO/DISTINTA_{nome_giro}.pdf')` | Logica / Config | cantiere |
| `core_genera_completo_giornata.py` | 116 | `light_blob = bucket.blob(f'REPORTS/{data_consegna}/DISTINTE_VIAGGIO/DISTINTA_LIGHT_{nome_giro}.pdf')` | Logica / Config | cantiere |
| `deep_audit_25_07.py` | 177 | `category = "INPUT" if "input_pdf_fornitore" in b_name else ("REPORT" if "REPORTS" in b_name else "ALTRO")` | Logica / Config | main & cantiere |
| `download_file.py` | 8 | `blob = bucket.blob('input_pdf_fornitore/CATTEL_25-07-2026_ReportPianificazione.xlsx')` | Logica / Config | main & cantiere |
| `dr_system/MANUALE_GESTIONE_UMANA_DR.md` | 103 | `2. **Ripristino Storage**: Ricarica il tesoro chilometrico (le cartelle `caches`, `split\_ddt`, `REPORTS`) nel nuovo buc` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/orchestrate-test8.js` | 97 | `const cachesFound = cacheNamesRes.caches.map(c => c.cacheName);` | JS Function | main & cantiere |
| `e2e-tests/scripts/orchestrate-test8.js` | 98 | `console.log(`[CDP] Nomi Cache rilevati:`, cachesFound);` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/orchestrate-test8.js` | 101 | `const v6Cache = cacheNamesRes.caches.find(c => c.cacheName.includes('log-solution-v6.256'));` | JS Function | main & cantiere |
| `e2e-tests/tests/pwa/pwa-functions.js` | 32 | `const keys = await caches.keys();` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa-functions.js` | 35 | `const cache = await caches.open(k);` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa-rollback.spec.js` | 31 | `// Controllo caches` | Logica / Config | main & cantiere |
| `e2e-tests/tests/pwa/pwa-rollback.spec.js` | 33 | `return await window.caches.keys();` | Logica / Config | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 24 | `const keys = await caches.keys();` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 27 | `const cache = await caches.open(k);` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 67 | `const cachesInfo = await getCacheInfo(page);` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 68 | `expect(Object.keys(cachesInfo).some(k => k.includes('log-solution-v'))).toBeTruthy();` | JS Function | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 148 | `const cachesInfo = await getCacheInfo(page);` | Variable Assignment | main & cantiere |
| `e2e-tests/tests/pwa/pwa.spec.js` | 149 | `expect(Object.keys(cachesInfo).some(k => k.includes('log-solution-v'))).toBeFalsy();` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 394 | `const fileRef = sRef(storage, `REPORTS/${formattedDate}/manifest_link_viaggi.json`);` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 579 | `caches.keys().then(names => Promise.all(names.map(name => caches.delete(name)))).then(() => {` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 24 | `caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 33 | `caches.keys().then((cacheNames) =>` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 38 | `return caches.delete(name);` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 84 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 87 | `.catch(() => caches.match(event.request))` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 98 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 102 | `caches.match(event.request).then((res) => {` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 112 | `caches.match(event.request).then((cached) => {` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 116 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/core/sync-manager.js` | 321 | `// File path su Storage: CONSEGNE/CONSEGNE_[DATA]/photoId.jpg` | Logica / Config | main & cantiere |
| `frontend/core/sync-manager.js` | 322 | `const fileRef = sRef(storage, `CONSEGNE/OFFLINE_CONSEGNE/${photoId}.jpg`);` | Variable Assignment | main & cantiere |
| `frontend/core/sync-manager.js` | 481 | `const fileRef = sRef(storage, "caches/distanze_reali_cache.json");` | Variable Assignment | main & cantiere |
| `frontend/elaborazione.html` | 574 | `const path = `input_pdf_fornitore/${typeName}_${dateStr}_${safeName}`;` | Variable Assignment | main |
| `frontend/elaborazione.html` | 602 | `const path = `input_pdf_fornitore/${typeName}_${dateStr}_${safeName}`;` | Variable Assignment | cantiere |
| `frontend/elaborazione.html` | 887 | `return Swal.fire('Nessun Dato', 'Non ci sono nuovi file di dati (in split_ddt) da elaborare per questa giornata.', 'info` | Logica / Config | main |
| `frontend/elaborazione.html` | 934 | `return Swal.fire('Nessun Dato', 'Non ci sono nuovi file di dati (in split_ddt) da elaborare per questa giornata.', 'info` | Logica / Config | cantiere |
| `frontend/impostazioni.html` | 2061 | `selectCacheBackup.innerHTML = '<option value="">Nessun backup trovato su Storage (caches_backup/)</option>';` | Logica / Config | main & cantiere |
| `frontend/link_viaggi.html` | 302 | `const storagePathPrefix = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS` : 'REPORTS';` | Variable Assignment | cantiere |
| `frontend/link_viaggi.html` | 303 | `const sRef = storageRef(storage, `REPORTS/${dataLavoro}/manifest_link_viaggi.json`);` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 2212 | `const path = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}/viaggi_giornalieri_Johnson.json` : `REP` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 2256 | `const path = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}/viaggi_giornalieri_Johnson.json` : `REP` | Variable Assignment | cantiere |
| `frontend/mappa_zone.html` | 3653 | `const pathBase = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}` : `REPORTS/${targetFileDate}`;` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 3751 | `const pathBase = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}` : `REPORTS/${targetFileDate}`;` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 3804 | `const pathBase = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}` : `REPORTS/${targetFileDate}`;` | Variable Assignment | cantiere |
| `frontend/mappa_zone.html` | 3902 | `const pathBase = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}` : `REPORTS/${targetFileDate}`;` | Variable Assignment | cantiere |
| `frontend/mappa_zone.html` | 4031 | `const pathBase = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}` : `REPORTS/${targetFileDate}`;` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 4182 | `const pathBase = activeTenant !== 'DNR' ? `${activeTenant}/REPORTS/${targetFileDate}` : `REPORTS/${targetFileDate}`;` | Variable Assignment | cantiere |
| `frontend/mappe_autisti/GranChef V01_B_Zone_GranChef_V01_B_09-06-2026.html` | 224 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_03-06-2026.html` | 224 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V01_Zone_GranChef_V01_09-06-2026.html` | 224 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V02_Zone_GranChef_V02_03-06-2026.html` | 284 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V03_Zone_GranChef_V03_03-06-2026.html` | 334 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V04_Zone_GranChef_V04_03-06-2026.html` | 254 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V05_Zone_GranChef_V05_03-06-2026.html` | 204 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef V06_Zone_GranChef_V06_03-06-2026.html` | 294 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Ayoub_Zone_GranChef_V03_09-06-2026_-_Dopo_la_divisone_bolle.html` | 347 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Baye_Zone_GranChef_V02_09-06-2026_-_Dopo_la_divisone_bolle.html` | 351 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Costantin_Zone_GranChef_V01_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 221 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_01-06-2026.html` | 332 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V01_08-06-2026.html` | 332 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_04-06-2026.html` | 325 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_08-06-2026.html` | 281 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_11-06-2026.html` | 269 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026.html` | 315 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_12-06-2026_-_Copia.html` | 315 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_13-06-2026.html` | 315 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_1_Zone_GranChef_V02_16-06-2026.html` | 315 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_04-06-2026.html` | 299 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_08-06-2026.html` | 320 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V01_GranChef_V02_12-06-2026_-_Copia.html` | 305 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_05-06-2026.html` | 328 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_08-06-2026.html` | 269 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_16-06-2026.html` | 325 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V02_B_12-06-2026.html` | 305 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_BS_2_Zone_GranChef_V03_11-06-2026.html` | 272 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_11-06-2026.html` | 269 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026.html` | 302 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 250 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V01_16-06-2026.html` | 344 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V02_B_01-06-2026.html` | 332 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_04-06-2026.html` | 286 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_05-06-2026.html` | 302 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_08-06-2026.html` | 344 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_1_Zone_GranChef_V03_B_08-06-2026.html` | 326 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 289 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_16-06-2026.html` | 312 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V01_B_12-06-2026.html` | 289 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V02_01-06-2026.html` | 332 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_2_Zone_GranChef_V03_B_08-06-2026.html` | 311 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_12-06-2026_-_Copia.html` | 221 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_LAGO_VR_3_Zone_GranChef_V01_16-06-2026.html` | 260 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Orjito_Zone_GranChef_V01_B_09-06-2026_-_Dopo_la_divisone_bolle.html` | 279 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Titti_Zone_GranChef_V03_C_09-06-2026_-_Dopo_la_divisone_bolle.html` | 325 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_2_Zone_GranChef_V02_19-06-2026.html` | 309 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_Zone_GranChef_V01_01-06-2026.html` | 228 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_Zone_GranChef_V01_GranChef_V02_13-06-2026.html` | 305 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_Zone_GranChef_V01_GranChef_V02_19-06-2026.html` | 299 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_3_Zone_GranChef_V01_13-06-2026.html` | 273 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_B_Zone_GranChef_V01_B_09-06-2026.html` | 224 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_01-06-2026.html` | 319 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_09-06-2026.html` | 224 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_13-06-2026.html` | 318 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_17-06-2026.html` | 319 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_19-06-2026.html` | 332 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V02_Zone_GranChef_V02_19-06-2026.html` | 303 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_VR_1_Zone_GranChef_V03_B_05-06-2026.html` | 347 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_VR_MN_Zone_GranChef_V01_16-06-2026.html` | 318 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_VR_MN_Zone_GranChef_V02_B_B_01-06-2026.html` | 272 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_VR_MN_Zone_GranChef_V03_B_04-06-2026.html` | 250 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_VR_MN_Zone_GranChef_V03_B_B_08-06-2026.html` | 320 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_Vasyle_Zone_GranChef_V03_B_09-06-2026_-_Dopo_la_divisone_bolle.html` | 273 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef__VR_1_Zone_GranChef_V01_B_11-06-2026.html` | 257 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Lago_Gardone_Zone_GranChef_V01_23-06-2026.html` | 355 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Lago_Malcesine_Zone_GranChef_V02_23-06-2026.html` | 348 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Lago_Sirmione_Zone_GranChef_V01_23-06-2026.html` | 319 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Mantova_Zone_GranChef_V02_23-06-2026.html` | 306 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V01_Zone_3106_26-05-2026.html` | 364 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V01_Zone_3108_27-05-2026.html` | 364 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V01_Zone_3110_28-05-2026.html` | 384 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V01_Zone_3110_28-05-2026_29-05-2026.html` | 364 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V01_Zone_4108_03-06-2026.html` | 204 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V02_Zone_3107_26-05-2026.html` | 374 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V02_Zone_3109_27-05-2026.html` | 344 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V02_Zone_3111_28-05-2026.html` | 364 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V02_Zone_3111_28-05-2026_29-05-2026.html` | 374 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V02_Zone_4109_03-06-2026.html` | 214 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V03_Zone_3198_27-05-2026.html` | 164 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V03_Zone_3199_27-05-2026.html` | 314 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V03_Zone_3202_26-05-2026.html` | 244 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V03_Zone_3205_28-05-2026.html` | 314 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V03_Zone_3205_28-05-2026_29-05-2026.html` | 264 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V04_Zone_3199_27-05-2026.html` | 274 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V04_Zone_3203_27-05-2026.html` | 284 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V04_Zone_3206_28-05-2026.html` | 324 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V04_Zone_3206_28-05-2026_29-05-2026.html` | 354 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V04_Zone_3207_26-05-2026.html` | 364 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V05_Zone_3203_27-05-2026.html` | 284 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V05_Zone_3204_27-05-2026.html` | 304 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V05_Zone_3206_B_28-05-2026.html` | 164 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V05_Zone_3209_28-05-2026_29-05-2026.html` | 324 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V05_Zone_4113_26-05-2026.html` | 184 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V06_Zone_3204_27-05-2026.html` | 294 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V06_Zone_3209_28-05-2026.html` | 334 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V06_Zone_4120_26-05-2026.html` | 354 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V06_Zone_GranChef_V01_28-05-2026_29-05-2026.html` | 224 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V07_Zone_3209_27-05-2026.html` | 164 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V07_Zone_4111_28-05-2026.html` | 234 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V07_Zone_GranChef_V02_28-05-2026_29-05-2026.html` | 284 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V08_Zone_4199_27-05-2026.html` | 184 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V08_Zone_GranChef_V03_28-05-2026_29-05-2026.html` | 334 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V09_Zone_GranChef_27-05-2026.html` | 374 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V09_Zone_GranChef_V04_28-05-2026_29-05-2026.html` | 254 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V10_Zone_GranChef_V05_28-05-2026_29-05-2026.html` | 204 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/V11_Zone_GranChef_V06_28-05-2026_29-05-2026.html` | 294 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Valpolicella_Zone_GranChef_V02_23-06-2026.html` | 342 | `// --- GESTIONE STATO CONSEGNE ---` | Logica / Config | main & cantiere |
| `frontend/script.js` | 394 | `const fileRef = sRef(storage, `REPORTS/${formattedDate}/manifest_link_viaggi.json`);` | Variable Assignment | main |
| `frontend/script.js` | 403 | `const fileRef = sRef(storage, `REPORTS/${formattedDate}/manifest_link_viaggi.json`);` | Variable Assignment | cantiere |
| `frontend/script.js` | 589 | `caches.keys().then(names => Promise.all(names.map(name => caches.delete(name)))).then(() => {` | JS Function | main |
| `frontend/script.js` | 598 | `caches.keys().then(names => Promise.all(names.map(name => caches.delete(name)))).then(() => {` | JS Function | cantiere |
| `frontend/sw.js` | 66 | `caches.open(CACHE_NAME).then(async (cache) => {` | JS Function | main & cantiere |
| `frontend/sw.js` | 84 | `const cachedRes = await caches.match(req, { ignoreSearch: false });` | Variable Assignment | main & cantiere |
| `frontend/sw.js` | 149 | `caches.keys().then((cacheNames) =>` | JS Function | main & cantiere |
| `frontend/sw.js` | 154 | `return caches.delete(name);` | Logica / Config | main & cantiere |
| `frontend/sw.js` | 201 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/sw.js` | 204 | `.catch(() => caches.match(event.request, { ignoreSearch: true }).then((res) => {` | JS Function | main & cantiere |
| `frontend/sw.js` | 238 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/sw.js` | 242 | `caches.match(event.request, { ignoreSearch: true }).then((res) => {` | JS Function | main & cantiere |
| `frontend/sw.js` | 254 | `caches.match(event.request, { ignoreSearch: true }).then((cached) => {` | JS Function | main & cantiere |
| `frontend/sw.js` | 259 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `functions/core_func.py` | 39 | `blob_old_json = bucket.blob(f"REPORTS/{data_consegna}/viaggi_giornalieri_Johnson.json")` | Logica / Config | main & cantiere |
| `functions/core_func.py` | 52 | `f"REPORTS/{data_consegna}/",` | Logica / Config | main & cantiere |
| `functions/core_func.py` | 53 | `f"CONSEGNE/CONSEGNE_{data_f}/"` | Logica / Config | main & cantiere |
| `functions/core_func.py` | 66 | `prefix_search = f"split_ddt/{data_consegna}/"` | Logica / Config | main & cantiere |
| `functions/core_func.py` | 108 | `cercati = [f"split_ddt/{data_consegna}/**/ddt_estratti_*.json"]` | Logica / Config | main & cantiere |
| `functions/core_func.py` | 110 | `prefix_check = f"split_ddt/{data_consegna}/"` | Logica / Config | main & cantiere |
| `functions/core_func.py` | 495 | `path_base = f"REPORTS/{data_consegna}"` | Logica / Config | main & cantiere |
| `functions/infrastructure/firebase_setup.py` | 43 | `"directions_cache_v2.json": None,` | Logica / Config | cantiere |
| `functions/infrastructure/firebase_setup.py` | 54 | `blob = bucket.blob(f"caches/{filename}")` | Logica / Config | main |
| `functions/infrastructure/firebase_setup.py` | 55 | `blob = bucket.blob(f"caches/{filename}")` | Logica / Config | cantiere |
| `functions/infrastructure/firebase_setup.py` | 68 | `backup_latest = bucket.blob(f"caches_backup/{filename.replace('.json', '')}_latest.json")` | Logica / Config | main |
| `functions/infrastructure/firebase_setup.py` | 69 | `backup_latest = bucket.blob(f"caches_backup/{filename.replace('.json', '')}_latest.json")` | Logica / Config | cantiere |

*(Mostrati primi 300 risultati su 528 reali per questa categoria)*

## 6. Parser Excel e PDF
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `DEBT_ISOLAMENTO_TENANT_DNR.md` | 1 | `# Memoria Storica: Disaccoppiamento DNR e Isolamento Totale Tenant` | Tenant Setup | main & cantiere |
| `Pianificazione _ InTime.html` | 31 | `<script type="text/javascript" src="./Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download"></script><style typ` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 36 | `<div id="mnuForm:j_idt8" style="display: none;"></div><div id="mnuForm:idleDialog" class="ui-dialog ui-widget ui-widget-` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 38 | `<div class="navbar-header"><a id="mnuForm:j_idt15" href="https://intime.lac-consulting.eu/webClient/responseDetail#" cla` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 54 | `<i class="pi pi-bell" style="font-size: 20px" title="Notifiche"></i></div></a><div id="mnuForm:notification-panel" class` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 147 | `<br><button id="response-detail-form:j_idt78" name="response-detail-form:j_idt78" class="ui-button ui-widget ui-state-de` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 161 | `<div class="form-group col-lg-7"><div id="response-detail-form:j_idt118" class="ui-panel ui-widget ui-widget-content ui-` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 205 | `</div></td><td role="gridcell" style="width: 11%; text-align:center;"><span style="width:100%; text-align:center; color:` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 222 | `<div class="form-group col-lg-12"><div id="response-detail-form:lower-panel" class="ui-panel ui-widget ui-widget-content` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 380 | `</div></td><td role="gridcell" style="width: 15%; padding:3px; text-align:center;" class="ui-sortable-handle"><button id` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 397 | `<div class="form-group col-lg-6"><span class="h4" style="margin-bottom:10px;">Nessun dato disponibile</span><button id="` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 405 | `</div><div id="response-detail-form:copyNameDialog" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 415 | `</div></div></div><div id="response-detail-form:itinerariesDialog" class="ui-dialog ui-widget ui-widget-content ui-corne` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 428 | `</div></div></div><div id="response-detail-form:moveTruckDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 432 | `</div></div></div></div><div id="response-detail-form:chartsDialog" class="ui-dialog ui-widget ui-widget-content ui-corn` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 466 | `</div></div></div><div id="response-detail-form:confirmResponseDlg" class="ui-dialog ui-widget ui-widget-content ui-corn` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 474 | `<div class="form-group col-lg-3"><button id="response-detail-form:j_idt630" name="response-detail-form:j_idt630" class="` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 476 | `<div class="form-group col-lg-3"><button id="response-detail-form:j_idt632" name="response-detail-form:j_idt632" class="` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 478 | `<div class="form-group col-lg-3"><button id="response-detail-form:j_idt634" name="response-detail-form:j_idt634" class="` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 480 | `</div></div></div><div id="response-detail-form:logDialogDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 485 | `<div id="twStartReworkForm:twStartReworkDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hid` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 489 | `<span id="documentForm:growlDocument"></span><div id="documentForm:j_idt666" class="ui-dialog ui-widget ui-widget-conten` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 493 | `<div id="summaryRowEditForm:summaryRowEditDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-h` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 497 | `<div id="supportDriverForm:supportDriverDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hid` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 501 | `<div id="summaryRowNoteForm:summaryRowNoteDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-h` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 505 | `<div id="summaryRowNewForm:summaryRowNewDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hid` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 509 | `<div id="departureTimesEditForm:departureTimesEditDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-sha` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 513 | `<span id="smsForm:growlSms"></span><div id="smsForm:smsDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all u` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 517 | `<span id="emailForm:growlEmail"></span><div id="emailForm:emailDlg" class="ui-dialog ui-widget ui-widget-content ui-corn` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 521 | `<div id="notesForm:notesDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidden-container" s` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 525 | `<div id="closestFcForm:closestFcDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidden-cont` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 529 | `<div id="completeForm:completeDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidden-contai` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 533 | `<script id="searchBarCodeForm:j_idt816" type="text/javascript">quickSearchOrderCode = function() {return PrimeFaces.ab({` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 539 | `<div class="row"><label id="searchBarCodeForm:result-truck-searched" class="ui-outputlabel ui-widget" style="width: 100%` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 544 | `<div id="filterOrderForm:filterOrderDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidden-` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 548 | `<div id="nameTemplateForm:nameTemplateDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hidde` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 552 | `<div id="shuttleOrdersForm:shuttleOrdersDlg" class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow ui-hid` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 571 | `<div id="textarea_simulator" style="position: absolute; top: 0px; left: 0px; visibility: hidden;"></div><div class="ui-d` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/chartjs.js.xhtml` | 13 | `*/function bt(t){return t+.5\|0}const xt=(t,e,i)=>Math.max(Math.min(t,i),e);function _t(t){return xt(bt(2.55*t),0,255)}f` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 18 | `.ui-datepicker .ui-datepicker-header{position:relative;padding:.2em 0}.ui-datepicker .ui-datepicker-prev,.ui-datepicker ` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 21 | `.ui-datepicker-multi-2 .ui-datepicker-group{width:50%}.ui-datepicker-multi-3 .ui-datepicker-group{width:33.3%}.ui-datepi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 22 | `.ui-datepicker-rtl .ui-datepicker-next{left:2px;right:auto}.ui-datepicker-rtl .ui-datepicker-prev:hover{right:1px;left:a` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 24 | `.ui-slider-horizontal{height:.8em}.ui-slider-horizontal .ui-slider-handle{top:-.3em;margin-left:-.6em}.ui-slider-horizon` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 28 | `.ui-confirm-popup.ui-confirm-popup-flipped:after{border-bottom-color:transparent}.ui-confirm-popup.ui-confirm-popup-flip` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 29 | `.ui-accordion.ui-accordion-rtl .ui-accordion-header .ui-icon{right:.5m;left:auto}.ui-accordion.ui-accordion-rtl .ui-acco` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 30 | `.ui-accordion .ui-accordion-header .ui-panel-titlebar-icon .ui-icon{position:inherit}.ui-autocomplete{width:auto;cursor:` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 39 | `}@media screen and (min-width:70em){.ui-columntoggler .ui-columntoggler-item.ui-column-p-6{display:block}}.ui-dashboard-` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 40 | `.ui-datascroller .ui-datascroller-virtualscroll-wrapper{position:relative}.ui-datascroller .ui-datascroller-virtualscrol` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 42 | `.ui-datatable tr.ui-state-highlight{cursor:pointer}.ui-datatable .ui-selection-column .ui-chkbox-all{display:block;margi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 43 | `.ui-datatable-scrollable .ui-datatable-scrollable-header td{font-weight:normal}.ui-datatable .ui-datatable-scrollable-bo` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 49 | `.ui-datatable-reflow .ui-reflow-label,.ui-datatable-reflow .ui-reflow-dropdown{margin-bottom:10px;display:none}.ui-datat` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 57 | `.ui-divider.ui-divider-dashed.ui-divider-vertical:before{border-left-style:dashed}.ui-divider.ui-divider-dotted.ui-divid` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 60 | `.ui-multiselectlistbox.ui-state-disabled .ui-multiselectlistbox-item{cursor:default}.ui-multiselectlistbox .ui-multisele` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 76 | `.ui-selectcheckboxmenu-panel .ui-selectcheckboxmenu-table th:first-of-type,.ui-selectcheckboxmenu-panel .ui-selectcheckb` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 77 | `.ui-selectcheckboxmenu-header .ui-inputfield{padding:1px 20px 1px 2px}.ui-selectcheckboxmenu-header span.ui-icon{float:l` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 80 | `.ui-splitbuttonmenu .ui-splitbuttonmenu-filter{width:100%;padding-right:15px;-moz-box-sizing:border-box;-webkit-box-sizi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 81 | `.ui-splitbuttonmenu .ui-divider-horizontal{width:auto}div.ui-button,.ui-splitbutton{display:inline-block}.ui-password-pa` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 109 | `.ui-growl-image-info{background-position:0 -264px}.ui-growl-image-warn{background-position:0 -396px}.ui-growl-image-erro` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 110 | `.ui-menu .ui-menuitem-link{display:block;width:92%;outline:0;text-decoration:none;font-weight:400;border:solid 1px trans` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 111 | `.ui-menu .ui-menu-parent .ui-menu-child{display:none;width:12.5em;padding:.3em;position:absolute;margin:0;outline:0;line` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 113 | `.ui-menubar .ui-menu-child .ui-menuitem-link{width:92%}.ui-menubar .ui-widget-header{clear:none;width:auto;margin:0 3px ` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 115 | `.ui-megamenu .ui-widget-header span{display:block;float:left;font-size:1em;margin:0 auto;padding:.4em .3em}.ui-breadcrum` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 117 | `.ui-slidemenu .ui-menu-list{position:absolute;top:0}.ui-slidemenu .ui-menu-parent{position:static}.ui-slidemenu .ui-menu` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 118 | `.ui-panelmenu .ui-panelmenu-header a{display:block;padding:.5em .5em .5em 2.2em}.ui-panelmenu .ui-panelmenu-header .ui-i` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 128 | `.ui-panel-collapsed-h .ui-panel-titlebar-icon,.ui-panel-collapsed-h .ui-panel-titlebar-icon:hover,.ui-panel-collapsed-h ` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 161 | `.ui-fluid .ui-tree{width:100%}.ui-treetable table{border-collapse:collapse;width:100%;table-layout:fixed}.ui-treetable .` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 162 | `.ui-treetable tbody td{border-color:inherit}.ui-treetable .ui-treetable-toggler{display:inline-block;vertical-align:midd` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 163 | `.ui-treetable.ui-treetable-scrollable table{table-layout:fixed}.ui-treetable-scrollable .ui-treetable-scrollable-header,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.css.xhtml` | 173 | `}.ui-dataview .ui-dataview-header{border-bottom:0 none}.ui-dataview .ui-dataview-header,.ui-dataview .ui-dataview-footer` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 5 | `(a.options.styleClass\|\|"")+'" data-pfdlgcid\x3d"'+PrimeFaces.escapeHTML(a.pfdlgcid)+'" data-widget\x3d"'+e+'"\x3e\x3c/` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 7 | `(a.options.iframeStyleClass\|\|"")+'" style\x3d"border:0 none" frameborder\x3d"0"\x3e\x3c/iframe\x3e\x3c/div\x3e');f.app` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 10 | `blockScroll:a.options.blockScroll,resizable:a.options.resizable,hasIframe:!0,draggable:a.options.draggable,width:a.optio` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 13 | `(g="(function(ext){this."+h+"})",g=b.PrimeFaces.csp.NONCE_VALUE?PrimeFaces.csp.evalResult(g,b.PrimeFaces.csp.NONCE_VALUE` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 17 | `PrimeFaces.widget.AccordionPanel=PrimeFaces.widget.BaseWidget.extend({init:function(a){this._super(a);this.stateHolder=$` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 18 | `initActive:function(){var a=this.stateHolder.val();if(this.cfg.multiple){if(this.cfg.active=[],null!=a&&0<a.length){a=th` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 19 | `bindEvents:function(){var a=this;this.headers.on("mouseover",function(){var b=$(this);b.hasClass("ui-state-active")\|\|b` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 20 | `this.bindKeyEvents()},bindKeyEvents:function(){this.headers.on("focus.accordion",function(){$(this).addClass("ui-tabs-ou` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 22 | `unselect:function(a){this.panels.eq(a).prev().hasClass("ui-state-active")&&(this.cfg.controlled\|\|this.hide(a),this.fir` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 71 | `b,c){b.is(".ui-autocomplete-table")?(this.colspan\|\|(this.colspan=this.items.eq(0).children("td").length),a=$('\x3ctr c` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 159 | `!1;this.headers=this.thead.find("\x3e tr \x3e th");this.sortableColumns=this.headers.filter(".ui-sortable-column");this.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 188 | `a.eq(b),d=c.find(".ui-reflow-headertext:first").text();c=c.children(".ui-column-title");d=d&&d.length?d:c.text();c=this.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 189 | `this.scrollFooter=this.jq.children(".ui-datatable-scrollable-footer");this.scrollStateHolder=$(this.jqId+"_scrollState")` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 198 | `this.jq.parent().innerHeight()*(parseInt(this.cfg.scrollHeight)/100),b=this.jq.children(".ui-datatable-header"),c=this.j` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 200 | `this;this.jq.children(".ui-widget-header").each(function(){b.setOuterWidth($(this),a)});this.scrollHeader.width(a);this.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 202 | `fixColumnWidths:function(){var a=this;if(!this.columnWidthsFixed){if(this.cfg.scrollable)this.scrollHeader.find("\x3e .u` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 281 | `c=c.clone();for(var e=c.children(),f=0;f<e.length;f++){var g=e.eq(f);g.width(b.eq(f).width());g.children().remove(".ui-c` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 282 | `$(this);(e.hasClass("ui-rowgroup-header")\|\|e.hasClass("ui-expanded-row-content"))&&toIndex--});toIndex=Math.max(toInde` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 294 | `this.cfg.reflow){b=0<b?0:1;a=a.text().replace(/[^a-zA-Z0-9\u00C0-\u017F]/g,"");var c=a.indexOf("Filter by");-1!==c&&(a=a` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 296 | `e)}},bindToggleRowGroupEvents:function(){this.tbody.children("tr.ui-rowgroup-header").find("\x3e td:first \x3e a.ui-rowg` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 297 | `(b.attr("aria-expanded",!0),c.addClass("ui-icon-circle-triangle-s").removeClass("ui-icon-circle-triangle-e"),d.nextUntil` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 301 | `updateColumnsView:function(){if(!this.isEmpty()){if(this.headers&&!this.hasColGroup())for(var a=this.tbody.find("\x3e tr` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 304 | `this.scrollContainer.children(".ui-datatable-scrollable-header");this.scrollHeaderBox=this.scrollHeader.children("div.ui` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 305 | `this.scrollBodyTable=this.cfg.virtualScroll?this.scrollBody.children("div").children("table"):this.scrollBody.children("` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 313 | `a.adjustScrollWidth()},150)})},cloneHead:function(){this.frozenTheadClone&&this.frozenTheadClone.remove();this.frozenThe` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 314 | `100),b=this.jq.children(".ui-datatable-header"),c=this.jq.children(".ui-datatable-footer");b=0<b.length?b.outerHeight(!0` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 315 | `this.frozenLayout.innerWidth();a=parseInt(a*(parseInt(this.cfg.scrollWidth)/100));this.setScrollWidth(a)},setScrollWidth` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 316 | `this.scrollColgroup),this._fixColumnWidths(this.frozenHeader,this.frozenFooterCols,this.frozenColgroup)):this.jq.find("\` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 335 | `this.cfg.absolutePositioned=this.jq.hasClass("ui-dialog-absolute");this.jqEl=this.jq[0];this.positionInitialized=!1;this` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 359 | `showMessage:function(a){a.beforeShow&&PrimeFaces.csp.eval(a.beforeShow);a.icon?(this.icon.removeClass().addClass("ui-ico` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 496 | `this.bindPanelContentEvents();this.bindPanelKeyEvents();this.isDynamicLoaded=!0},renderPanel:function(){var a=this.id+"_` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 550 | `function(){setTimeout(function(){a.filter(a.filterInput.val())},2)})},highlightNext:function(a){var b=this.menuitems.fil` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 552 | `contains:this.containsFilter,endsWith:this.endsWithFilter,custom:this.cfg.filterFunction};this.filterMatcher=this.filter` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 553 | `this.menuitemContainer.children(".ui-separator").show();else{for(var c=0;c<this.menuitems.length;c++){var d=this.menuite` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 559 | `a.closest(".ui-multiselectlistbox-listcontainer").nextAll().remove();this.input.val(a.attr("data-value"));var b=a.childr` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 562 | `this.cfg.showHeaders&&f.prepend('\x3cdiv class\x3d"ui-multiselectlistbox-header ui-widget-header ui-corner-top"\x3e'+Pri` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 599 | `function(b){$(this).removeClass("ui-state-hover")});this.cfg.overlay&&(this.menuitemLinks.on("click",function(){a.hide()` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 602 | `PrimeFaces.createStorageKey(this.id,"PlainMenu",this.cfg.statefulGlobal)},collapseSubmenu:function(a,b){var c=a.nextUnti` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 635 | `PrimeFaces.widget.PanelMenu=PrimeFaces.widget.BaseWidget.extend({init:function(a){this._super(a);this.headers=this.jq.fi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 636 | `this.focusedItem=null;this.menuText.attr("tabindex",-1);this.menuText.attr("role","menuitem");this.treeLinks.find("\x3e ` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 638 | `c)});this.treeLinks.on("click",function(b){var c=$(this),d=c.parent();c.next().is(":visible")?a.collapseTreeItem(d):a.ex` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 642 | `var b="click."+this.id;$(document.body).off(b).on(b,function(c){$(c.target).closest(".ui-panelmenu").length\|\|a.removeF` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 647 | `this.expandedNodes=a.split(","),a=0;a<this.expandedNodes.length;a++){var b=$(PrimeFaces.escapeClientId(this.expandedNode` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 648 | `c.length;a++)this.expandedNodes.push(c.eq(a).parent().attr("id"))}},removeAsExpanded:function(a){var b=a.attr("id");this` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 657 | `PrimeFaces.widget.Panel=PrimeFaces.widget.BaseWidget.extend({init:function(a){this._super(a);this.header=this.jq.childre` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 658 | `"_menu").on("click.panel",function(b){b.preventDefault()});this.header.find(".ui-panel-titlebar-icon").on("mouseover.pan` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 659 | `!0);this.toggleState(!1,"ui-icon-plusthick","ui-icon-minusthick");"vertical"===this.cfg.toggleOrientation?this.slideDown` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 798 | `this.navcrollerLeft=this.navscroller.children(".ui-tabs-navscroller-btn-left"),this.navcrollerRight=this.navscroller.chi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 800 | `"resize."+this.id+"_align",this.jq,function(){a.initScrolling()})}},destroy:function(){this._super();PrimeFaces.env.isTo` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 801 | `a.headerContainer.index(c);c.hasClass("ui-state-disabled")\|\|d===a.cfg.selected\|\|(a.select(d),c.trigger("focus.tabvie` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 804 | `bindKeyEvents:function(){var a=this,b=this.headerContainer;b.not(".ui-state-disabled").attr("tabindex",this.tabindex);b.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 806 | `this,b=-1;this.addRefreshListener(function(){$(this.jqId+"\x3eul\x3eli.ui-tabs-header").each(function(){var c=$("a",this` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 807 | `initScrolling:function(){this.headerContainer.length&&(this.lastTab.position().left+this.lastTab.width()-this.firstTab.p` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 811 | `this.fireTabChangeEvent(c):this.cfg.multiViewState&&(a={source:this.id,partialSubmit:!0,partialSubmitFilter:PrimeFaces.e` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 815 | `b.show(d)}};this.hasBehavior("tabChange")?this.callBehavior("tabChange",a):PrimeFaces.ajax.Request.handle(a)},remove:fun` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 816 | `(b=this.headerContainer.filter(":not(.ui-state-disabled):first"),b.length&&this.select(b.index(),!0)):this.select(b,!0))` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 817 | `this.callBehavior("tabClose",{params:[{name:this.id+"_closeTab",value:a},{name:this.id+"_tabindex",value:b}]})},reload:f` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 940 | `this.callBehavior("unselect",{params:[{name:this.id+"_instantUnselection",value:a}]})},setupScrolling:function(){this.sc` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 941 | `this.headerTable=this.scrollHeaderBox.children("table");this.bodyTable=this.scrollBody.children("table");this.footerTabl` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 944 | `a.adjustScrollHeight();a.percentageScrollWidth&&a.adjustScrollWidth()})},cloneTableHeader:function(a,b){a=a.clone();a.fi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 945 | `this.bodyTable)},fixColumnWidths:function(){var a=this;if(!this.columnWidthsFixed){if(this.cfg.scrollable)this.headerCol` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 948 | `(parseInt(this.cfg.scrollHeight)/100),b=this.jq.children(".ui-treetable-header").outerHeight(!0),c=this.jq.children(".ui` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 949 | `b){var c=a.outerWidth()-a.width();a.width(b-c)},hasVerticalOverflow:function(){return this.cfg.scrollHeight&&this.bodyTa` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 990 | `PrimeFaces.widget.ScrollTop=PrimeFaces.widget.BaseWidget.extend({init:function(a){this._super(a);this.scrollElement="win` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 991 | `start:function(){"auto"===c&&"auto"===a.jq.css("zIndex")&&a.jq.css("zIndex",PrimeFaces.nextZindex())}}):a.jq.fadeOut({du` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 997 | `PrimeFaces.widget.DataView=PrimeFaces.widget.BaseWidget.extend({init:function(a){this._super(a);this.header=this.jq.chil` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 14 | `function(){$(this).removeClass("ui-state-focus");b.hasClass("hasDatepicker")?setTimeout(function(){e()},150):e()});b.is(` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 35 | `e(this.container).attr("id")+"_panel']").not(this.panel).remove(),this.panel.appendTo(this.options.appendTo)):this.panel` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 36 | `d){e(d).val(a);b+=1;12===b&&(b=0,a+=1)})}this.options.monthNavigator&&"month"!==this.options.view&&(b=this.viewDate.getM` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 40 | `renderDateView:function(){this.monthsMetadata=this.createMonths(this.viewDate.getMonth(),this.viewDate.getFullYear());re` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 41 | `c+'\x3c/div\x3e\x3c/div\x3e\x3cdiv class\x3d"ui-monthpicker"\x3e'+d+"\x3c/div\x3e\x3c/div\x3e"},renderTimePicker:functio` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 43 | `g>f\|\|h&&h<f)k+=" ui-helper-hidden";return'\x3cdiv class\x3d"ui-datepicker-buttonbar ui-widget-header"\x3e\x3cdiv class` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 46 | `c,d);return'\x3cdiv class\x3d"ui-datepicker-group ui-widget-content"\x3e\x3cdiv class\x3d"ui-datepicker-header ui-widget` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 62 | `this.onInputClick.bind(a)),this.triggerButton))this.triggerButton.off("click.datePicker-triggerButton").on("click.datePi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 63 | `".ui-datepicker-header \x3e .ui-datepicker-next").on("click.datePicker-navForward",".ui-datepicker-header \x3e .ui-datep` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 64 | `".ui-datepicker-header \x3e .ui-datepicker-title \x3e .ui-datepicker-year",null,this.onYearDropdownChange.bind(a));this.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 77 | `this.options.onMonthChange.call(this,b.getMonth()+1,b.getFullYear())}else if("month"===this.options.view){c=b.getFullYea` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/datepicker.js.xhtml` | 78 | `c=this.panel.find(".ui-datepicker-header \x3e .ui-datepicker-next");if(this.options.disabled)b.addClass("ui-state-disabl` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/jquery-plugins.js.xhtml` | 190 | `e.ui.mouse,{version:"1.13.2",widgetEventPrefix:"slide",options:{animate:!1,classes:{"ui-slider":"ui-corner-all","ui-slid` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/jquery-plugins.js.xhtml` | 255 | `origin:a.origin\|\|["middle","center"]},a);a.fade&&(c.from.opacity=1,c.to.opacity=0);e.effects.effect.size.call(this,c,b` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/jquery.js.xhtml` | 2 | `!function(e,t){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=e.document?t(e,!0):f` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 213 | `// https://github.com/Leaflet/Leaflet/blob/master/src/map/Map.js#L1490-L1508` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 51 | `// has [been supported for longer](http://stackoverflow.com/a/9181508/229001).` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12126 | `header: 'Routing error',` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12155 | `var header,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12161 | `header = L.DomUtil.create('h3', null, this._element);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12164 | `header.innerHTML = this.options.header;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 328 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 562 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 721 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 940 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1642 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1848 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2009 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2185 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2538 | `.find('.ui-datatable-scrollable-header-box').attr('style', 'margin-right: -1px !important');` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2546 | `.find('.ui-datatable-scrollable-header-box').css('margin-right', '');` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.browser.print.js.download` | 127 | `eval("/**\r\n\tMIT License http://www.opensource.org/licenses/mit-license.php\r\n\tAuthor Igor Vladyka <igor.vladyka@gma` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.browser.print.js.download` | 138 | `eval("/**\r\n\tMIT License http://www.opensource.org/licenses/mit-license.php\r\n\tAuthor Igor Vladyka <igor.vladyka@gma` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 1 | `@import url("//fonts.googleapis.com/css?family=Open+Sans:400italic,700italic,400,700");article,aside,details,figcaption,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 2 | `:not(.fa, .pi){font-family:'Roboto', 'Open Sans', sans-serif !important;}html, body{height:100%;}body{padding-top:50px;}` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 3 | `rgba(255, 255, 255, 0.125);}.nav-stacked .nav-header{margin-bottom:10px;font-size:18px;}body#login{padding-bottom:40px;}` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 4 | `.ui-widget-content .ui-inputfield.ui-state-error{border:2px solid #CD0A0A;}.ui-widget{font-size:14px;}.container{width:1` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 9 | `.ui-widget-header .ui-state-disabled{opacity:.65;}.ui-selectonemenu-item{font-size:12px !important;}legend{width:auto;fo` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 18 | `.ui-paginator-page, .ui-paginator-next, .ui-paginator-last{background:white !important;}.close-btn .ui-corner-left, .clo` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 19 | `.ui-treetable tbody td{padding:3px 7px;}.ui-datatable thead th{background-image:none !important;background-color:#f8f9fa` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/maplibre-gl.js.download` | 31 | `define(["exports"],(function(t){"use strict";function e(t){return t&&t.__esModule&&Object.prototype.hasOwnProperty.call(` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/maplibre-gl.js.download` | 35 | `define(["./shared"],(function(t){"use strict";var e="3.2.1";class i{static testProp(t){if(!i.docStyle)return t[0];for(le` | Python Function Def | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 40 | `.dialog-no-header .ui-dialog-titlebar {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 44 | `.dialog-no-header .ui-dialog-content.ui-widget-content {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 118 | `.nav-stacked .nav-header {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 387 | `.ui-state-error, .ui-widget-content .ui-state-error, .ui-widget-header .ui-state-error` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 394 | `.ui-inputfield.ui-state-error, .ui-widget-header .ui-inputfield.ui-state-error,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 449 | `width: 150px;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 542 | `.enmon-table.ui-datatable-header {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 784 | `.ui-widget-header .ui-state-disabled {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 814 | `.enmon-channel-vpanel .ui-widget-header {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 961 | `.enmon-table.ui-datatable-header {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 1447 | `.ui-datatable-scrollable-header thead th {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 1474 | `.ui-datatable-scrollable-header {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/style.css` | 1480 | `.ui-datatable-scrollable-header-box {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/sub-trips-map-controller.js.download` | 154 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/sub-trips-map-controller.js.download` | 388 | `return { url, headers: { 'ApiKey': apiKey } };` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.css.xhtml` | 31 | `.ql-snow .ql-color-picker .ql-picker-options{padding:3px 5px;width:152px}.ql-snow .ql-color-picker .ql-picker-item{borde` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.css.xhtml` | 32 | `.ql-snow .ql-picker.ql-header{width:98px}.ql-snow .ql-picker.ql-header .ql-picker-label::before,.ql-snow .ql-picker.ql-h` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.css.xhtml` | 33 | `.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="3"]::before,.ql-snow .ql-picker.ql-header .ql-picker-item[dat` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.css.xhtml` | 34 | `.ql-snow .ql-picker.ql-header .ql-picker-label[data-value="5"]::before,.ql-snow .ql-picker.ql-header .ql-picker-item[dat` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.css.xhtml` | 35 | `.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="1"]::before{font-size:2em}.ql-snow .ql-picker.ql-header .ql-pi` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.css.xhtml` | 36 | `.ql-snow .ql-picker.ql-header .ql-picker-item[data-value="6"]::before{font-size:.67em}.ql-snow .ql-picker.ql-font{width:` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 158 | `I[0];I=I[1];var K=(0,v.default)({},G.formats(),{list:"checked"});G=(new z.default).retain(E.index).insert("\n",K).retain` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 159 | `G.format).retain(I.length()-K-1).retain(1,{header:null});this.quill.updateContents(G,C.default.sources.USER);this.quill.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 162 | `color:h(83),direction:{"":h(84),rtl:h(85)},float:{center:h(86),full:h(87),left:h(88),right:h(89)},formula:h(90),header:{` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 216 | `(G.classList.contains("ql-font")?d(G,v):G.classList.contains("ql-header")?d(G,z):G.classList.contains("ql-size")&&d(G,D)` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 225 | `g.default.register({"formats/align":x.AlignClass,"formats/direction":q.DirectionClass,"formats/indent":p.IndentClass,"fo` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 320 | `p))throw new TypeError("Cannot call a class as a function");var d=(p.__proto__\|\|Object.getPrototypeOf(p)).apply(this,a` | Class Def | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 393 | `y(h),u=[["bold","italic","link"],[{header:1},{header:2},"blockquote"]];h=function(k){function n(l,v){x(this,n);null!=v.m` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 401 | `var b=h(9),f=y(b);b=h(44);var m=y(b),t=h(15),u=y(t),e=h(22);h=h(26);var r=y(h),k=[[{header:["1","2","3",!1]}],["bold","i` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/texteditor.js.xhtml` | 407 | `PrimeFaces.widget.TextEditor=PrimeFaces.widget.DeferredWidget.extend({toolbarTemplate:'\x3cdiv class\x3d"ui-editor-toolb` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/theme.css.xhtml` | 1 | `/** jQuery UI CSS Framework 1.8.9** Copyright 2011, AUTHORS.txt (http://jqueryui.com/about)* Dual licensed under the MIT` | Logica / Config | main & cantiere |
| `analizza_storage.py` | 42 | `print(f"Totale File presenti: {file_count}")` | Logica / Config | main & cantiere |
| `analizza_storage.py` | 43 | `print(f"Spazio Totale Occupato: {total_mb:.2f} MB")` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_RvfDgA7vTgPOCWFev6bf", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 6h 4m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 71 | `</div><div class="card" id="card-0" onclick="selectCard(0)" style="grid-template-columns: 42px 1fr auto;"><div class="st` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_IUnudti8E1xuOJbcny4h", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 6h 14m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 4h 6m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 8m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 71 | `</div><div class="card" id="card-0" onclick="selectCard(0)" style="grid-template-columns: 42px 1fr 44px;"><div class="st` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 44m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_HmOYhzXBoEmSLHJrj7yx", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 24m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 72 | `</div><div class="card" id="card-0" onclick="selectCard(0)" style="grid-template-columns: 42px 1fr 44px;"><div class="st` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 84 | `const PUNTI=[{"lat": 45.5817136964835, "lng": 10.47910862445829, "nome": "ALLE TROTE-OTTOLINI F.LI&C.SNC TRATTORIA", "is` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 30m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 7m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 16m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 55m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 55m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 55m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 27m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 6h 34m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 56 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 58m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 55m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 26m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 37m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 30m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/4_mappa_zone_google.html` | 15 | `.zone-header { display: flex; align-items: center; gap: 10px; font-weight: 800; }` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/4_mappa_zone_google.html` | 28 | `const ZONE = [{"id_zona": "GC_WB8HvCPskBeYXE0fgQ2K", "nome_giro": "Viaggio 1 Grand Chef", "color": "#4f46e5", "lista_pun` | Variable Assignment | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/4_mappa_zone_google.html` | 40 | `div.innerHTML = `<div class="zone-header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 5h 26m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 71 | `</div><div class="card" id="card-0" onclick="selectCard(0)" style="grid-template-columns: 42px 1fr 44px;"><div class="st` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 3h 14m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 50 | `<div class="header">` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 55 | `<div><div class="stat-val">&#x23F1;&#xFE0F; 6h 26m</div><div class="stat-lbl">Totale</div></div>` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 16 | `.header{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}` | Logica / Config | main & cantiere |

*(Mostrati primi 300 risultati su 1258 reali per questa categoria)*

## 7. Mappe, magazzini e routing
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `ARCHITECTURE.md` | 185 | `* `mappa_zone.html` & `mappa_google.html`: Ottimizzazione grafica e trascinamento tappe.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 460 | `\| **puntoDiConsegna** \| Destinazione fisica sul territorio identificata da indirizzo e coordinate GPS. \| `[DA MIGLIOR` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 57 | `\| **Punto di Consegna** \| Indirizzo fisico geografico e coordinate GPS di destinazione raggiunti dai veicoli. \| Terri` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 65 | `\| **Distinta di Viaggio** \| Documento riepilogativo PDF generato per l'autista contenente la sequenza ufficiale delle ` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 260 | `* Capitolo M-003 (*Obiettivi Strategici*): Per le tappe di sviluppo ed i traguardi quantitativi.` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 324 | `* L'entità *Punto di Consegna* è definita dalle sue coordinate geografiche e caratteristiche di sosta, separata concettu` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 387 | `* **Scopo del Capitolo**: Spiegare le dinamiche economiche di valorizzazione dei servizi resi da Loge Solution ai commit` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 467 | `* **Scopo del Capitolo**: Definire l'entità geografica del Punto di Consegna sul territorio, distinguendolo dal codice c` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime.html` | 147 | `<br><button id="response-detail-form:j_idt78" name="response-detail-form:j_idt78" class="ui-button ui-widget ui-state-de` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 43 | `d.preventDefault();break;case "Enter":a.timeout&&a.deleteTimeout();0<e.length?(a.preventInputChangeEvent=!0,e.trigger("c` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 47 | `function(){a.touchToDropdownButton\|\|(a.itemClick=!0)})},processKeyEvent:function(a){var b=this;if(b.suppressInput)a.pr` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 48 | `(b.timeout&&b.deleteTimeout(),b.fireClearEvent())}},showItemtip:function(a){if(a.hasClass("ui-autocomplete-moretext"))th` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 71 | `b,c){b.is(".ui-autocomplete-table")?(this.colspan\|\|(this.colspan=this.items.eq(0).children("td").length),a=$('\x3ctr c` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 79 | `c):!b},show:function(a){var b=this;if(!this.isBlocking()){var c=this.cfg.delay\|\|0;this.timeout=setTimeout(function(){i` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 84 | `deleteTimeout:function(){clearTimeout(this.timeout);this.timeout=null}});` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 365 | `{name:a.id+"_dropId",value:a.cfg.target}]},b.call(a,c))}}});PrimeFaces.widget.Effect=PrimeFaces.widget.BaseWidget.extend` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 375 | `default:var c=a.extractQuery();c&&c.length>=a.cfg.minQueryLength&&(a.timeout&&a.clearTimeout(a.timeout),a.timeout=setTim` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 379 | `a.jq.trigger("focus");a.jq.setSelection(d-e,d);a.jq.replaceSelectedText(c);a.invokeItemSelectBehavior(b,c);a.hide()})},i` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 567 | `b.appendTo(this.jq).fadeIn()},bindEvents:function(a){var b=this,c=this.cfg.sticky;a.on("mouseover",function(){var d=$(th` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 568 | `0,function(){a.slideUp("normal","easeInOutCirc",function(){a.remove()})})},setRemovalTimeout:function(a){var b=this,c=se` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 589 | `PrimeFaces.widget.Menubar=PrimeFaces.widget.TieredMenu.extend({showSubmenu:function(a,b){var c=null;c=a.parent().hasClas` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 605 | `!0;this.hide();PrimeFaces.utils.disableButton(this.button)},enable:function(){this.cfg.disabled=!1;PrimeFaces.utils.enab` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 634 | `{my:"left top",at:"right top",of:a,collision:"flipfit"}:{my:"left top",at:"left bottom",of:a,collision:"flipfit"};this.t` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 825 | `var e=d.data("tooltip");e&&(a.cfg.escape?a.jq.children(".ui-tooltip-text").text(e):a.jq.children(".ui-tooltip-text").htm` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 831 | `if(!b\|\|!c)switch(this.cfg.position){case "right":b="left center";c="right center";break;case "left":b="right center";c` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 832 | `_show:function(){var a=this;if(!this.cfg.beforeShow\|\|!1!==this.cfg.beforeShow.call(this)){var b="";this.isAutoHide()&&` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/components.js.xhtml` | 833 | `this;this.isVisible()&&(this.isAutoHide()\|\|!1!==this.allowHide)&&(this.jq.hide(this.cfg.hideEffect,{},this.cfg.hideEff` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 39 | `if(!PrimeFaces.ajax){PrimeFaces.ab=function(a,c){for(var b in a)a.hasOwnProperty(b)&&PrimeFaces.ajax.CFG_SHORTCUTS[b]&&(` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 45 | `var d=function(){return setTimeout(function(){b.requests.push(a);1===b.requests.length&&PrimeFaces.ajax.Request.send(a)}` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 56 | `[n,this])}};e?($.each(h,function(n,q){f.append(q.name,q.value)}),g.data=f,g.enctype="multipart/form-data",g.processData=` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 119 | `PrimeFaces.widget.AjaxStatus=PrimeFaces.widget.BaseWidget.extend({init:function(a){this._super(a);this.bind()},bind:func` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 120 | `a.trigger("complete",arguments)});this.addDestroyListener(function(){$(document).off(c)});window.jsf&&jsf.ajax&&(jsf.aja` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/core.js.xhtml` | 121 | `arguments);a.trigger("complete",arguments)}))},trigger:function(a,c){var b=this.cfg[a];b&&b.apply(document,c);("complete` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/idlemonitor.js.xhtml` | 1 | `(function(c){c.idleTimer=function(b,e,f){if("object"===typeof b){var g=b;b=null}else"number"===typeof b&&(g={timeout:b},` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/idlemonitor.js.xhtml` | 3 | `d.timeout))},n=function(){var a=c.data(e,"idleTimerObj"+f)\|\|{};a.idle=a.idleBackup;a.olddate=+new Date;a.lastActive=a.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/idlemonitor.js.xhtml` | 4 | `f)\|\|{};clearTimeout(a.tId);h.removeData("idleTimerObj"+f);h.off("._idleTimer"+f)},u=function(){var a=c.data(e,"idleTim` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/idlemonitor.js.xhtml` | 5 | `b)return u();if("getElapsedTime"===b)return+new Date-k.olddate;if("getLastActiveTime"===b)return k.lastActive;if("isIdle` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/idlemonitor.js.xhtml` | 7 | `PrimeFaces.widget.IdleMonitor=PrimeFaces.widget.BaseWidget.extend({init:function(c){this._super(c);var b=this;$(document` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/idlemonitor.js.xhtml` | 8 | `$(document).data("idleTimerObj"+this.cfg.id).lastActive);b.timer=setInterval(function(){var f=$(document).data("idleTime` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/jquery-plugins.js.xhtml` | 100 | `this.originalElement.css("margin",0);this.originalResizeStyle=this.originalElement.css("resize");this.originalElement.cs` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/jquery-plugins.js.xhtml` | 295 | `w),D[y].offset=D[y].element.offset(),z=1,D[y].options.zoomFactor&&(z=D[y].options.zoomFactor.call()),D[y].proportions({w` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/jquery.js.xhtml` | 2 | `!function(e,t){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=e.document?t(e,!0):f` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 46 | `if (map.options.zoomAnimation) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 52 | `if (this._map._proxy && this._map.options.zoomAnimation) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 65 | `zoomanim: this._animateZoom, // applys the zoom animation to the <canvas>` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 66 | `zoom: this._pinchZoom, // animate every zoom event for smoother pinch-zooming` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 67 | `zoomstart: this._zoomStart, // flag starting a zoom to disable panning` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 68 | `zoomend: this._zoomEnd,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 122 | `zoom: this._map.getZoom() - 1,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 142 | `L.DomUtil.addClass(canvas, 'leaflet-zoom-animated');` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 152 | `// update the offset so we can correct for it later when we zoom` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 155 | `if (this._zooming) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 195 | `tr.zoom = this._map.getZoom() - 1;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 198 | `// update the map constantly during a pinch zoom` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 201 | `zoom: this._map.getZoom() - 1,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 209 | `var scale = this._map.getZoomScale(e.zoom);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 214 | `var topLeft = this._map.project(e.center, e.zoom)` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 218 | `var offset = this._map.project(this._map.getBounds().getNorthWest(), e.zoom)` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 228 | `_zoomStart: function (e) {` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 229 | `this._zooming = true;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 232 | `_zoomEnd: function () {` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 242 | `this._zooming = false;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 249 | `var zoom = this._map.getZoom();` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 260 | `this._zoomEnd();` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-maplibre-gl.js.download` | 266 | `zoom: zoom - 1` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 73 | `x.ontimeout = function(evt) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 118 | `var coordinate = current - previous;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 119 | `coordinate <<= 1;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 121 | `coordinate = ~coordinate;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 124 | `while (coordinate >= 0x20) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 125 | `output += String.fromCharCode((0x20 \| (coordinate & 0x1f)) + 63);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 126 | `coordinate >>= 5;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 128 | `output += String.fromCharCode(coordinate + 63);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 133 | `* Decodes to a [latitude, longitude] coordinates array.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 147 | `coordinates = [],` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 157 | `// loop iteration, a single coordinate is decoded.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 186 | `coordinates.push([lat / factor, lng / factor]);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 189 | `return coordinates;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 193 | `* Encodes the given [latitude, longitude] coordinates array.` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 195 | `* @param {Array.<Array.<Number>>} coordinates` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 199 | `polyline.encode = function(coordinates, precision) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 200 | `if (!coordinates.length) { return ''; }` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 203 | `output = encode(coordinates[0][0], 0, factor) + encode(coordinates[0][1], 0, factor);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 205 | `for (var i = 1; i < coordinates.length; i++) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 206 | `var a = coordinates[i], b = coordinates[i - 1];` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 236 | `return polyline.encode(flipped(geojson.coordinates), precision);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 250 | `coordinates: flipped(coords)` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 11558 | `timeout: 500,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 11686 | `this.options.timeout);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 11844 | `this._map.on('zoomend', this._onZoomEnd, this);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 11854 | `map.off('zoomend', this._onZoomEnd, this);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12458 | `this.options.geocoder.reverse(wp.latLng, 67108864 /* zoom 18 */, function(rs) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12777 | `this._addRowListeners(step, r.coordinates[instr.index]);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12784 | `_addRowListeners: function(row, coordinate) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12786 | `this._marker = L.circleMarker(coordinate,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12796 | `this._map.panTo(coordinate);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12888 | `route.coordinates,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12894 | `return L.latLngBounds(this._route.coordinates);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12914 | `for (i = this._route.coordinates.length - 1; i >= 0 ; i--) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12916 | `d = latlng.distanceTo(this._route.coordinates[i]);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 12935 | `routeCoord = L.latLng(this._route.coordinates[wpIndices[i]]);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 13824 | `timeout: 30 * 1000,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 13878 | `}, this.options.timeout);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 13922 | `requiresMoreDetail: function(route, zoom, bounds) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 13970 | `coordinates: [],` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 14004 | `result.coordinates.push.apply(result.coordinates, geometry);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-routing-machine.js.download` | 14034 | `result.coordinates = this._decodePolyline(responseRoute.geometry);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 163 | `<span>Viaggio ${lap} (${count} tappe)</span></div>`;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 202 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 346 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 479 | `var zoom = hasPoint ? 15 : defaultZoom;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 496 | `zoom: zoom,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 498 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 581 | `var zoom = hasPoint ? 15 : defaultZoom;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 588 | `zoom: zoom,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 590 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 655 | `var zoom = hasPoint ? 15 : defaultZoom;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 672 | `zoom: zoom,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 674 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 740 | `var zoom = hasPoint ? 15 : defaultZoom;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 747 | `zoom: zoom,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 749 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 863 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 958 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1166 | `maxClusterRadius: enhanced ? function (zoom) {` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1167 | `if (zoom <= 7) return 24;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1168 | `if (zoom <= 11) return 16;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1169 | `if (zoom <= 15) return 10;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1587 | `zoomControl: true,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1588 | `zoomSnap: 0.5,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1589 | `zoomDelta: 0.5,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1660 | `zoomControl: true,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1662 | `zoomSnap: 0.5,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1663 | `zoomDelta: 0.5,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1741 | `zoomControl: true,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1743 | `zoomSnap: 0.5,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1744 | `zoomDelta: 0.5,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1783 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1866 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 1942 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2027 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2104 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet-scripts.js.download` | 2203 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.browser.print.js.download` | 127 | `eval("/**\r\n\tMIT License http://www.opensource.org/licenses/mit-license.php\r\n\tAuthor Igor Vladyka <igor.vladyka@gma` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.browser.print.js.download` | 138 | `eval("/**\r\n\tMIT License http://www.opensource.org/licenses/mit-license.php\r\n\tAuthor Igor Vladyka <igor.vladyka@gma` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 10 | `.leaflet-zoom-box,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 68 | `.leaflet-container.leaflet-touch-zoom {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 73 | `-ms-touch-action: pinch-zoom;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 74 | `/* Fallback for FF which doesn't support pinch-zoom */` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 76 | `touch-action: pinch-zoom;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 78 | `.leaflet-container.leaflet-touch-drag.leaflet-touch-zoom {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 95 | `.leaflet-zoom-box {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 177 | `/* zoom and fade animations */` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 188 | `.leaflet-zoom-animated {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 193 | `svg.leaflet-zoom-animated {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 197 | `.leaflet-zoom-anim .leaflet-zoom-animated {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 202 | `.leaflet-zoom-anim .leaflet-tile,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 209 | `.leaflet-zoom-anim .leaflet-zoom-hide {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 267 | `.leaflet-zoom-box {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 338 | `/* zoom control */` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 340 | `.leaflet-control-zoom-in,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 341 | `.leaflet-control-zoom-out {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 346 | `.leaflet-touch .leaflet-control-zoom-in, .leaflet-touch .leaflet-control-zoom-out  {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 549 | `-ms-zoom: 1;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.css` | 559 | `.leaflet-oldie .leaflet-control-zoom,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.js.download` | 5 | `!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?e(exports):"function"==typeof define&&define.amd?def` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/leaflet.markercluster.js.download` | 1 | `!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?t(exports):"function"==typeof define&&define.amd?def` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/main.css` | 1 | `@import url("//fonts.googleapis.com/css?family=Open+Sans:400italic,700italic,400,700");article,aside,details,figcaption,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/maplibre-gl.css` | 1 | `.maplibregl-map{-webkit-tap-highlight-color:rgb(0 0 0/0);font:12px/20px Helvetica Neue,Arial,Helvetica,sans-serif;overfl` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/maplibre-gl.js.download` | 31 | `define(["exports"],(function(t){"use strict";function e(t){return t&&t.__esModule&&Object.prototype.hasOwnProperty.call(` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/maplibre-gl.js.download` | 33 | `define(["./shared"],(function(e){"use strict";class t{constructor(e){this.keyCache={},e&&this.replace(e);}replace(e){thi` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/maplibre-gl.js.download` | 35 | `define(["./shared"],(function(t){"use strict";var e="3.2.1";class i{static testProp(t){if(!i.docStyle)return t[0];for(le` | Python Function Def | main & cantiere |
| `Pianificazione _ InTime_files/open-layers-scripts.js.download` | 120 | `// zoomMethod : null,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/open-layers-scripts.js.download` | 166 | `map.zoomToExtent(bounds);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 214 | `// It may still be an array of array of coordinates` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 241 | `// zoom change` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 316 | `// listen to zoom changes to redraw pixel-spaced patterns` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 318 | `this._map.on('zoomend', this._softRedraw, this);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 323 | `// remove optional map zoom listener` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 324 | `this._map.off('zoomend', this._softRedraw, this);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 341 | `_getCache : function(pattern, zoom, pathIndex) {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 342 | `var zoomCache = pattern.cache[zoom];` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 343 | `if (typeof zoomCache === 'undefined') {` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 344 | `pattern.cache[zoom] = [];` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 347 | `return zoomCache[pathIndex];` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 355 | `var zoom = this._map.getZoom();` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 356 | `var dirPoints = this._getCache(pattern, zoom, pathIndex);` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 388 | `pattern.cache[zoom][pathIndex] = dirPoints;` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/polyline-decoration.js.download` | 401 | `* "Soft" redraw, called internally for example on zoom changes,` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/sub-trips-map-controller.js.download` | 22 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/sub-trips-map-controller.js.download` | 172 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/sub-trips-map-controller.js.download` | 312 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/sub-trips-map-controller.js.download` | 406 | `zoomControl: true` | Logica / Config | main & cantiere |
| `Pianificazione _ InTime_files/theme.css.xhtml` | 1 | `/** jQuery UI CSS Framework 1.8.9** Copyright 2011, AUTHORS.txt (http://jqueryui.com/about)* Dual licensed under the MIT` | Logica / Config | main & cantiere |
| `ROADMAP_OTTIMIZZAZIONE_FRONTEND.md` | 58 | `*   `mappa.html` -> solo coordinate clienti.` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/01-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/02-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/03-07-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 91 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/04-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/BRESCIA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/05-06-2026/MAPPE_AUTISTI/VERONA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/09-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/10-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/11-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/12-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/16-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/17-06-2026/MAPPE_AUTISTI/Viaggio 1 Grand Chef.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/18-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/19-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/23-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/MANTOVA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/25-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/4_mappa_zone_google.html` | 42 | `${z.nome_giro} (${z.lista_punti.length} tappe)` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO GARDONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO MALCESINE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/LAGO SIRMIONE.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/26-06-2026/MAPPE_AUTISTI/VALPOLICELLA.html` | 90 | `zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true});` | Logica / Config | main & cantiere |
| `backup/storage_export/REPORTS/30-06-2026/4_mappa_zone_google.html` | 32 | `center: { lat: 45.44, lng: 11.71 }, zoom: 10` | Logica / Config | main & cantiere |

*(Mostrati primi 300 risultati su 1008 reali per questa categoria)*

## 8. Percorsi locali
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `ARCHITECTURE.md` | 1 | `# 🏛️ Blueprint Architetturale Ufficiale — AppLogSolutionsWeb` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 46 | ``ARCHITECTURE.md` è il **documento unico di riferimento tecnico (Single Source of Truth)** per la piattaforma AppLogSolu` | Tenant Setup | main & cantiere |
| `ARCHITECTURE.md` | 61 | `**AppLogSolutionsWeb** non è un semplice gestionale monolitico di bolle.` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 367 | `* **Governance Deploy**: Disciplinata nel documento vincolante [`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolut` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 472 | `* **[`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/AGENTS.md)**: **Costituzione Operativa degli Agenti` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 473 | `* **[`.agent/README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/README.md)**: Indice operativo e guid` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 474 | `* **[`.agent/workflows/workflow_automazione.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/wor` | Logica / Config | main & cantiere |
| `ARCHITECTURE.md` | 475 | `* **[`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/Gestio` | Logica / Config | main & cantiere |
| `DOMAIN_MODEL.md` | 3 | `> **Single Source of Truth del Dominio Logistico per AppLogSolutionsWeb**` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 3 | `> **Procedure Operative, Deploy, Backup e Disaster Recovery per AppLogSolutionsWeb**` | Logica / Config | main & cantiere |
| `OPERATIONS.md` | 73 | `1. Consultare la documentazione specialistica [`dr_system/MANUALE_GESTIONE_UMANA_DR.md`](file:///H:/Il%20mio%20Drive/App` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 3 | `> **Piattaforma Logistica Modulare e Multi-Committente AppLogSolutionsWeb**` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 65 | `Il documento `PROJECT_MANIFEST.md` costituisce la **Fonte Primaria (Source of Truth - Livello 0)** dell'intero progetto ` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 157 | `* **Tratta**: La filosofia fondativa, la natura immutabile dell'informazione, la centralità dell'evento logistico reale,` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 166 | `Definire il pilastro filosofico ed istituzionale su cui poggia l'intera piattaforma AppLogSolutionsWeb. Il presente capi` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 169 | `La distribuzione merci nell'ambito del trasporto merci su strada e della distribuzione capillare è stata storicamente su` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 204 | `La piattaforma non è un gestore di file o un archiviatore di documenti. **AppLogSolutionsWeb gestisce Eventi Logistici**` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 236 | `* **[`README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/README.md)**: Sezione 1 (Inquadramento generale) e ` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 237 | `* **[`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)**: Sezione 1 (Bounded Contex` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 238 | `* **[`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)**: Sezione 2 (Visione del Pr` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 241 | `* **[`.agent/workflows/workflow_automazione.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/wor` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 256 | `* **Tratta**: La ragione d'essere operativa quotidiana della piattaforma AppLogSolutionsWeb, l'impegno verso i beneficia` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 269 | `Definire l'impegno operativo quotidiano di AppLogSolutionsWeb nel trasformare le informazioni eterogenee di trasporto in` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 272 | `La distribuzione merci capillare nell'ambito del trasporto su strada si svolge in un ambiente altamente instabile, carat` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 340 | `* **[`README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/README.md)**: Sezione 1 (Inquadramento generale del` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 341 | `* **[`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)**: Sezione 1 (Bounded Contex` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 342 | `* **[`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)**: Sezione 3 (Identità Azien` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 343 | `* **[`OPERATIONS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/OPERATIONS.md)**: Sezione 2 (Procedure di Monit` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 346 | `* **[`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/Gestio` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 356 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 364 | `* **Documenti Core Collegati**: [`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/AGENTS.md), [`ARCHITECT` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 372 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 380 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 388 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 396 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 397 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLo` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 404 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 412 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 420 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 428 | `* **Documenti Core Collegati**: [`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/AGENTS.md), [`ARCHITECT` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 436 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 437 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/workflow_automazione.md`](file:///H:/Il%20mio%20Drive/App/Ap` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 444 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 445 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/workflow_automazione.md`](file:///H:/Il%20mio%20Drive/App/Ap` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 452 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 460 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 461 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/workflow_automazione.md`](file:///H:/Il%20mio%20Drive/App/Ap` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 468 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 476 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 484 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 492 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 500 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 501 | `* **Documenti Specialistici Collegati**: [`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLo` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 508 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 516 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 524 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 532 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 540 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 548 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md),` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 556 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 564 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 572 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 580 | `* **Documenti Core Collegati**: [`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/AGENTS.md), [`ARCHITECT` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 588 | `* **Documenti Core Collegati**: [`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 604 | `* **Documenti Core Collegati**: [`README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/README.md)` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 612 | `* **Documenti Core Collegati**: [`README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/README.md), [`OPERATION` | Logica / Config | main & cantiere |
| `PROJECT_MANIFEST.md` | 620 | `* **Documenti Core Collegati**: [`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)` | Logica / Config | main & cantiere |
| `README.md` | 1 | `# 🚀 AppLogSolutionsWeb v3.00 — Piattaforma Logistica Modulare Dual Mode` | Logica / Config | main & cantiere |
| `README.md` | 4 | `> **Repository Root**: `AppLogSolutionsWeb`` | Logica / Config | main & cantiere |
| `README.md` | 36 | `1. **[`README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/README.md)**: Porta d'ingresso e guida al Bootstra` | Logica / Config | main & cantiere |
| `README.md` | 37 | `2. **[`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/AGENTS.md)**: Costituzione Operativa Vincolante (G` | Logica / Config | main & cantiere |
| `README.md` | 38 | `3. **[`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)**: Modello di Dominio DDD e` | Tenant Setup | main & cantiere |
| `README.md` | 39 | `4. **[`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)**: Blueprint Architetturale` | Tenant Setup | main & cantiere |
| `README.md` | 40 | `5. **[`OPERATIONS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/OPERATIONS.md)**: Procedure Operative, Backup,` | Logica / Config | main & cantiere |
| `README.md` | 45 | `* [`frontend/docs/design-system.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/frontend/docs/design-system.md) ` | Logica / Config | main & cantiere |
| `README.md` | 46 | `* [`frontend/docs/differenze_modali.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/frontend/docs/differenze_mod` | Logica / Config | main & cantiere |
| `README.md` | 48 | `* [`.agent/workflows/workflow_automazione.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/workf` | Logica / Config | main & cantiere |
| `README.md` | 49 | `* [`.agent/workflows/Gestione CONSEGNE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/.agent/workflows/Gestione` | Logica / Config | main & cantiere |
| `README.md` | 51 | `* [`dr_system/README_DR_AUTONOMO.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/dr_system/README_DR_AUTONOMO.md` | Logica / Config | main & cantiere |
| `README.md` | 52 | `* [`dr_system/MANUALE_GESTIONE_UMANA_DR.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/dr_system/MANUALE_GESTIO` | Logica / Config | main & cantiere |
| `README.md` | 61 | `* **PRODUZIONE**: `log-solution-60007` (Consultare la sezione 13 di [`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLog` | Logica / Config | main & cantiere |
| `README.md` | 70 | `1. **[`README.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/README.md)** (Porta d'ingresso & Bootstrap Roadmap` | Logica / Config | main & cantiere |
| `README.md` | 71 | `2. **[`AGENTS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/AGENTS.md)** (Costituzione Operativa, Safety & Dep` | Logica / Config | main & cantiere |
| `README.md` | 72 | `3. **[`DOMAIN_MODEL.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/DOMAIN_MODEL.md)** (Linguaggio Ubiquo DDD & ` | Logica / Config | main & cantiere |
| `README.md` | 73 | `4. **[`ARCHITECTURE.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/ARCHITECTURE.md)** (Blueprint Architetturale` | Logica / Config | main & cantiere |
| `README.md` | 74 | `5. **[`OPERATIONS.md`](file:///H:/Il%20mio%20Drive/App/AppLogSolutionsWeb/OPERATIONS.md)** (Procedure Operative & DR)` | Logica / Config | main & cantiere |
| `check_cantiere_offline2.py` | 4 | `cred = credentials.Certificate("h:/Il mio Drive/App/AppLogSolutionsWeb/cantiere_key.json")` | Logica / Config | cantiere |
| `check_navette_prod.py` | 26 | `with open('C:\\Users\\Diego\\.gemini\\antigravity\\brain\\781e2882-d49e-4511-a802-d8295dbfdf99\\navette_luglio_produzion` | Logica / Config | main & cantiere |
| `cleanup_apps.py` | 4 | `FRONTEND = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"` | Logica / Config | main & cantiere |
| `cleanup_duplicates.py` | 4 | `FRONTEND = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"` | Logica / Config | main & cantiere |
| `deep_audit_25_07.py` | 223 | `brain_dir = pathlib.Path(r"C:\Users\39349\.gemini\antigravity\brain\2e582344-db76-4115-8e4e-627b211c5d26")` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 1 | `cd "H:\Il mio Drive\App\AppLogSolutionsWeb"` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 4 | `& "C:\Users\39349\AppData\Local\Programs\Python\Python314\python.exe" -m py_compile functions\main.py` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 11 | `& "C:\Users\39349\AppData\Local\Programs\Python\Python314\python.exe" test_cattel_parser.py` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 16 | `& "C:\Users\39349\AppData\Local\Programs\Python\Python314\python.exe" functions\test_preflight.py` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 24 | `$env:PATH = "H:\Il mio Drive\App\AppLogSolutionsWeb\functions\venv\Scripts;C:\Users\39349\AppData\Local\Programs\cursor\` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 27 | `$env:GOOGLE_APPLICATION_CREDENTIALS = "H:\Il mio Drive\App\AppLogSolutionsWeb\dev_key.json"` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 30 | `& "C:\Users\39349\AppData\Local\npm-cache\_npx\7750544ccf494d8b\node_modules\.bin\firebase.cmd" --version` | Logica / Config | main & cantiere |
| `deploy_dev.ps1` | 36 | `& "C:\Users\39349\AppData\Local\npm-cache\_npx\7750544ccf494d8b\node_modules\.bin\firebase.cmd" deploy `` | Logica / Config | main & cantiere |
| `dr_system/MANUALE_GESTIONE_UMANA_DR.md` | 26 | `Il sistema risiede interamente all'interno della cartella `G:\\Il mio Drive\\App\\AppLogSolutionsWeb\\dr\_system\\`.` | Logica / Config | main & cantiere |
| `dr_system/MANUALE_GESTIONE_UMANA_DR.md` | 33 | `1. Apri il terminale del PC all'interno della cartella del progetto web (`AppLogSolutionsWeb`).` | Logica / Config | main & cantiere |
| `dr_system/README_DR_AUTONOMO.md` | 3 | `Questo modulo contiene l'infrastruttura di grado Enterprise per il Disaster Recovery automatizzato e auto-certificante d` | Logica / Config | main & cantiere |
| `dr_system/dr_orchestrator.py` | 11 | `# Motore Automatico End-to-End per AppLogSolutionsWeb` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 1 | `2026/07/24-16:38:59.351 71d8 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 3 | `2026/07/24-16:38:59.793 71d8 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG.old` | 1 | `2026/07/24-16:38:44.105 1284 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\Defau` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG.old` | 2 | `2026/07/24-16:38:44.804 1284 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Local Storage/leveldb/LOG` | 1 | `2026/07/24-16:39:01.863 e78 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Local Storage/leveldb/LOG` | 3 | `2026/07/24-16:39:01.896 e78 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\De` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Local Storage/leveldb/LOG.old` | 1 | `2026/07/24-16:38:56.849 804c Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Local Storage/leveldb/LOG.old` | 3 | `2026/07/24-16:38:56.885 804c Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Service Worker/Database/LOG` | 1 | `2026/07/24-16:39:01.863 8a64 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Service Worker/Database/LOG` | 3 | `2026/07/24-16:39:01.896 8a64 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Service Worker/Database/LOG.old` | 1 | `2026/07/24-16:38:56.863 608 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Service Worker/Database/LOG.old` | 3 | `2026/07/24-16:38:56.885 608 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\De` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Session Storage/LOG` | 1 | `2026/07/24-16:39:02.796 8a64 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Session Storage/LOG` | 3 | `2026/07/24-16:39:02.811 8a64 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Session Storage/LOG.old` | 1 | `2026/07/24-16:38:57.824 1b0 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/Session Storage/LOG.old` | 3 | `2026/07/24-16:38:57.841 1b0 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\De` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/LOG` | 1 | `2026/07/24-16:39:02.490 7750 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/LOG` | 3 | `2026/07/24-16:39:02.509 7750 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/LOG.old` | 1 | `2026/07/24-16:38:57.112 4814 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/LOG.old` | 3 | `2026/07/24-16:38:57.127 4814 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/metadata/LOG` | 1 | `2026/07/24-16:39:01.965 7750 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/metadata/LOG` | 3 | `2026/07/24-16:39:01.988 7750 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/metadata/LOG.old` | 1 | `2026/07/24-16:38:56.913 4814 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_auth_profile/Default/shared_proto_db/metadata/LOG.old` | 3 | `2026/07/24-16:38:56.933 4814 Reusing old log G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_auth_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 1 | `2026/07/24-15:45:18.683 6f3c Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 2 | `2026/07/24-15:45:19.578 6f3c Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/Local Storage/leveldb/LOG` | 1 | `2026/07/24-15:45:11.473 6f3c Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/Local Storage/leveldb/LOG` | 2 | `2026/07/24-15:45:12.630 6f3c Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/Service Worker/Database/LOG` | 1 | `2026/07/24-15:45:18.924 8928 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/Service Worker/Database/LOG` | 2 | `2026/07/24-15:45:19.666 8928 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/Session Storage/LOG` | 1 | `2026/07/24-15:45:14.637 8928 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/Session Storage/LOG` | 2 | `2026/07/24-15:45:15.082 8928 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/shared_proto_db/LOG` | 1 | `2026/07/24-15:45:12.956 128c Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/shared_proto_db/LOG` | 2 | `2026/07/24-15:45:13.536 128c Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/shared_proto_db/metadata/LOG` | 1 | `2026/07/24-15:45:11.731 128c Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\Defaul` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_pwa_profile/Default/shared_proto_db/metadata/LOG` | 2 | `2026/07/24-15:45:12.728 128c Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_pwa_profile\D` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 1 | `2026/07/25-10:40:28.306 4544 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/IndexedDB/https_log-solutions-sviluppo.web.app_0.indexeddb.leveldb/LOG` | 2 | `2026/07/25-10:40:28.703 4544 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/Local Storage/leveldb/LOG` | 1 | `2026/07/25-10:40:23.304 2f84 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/Local Storage/leveldb/LOG` | 2 | `2026/07/25-10:40:24.309 2f84 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/Service Worker/Database/LOG` | 1 | `2026/07/25-10:40:28.345 3364 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/Service Worker/Database/LOG` | 2 | `2026/07/25-10:40:28.707 3364 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/Session Storage/LOG` | 1 | `2026/07/25-10:40:26.262 3364 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/Session Storage/LOG` | 2 | `2026/07/25-10:40:26.594 3364 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/shared_proto_db/LOG` | 1 | `2026/07/25-10:40:24.665 3364 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/shared_proto_db/LOG` | 2 | `2026/07/25-10:40:25.161 3364 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/shared_proto_db/metadata/LOG` | 1 | `2026/07/25-10:40:23.578 3364 Creating DB G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profile_v2\` | Logica / Config | main & cantiere |
| `e2e-tests/.playwright_test10_profile_v2/Default/shared_proto_db/metadata/LOG` | 2 | `2026/07/25-10:40:24.407 3364 Reusing MANIFEST G:\Il mio Drive\App\AppLogSolutionsWeb\e2e-tests\.playwright_test10_profil` | Logica / Config | main & cantiere |
| `fix_app_import.py` | 4 | `FRONTEND = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"` | Logica / Config | main & cantiere |
| `fix_db_import.py` | 10 | `FRONTEND = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"` | Logica / Config | main & cantiere |
| `fix_firestore_service.py` | 4 | `filepath = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\firestore-service.js"` | Logica / Config | main & cantiere |
| `fix_services.py` | 4 | `SERVICES_DIR = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend\services"` | Logica / Config | main & cantiere |
| `format_july.py` | 20 | `with open('C:\\Users\\Diego\\.gemini\\antigravity\\brain\\781e2882-d49e-4511-a802-d8295dbfdf99\\dati_luglio_2026.md', 'w` | Logica / Config | main & cantiere |
| `frontend/fix_snapshot.py` | 4 | `directory = "G:/Il mio Drive/App/AppLogSolutionsWeb/frontend"` | Logica / Config | main & cantiere |
| `frontend/mappa_zone.html` | 6 | `<title>Mappa Zone Interattiva - AppLogSolutionsWeb</title>` | Logica / Config | main & cantiere |
| `frontend/update_version.py` | 8 | `frontend_dir = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"` | Logica / Config | main & cantiere |
| `functions/delete_anomalies.py` | 34 | `check_env("SVILUPPO", "G:/Il mio Drive/App/AppLogSolutionsWeb/dev_key.json")` | Logica / Config | main & cantiere |
| `functions/delete_anomalies.py` | 35 | `check_env("PROD", r"C:\Users\Diego\Documents\antigravity\elegant-goodall\log-solution-60007-firebase-adminsdk-h4g9o-c46f` | Logica / Config | main & cantiere |
| `functions/migrate_navette.py` | 4 | `cred = credentials.Certificate(r"G:\Il mio Drive\App\AppLogSolutionsWeb\dev_key.json")` | Logica / Config | main & cantiere |
| `get_july_prod.py` | 20 | `with open('C:\\Users\\Diego\\.gemini\\antigravity\\brain\\781e2882-d49e-4511-a802-d8295dbfdf99\\presenze_luglio_produzio` | Logica / Config | main & cantiere |
| `run_audit_post.py` | 223 | `brain_dir = pathlib.Path(r"C:\Users\39349\.gemini\antigravity\brain\2e582344-db76-4115-8e4e-627b211c5d26")` | Logica / Config | main & cantiere |
| `scripts/gen_report_navette.py` | 73 | `with open(r'C:\Users\39349\.gemini\antigravity\brain\0d96d8cf-9921-42ad-bb82-412b4f04601a\report_navette_clienti.md', 'w` | Logica / Config | main & cantiere |
| `temp_append.py` | 122 | `with open(r'h:\Il mio Drive\App\AppLogSolutionsWeb\functions\main.py', 'a', encoding='utf-8') as f:` | Logica / Config | main & cantiere |
| `test_pattern.py` | 3 | `FRONTEND = r"G:\Il mio Drive\App\AppLogSolutionsWeb\frontend"` | Logica / Config | main & cantiere |
| `upload_mezzi.py` | 9 | `cred = credentials.Certificate(r"G:\Il mio Drive\App\AppLogSolutionsWeb\dev_key.json")` | Logica / Config | main & cantiere |
| `upload_mezzi.py` | 21 | `r"G:\Il mio Drive\App\AUTOMEZZI LEASING ESGrent",` | Logica / Config | main & cantiere |
| `upload_mezzi.py` | 22 | `r"G:\Il mio Drive\App\AUTOMEZZI LOG. SOLUTIONS"` | Logica / Config | main & cantiere |

## 9. Cache e versioni
| File | Riga | Contenuto (stralcio) | Funzione/Sezione | Branch |
|------|------|----------------------|------------------|--------|
| `Pianificazione _ InTime_files/chartjs.js.xhtml` | 13 | `*/function bt(t){return t+.5\|0}const xt=(t,e,i)=>Math.max(Math.min(t,i),e);function _t(t){return xt(bt(2.55*t),0,255)}f` | JS Function | main & cantiere |
| `Pianificazione _ InTime_files/jquery-plugins.js.xhtml` | 280 | `v){v?u.selectionEnd=u.selectionStart:u.selectionStart=u.selectionEnd};else if(w(R,"createTextRange")&&z(document,"select` | Logica / Config | main & cantiere |
| `ROADMAP_OTTIMIZZAZIONE_FRONTEND.md` | 36 | `- [x] **Cache Busting (`?v=6.039`)**: Per forzare i Service Worker e i browser a caricare i nuovi moduli.` | Logica / Config | main & cantiere |
| `bump_version.py` | 9 | `match = re.search(r'APP_VERSION\s*=\s*"([\d\.]+)"', c_script)` | Logica / Config | main & cantiere |
| `bump_version.py` | 38 | `c_script = re.sub(r'APP_VERSION\s*=\s*"[\d\.]+"', f'APP_VERSION = "{v_new}"', c_script)` | Logica / Config | main & cantiere |
| `bump_version.py` | 53 | `c_h = re.sub(r'\?v=[\d\.]+', f'?v={v_new}', c_h)` | Logica / Config | main & cantiere |
| `bump_version.py` | 68 | `c_js = re.sub(r'\?v=[\d\.]+', f'?v={v_new}', c_js)` | Logica / Config | main & cantiere |
| `e2e-tests/scripts/test10-continuity.js` | 29 | `body = body.replace(/const CACHE_NAME = "[^"]+";/, 'const CACHE_NAME = "log-solution-v6.258-ROTTA";');` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/login.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.037">` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/login.html` | 53 | `<script src="script.js?v=6.037"></script>` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/login.html` | 54 | `<script type="module" src="firebase-auth-sync.js?v=6.037"></script>` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 7 | `const APP_VERSION = "6.037";` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 10 | `window.APP_VERSION = APP_VERSION;` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 11 | `console.log("%c[App] Log Solution PWA - versione " + APP_VERSION, "color: #4f46e5; font-weight: bold; font-size: 12px;")` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 24 | `release: "log-solution-pwa@" + APP_VERSION,` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 447 | `el.textContent = 'v' + APP_VERSION;` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/script.js` | 587 | `console.log('[SW] Registrato correttamente sw.js con versione ' + APP_VERSION);` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 1 | `const CACHE_NAME = 'log-solution-v6.037';` | Variable Assignment | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 22 | `console.log(`[SW ${CACHE_NAME}] Installazione cache...`);` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 24 | `caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 31 | `console.log(`[SW ${CACHE_NAME}] Attivazione: pulizia cache vecchie...`);` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 36 | `if (name !== CACHE_NAME) {` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 49 | `console.log(`[SW ${CACHE_NAME}] SKIP_WAITING ricevuto ï¿½ attivazione forzata.`);` | Logica / Config | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 84 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 98 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/backup-pre-fase1/sw.js` | 116 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/centrale_resi.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 197 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/centrale_resi.html` | 198 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/centro_costi.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/centro_costi.html` | 243 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/centro_costi.html` | 244 | `<script src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/dashboard.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/dashboard.html` | 168 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/dashboard.html` | 169 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/elaborazione.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/elaborazione.html` | 376 | `<script src="script.js?v=6.356"></script>` | Logica / Config | main |
| `frontend/elaborazione.html` | 377 | `<script type="module" src="firebase-auth-sync.js?v=6.356"></script>` | Logica / Config | main |
| `frontend/elaborazione.html` | 399 | `<script src="script.js?v=6.389"></script>` | Logica / Config | cantiere |
| `frontend/elaborazione.html` | 400 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | cantiere |
| `frontend/fatturazione.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/fatturazione.html` | 313 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/fatturazione.html` | 314 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/fatturazione_clienti.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/fatturazione_clienti.html` | 988 | `<script type="module" src="firebase-auth-sync.js?v=6.356"></script>` | Logica / Config | main |
| `frontend/fatturazione_clienti.html` | 1098 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | cantiere |
| `frontend/fatturazione_v2.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 141 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 142 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 1320 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/fatturazione_v2.html` | 1321 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/gestione.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/gestione.html` | 365 | `<script src="script.js?v=6.356"></script>` | Logica / Config | main |
| `frontend/gestione.html` | 366 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/gestione.html` | 367 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | cantiere |
| `frontend/gestione_anomalie.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/gestione_anomalie.html` | 103 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/gestione_anomalie.html` | 104 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/gestione_articoli.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/gestione_mezzi.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/gestione_mezzi.html` | 426 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/gestione_mezzi.html` | 427 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/gestione_nuovi_clienti.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/gestione_orari.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/gestione_rientri.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/impostazioni.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/impostazioni.html` | 1433 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/impostazioni.html` | 1434 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/impostazioni.html` | 2465 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/impostazioni.html` | 2466 | `const { syncManager } = await import("./core/sync-manager.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/inserimento.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/inserimento.html` | 480 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/inserimento.html` | 481 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/inserimento.html` | 483 | `import { saveTrip, checkPendingTrip, closeTripWithAnomaly, deleteTrip } from "./firestore-service.js?v=6.389";` | Logica / Config | main & cantiere |
| `frontend/inserimento.html` | 484 | `import { auth } from "./firestore-service.js?v=6.389";` | Logica / Config | main & cantiere |
| `frontend/inserimento.html` | 485 | `import "./gps-tracker.js?v=6.389";` | Logica / Config | main & cantiere |
| `frontend/inserimento.html` | 885 | `const { syncManager } = await import("./core/sync-manager.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/link_viaggi.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/link_viaggi.html` | 213 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/link_viaggi.html` | 214 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/login.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/login.html` | 53 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/login.html` | 54 | `<script type="module" src="core/firebase-init.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/login.html` | 55 | `<script type="module" src="core/auth-service.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/mappa_consegne.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/mappa_consegne.html` | 189 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/mappa_consegne.html` | 190 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/mappa_riepilogativa.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/mappa_riepilogativa.html` | 319 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/mappa_riepilogativa.html` | 320 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/mappa_zone.html` | 9 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/mappa_zone.html` | 1589 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/mappa_zone.html` | 1590 | `const { syncManager } = await import("./core/sync-manager.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/mappa_zone.html` | 3459 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.356");` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 3610 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.389");` | Variable Assignment | cantiere |
| `frontend/mappa_zone.html` | 3839 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.356");` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 3919 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.356");` | Variable Assignment | main |
| `frontend/mappa_zone.html` | 3990 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.389");` | Variable Assignment | cantiere |
| `frontend/mappa_zone.html` | 4070 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.389");` | Variable Assignment | cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_2_Zone_GranChef_V02_19-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V01%202%202_Zone_GranChef_V02.pdf?v=1781793324" target="_blank" style="background:` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_Zone_GranChef_V01_01-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V01%202_Zone_GranChef_V01.pdf?v=1781703275" target="_blank" style="background: #02` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_2_Zone_GranChef_V01_GranChef_V02_19-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V01%202_Zone_GranChef_V01_GranChef_V02.pdf?v=1781793324" target="_blank" style="ba` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_01-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V01_Zone_GranChef_V01.pdf?v=1781761730" target="_blank" style="background: #0284c7` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_17-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V01_Zone_GranChef_V01.pdf?v=1781676419" target="_blank" style="background: #0284c7` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V01_Zone_GranChef_V01_19-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V01_Zone_GranChef_V01.pdf?v=1781793323" target="_blank" style="background: #0284c7` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/GranChef_V02_Zone_GranChef_V02_19-06-2026.html` | 98 | `<a href="distinte/DISTINTA_GranChef%20V02_Zone_GranChef_V02.pdf?v=1781793323" target="_blank" style="background: #0284c7` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Lago_Gardone_Zone_GranChef_V01_23-06-2026.html` | 98 | `<a href="distinte/DISTINTA_Lago%20Gardone_Zone_GranChef_V01.pdf?v=1782143982" target="_blank" style="background: #0284c7` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Lago_Malcesine_Zone_GranChef_V02_23-06-2026.html` | 98 | `<a href="distinte/DISTINTA_Lago%20Malcesine_Zone_GranChef_V02.pdf?v=1782143982" target="_blank" style="background: #0284` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Lago_Sirmione_Zone_GranChef_V01_23-06-2026.html` | 98 | `<a href="distinte/DISTINTA_Lago%20Sirmione_Zone_GranChef_V01.pdf?v=1782143982" target="_blank" style="background: #0284c` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Mantova_Zone_GranChef_V02_23-06-2026.html` | 98 | `<a href="distinte/DISTINTA_Mantova_Zone_GranChef_V02.pdf?v=1782143983" target="_blank" style="background: #0284c7; color` | Logica / Config | main & cantiere |
| `frontend/mappe_autisti/Valpolicella_Zone_GranChef_V02_23-06-2026.html` | 98 | `<a href="distinte/DISTINTA_Valpolicella_Zone_GranChef_V02.pdf?v=1782143982" target="_blank" style="background: #0284c7; ` | Logica / Config | main & cantiere |
| `frontend/pianificazione.html` | 7 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/pianificazione.html` | 1309 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/pianificazione.html` | 1310 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/presenze.html` | 19 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/presenze.html` | 590 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/presenze.html` | 591 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/presenze.html` | 596 | `import { calculateHours } from "./firestore-service.js?v=6.389";` | Logica / Config | main & cantiere |
| `frontend/presenze.html` | 1910 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/presenze.html` | 1978 | `const { syncManager } = await import("./core/sync-manager.js?v=6.389");` | Variable Assignment | main & cantiere |
| `frontend/presenze.html` | 2744 | `<script type="module" src="cedolini-splitter.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/report-post-fase2/lista-moduli.txt` | 13 | `- firebase-auth-sync.js : Importa in sequenza i 4 file sopra con cache buster (?v=6.039). Mantenuto per compatibilità as` | Logica / Config | main & cantiere |
| `frontend/script.js` | 7 | `const APP_VERSION = "6.389";` | Variable Assignment | main & cantiere |
| `frontend/script.js` | 10 | `window.APP_VERSION = APP_VERSION;` | Logica / Config | main & cantiere |
| `frontend/script.js` | 11 | `console.log("%c[App] Log Solution PWA - versione " + APP_VERSION, "color: #4f46e5; font-weight: bold; font-size: 12px;")` | Logica / Config | main & cantiere |
| `frontend/script.js` | 24 | `release: "log-solution-pwa@" + APP_VERSION,` | Logica / Config | main & cantiere |
| `frontend/script.js` | 447 | `el.textContent = 'v' + APP_VERSION;` | Logica / Config | main |
| `frontend/script.js` | 456 | `el.textContent = 'v' + APP_VERSION;` | Logica / Config | cantiere |
| `frontend/script.js` | 597 | `console.log('[SW] Registrato correttamente sw.js con versione ' + APP_VERSION);` | Logica / Config | main |
| `frontend/script.js` | 606 | `console.log('[SW] Registrato correttamente sw.js con versione ' + APP_VERSION);` | Logica / Config | cantiere |
| `frontend/sw.js` | 1 | `const CACHE_NAME = 'log-solution-v6.389';` | Variable Assignment | main & cantiere |
| `frontend/sw.js` | 64 | `console.log(`[SW ${CACHE_NAME}] Installazione cache...`);` | Logica / Config | main & cantiere |
| `frontend/sw.js` | 66 | `caches.open(CACHE_NAME).then(async (cache) => {` | JS Function | main & cantiere |
| `frontend/sw.js` | 147 | `console.log(`[SW ${CACHE_NAME}] Attivazione: pulizia cache vecchie...`);` | Logica / Config | main & cantiere |
| `frontend/sw.js` | 152 | `if (name.startsWith('log-solution-') && name !== CACHE_NAME) {` | Logica / Config | main & cantiere |
| `frontend/sw.js` | 165 | `console.log(`[SW ${CACHE_NAME}] SKIP_WAITING ricevuto ï¿½ attivazione forzata.`);` | Logica / Config | main & cantiere |
| `frontend/sw.js` | 201 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/sw.js` | 238 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/sw.js` | 259 | `caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));` | JS Function | main & cantiere |
| `frontend/update_version.py` | 14 | `new_content = re.sub(r'\?v=\d+\.\d+', f'?v={NEW_VERSION}', content)` | Logica / Config | main & cantiere |
| `frontend/update_version.py` | 24 | `new_content = re.sub(r'const APP_VERSION = ".*?";', f'const APP_VERSION = "{NEW_VERSION}";', content)` | Variable Assignment | main & cantiere |
| `frontend/update_version.py` | 34 | `new_content = re.sub(r"const CACHE_NAME = 'log-solution-v.*?';", f"const CACHE_NAME = 'log-solution-v{NEW_VERSION}';", c` | Variable Assignment | main & cantiere |
| `frontend/visualizzazione.html` | 8 | `<link rel="stylesheet" href="styles.css?v=6.389">` | Logica / Config | main & cantiere |
| `frontend/visualizzazione.html` | 240 | `<script src="script.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/visualizzazione.html` | 242 | `<script type="module" src="firebase-auth-sync.js?v=6.389"></script>` | Logica / Config | main & cantiere |
| `frontend/visualizzazione.html` | 245 | `import { getAllTrips, getTripLogs, deleteTrip } from "./firestore-service.js?v=6.389";` | Logica / Config | main & cantiere |
| `frontend/visualizzazione.html` | 246 | `import { renderTripList, removeTripCard } from "./ui-render.js?v=6.389";` | Logica / Config | main & cantiere |
| `temp_script.js` | 4 | `import { calculateHours } from "./firestore-service.js?v=6.293";` | Logica / Config | main & cantiere |
| `temp_script.js` | 1317 | `const { connectivityService } = await import("./core/connectivity-service.js?v=6.293");` | Variable Assignment | main & cantiere |
| `temp_script.js` | 1378 | `const { syncManager } = await import("./core/sync-manager.js?v=6.293");` | Variable Assignment | main & cantiere |

## 10. Confronto Branch (Cantiere vs Main)
| File | Riga | Valore in Cantiere | Valore in Main | Note |
|------|------|--------------------|----------------|------|
| `.firebaserc` | 4 | `"cantiere": "log-solutions-cantiere"` | `(assente)` | Divergenza | 
| `ARCHITECTURE.md` | 181 | `* **Inizializzazione**: `frontend/core/firebase-in` | `* **Inizializzazione**: `frontend/core/firebase-in` | Divergenza | 
| `ARCHITECTURE.md` | 350 | `Storage Bucket (log-solutions-cantiere / log-solut` | `Storage Bucket (log-solutions-sviluppo / log-solut` | Divergenza | 
| `ARCHITECTURE.md` | 365 | `* **Ambiente Sviluppo**: `log-solutions-cantiere`` | `(assente)` | Divergenza | 
| `check_cantiere.py` | 4 | `os.environ["GCLOUD_PROJECT"] = "log-solutions-cant` | `(assente)` | Divergenza | 
| `check_cantiere.py` | 18 | `bucket = storage.bucket("log-solutions-cantiere.ap` | `(assente)` | Divergenza | 
| `check_cantiere_offline.py` | 2 | `os.environ["GCLOUD_PROJECT"] = "log-solutions-cant` | `(assente)` | Divergenza | 
| `check_cantiere_offline.py` | 10 | `bucket = storage.bucket("log-solutions-cantiere.ap` | `(assente)` | Divergenza | 
| `check_cantiere_offline2.py` | 7 | `'storageBucket': 'log-solutions-cantiere.appspot.c` | `(assente)` | Divergenza | 
| `check_deliveries.py` | 4 | `db = firestore.Client(project="log-solutions-canti` | `(assente)` | Divergenza | 
| `frontend/elaborazione.html` | 414 | `const functions = getFunctions(app, "europe-west1"` | `(assente)` | Divergenza | 
| `frontend/firebase-config.js` | 15 | `authDomain: "log-solutions-cantiere.firebaseapp.co` | `authDomain: "log-solutions-sviluppo.web.app",` | Divergenza | 
| `frontend/firebase-config.js` | 16 | `projectId: "log-solutions-cantiere",` | `(assente)` | Divergenza | 
| `frontend/firebase-config.js` | 17 | `storageBucket: "log-solutions-cantiere.firebasesto` | `storageBucket: "log-solutions-sviluppo.firebasesto` | Divergenza | 
| `frontend/firebase-config.js` | 24 | `const isDevEnvironment = window.location.hostname.` | `(assente)` | Divergenza | 
| `frontend/firebase-config.js` | 26 | `window.location.hostname === 'localhost' \|\|` | `window.location.hostname === '127.0.0.1';` | Divergenza | 
| `frontend/firebase-config.js` | 27 | `window.location.hostname === '127.0.0.1';` | `(assente)` | Divergenza | 
| `frontend/firebase-config.js` | 32 | `console.log("[Firebase Config] ATTENZIONE: Conness` | `(assente)` | Divergenza | 
| `frontend/firebase-config.js` | 34 | `console.log("[Firebase Config] Connesso alla PRODU` | `(assente)` | Divergenza | 
| `frontend/mappa_zone.html` | 4017 | `const functions = getFunctions(app, "europe-west1"` | `(assente)` | Divergenza | 
| `frontend/script.js` | 33 | `// Attivazione su localhost, cantiere o test` | `if (hostname.includes('log-solutions-sviluppo') \|` | Divergenza | 
| `frontend/script.js` | 34 | `if (hostname.includes('cantiere') \|\| hostname.in` | `(assente)` | Divergenza | 
| `functions/infrastructure/firebase_setup.py` | 28 | `if PROJECT_ID == "log-solutions-cantiere":` | `(assente)` | Divergenza | 
| `functions/infrastructure/firebase_setup.py` | 29 | `BUCKET_NAME = "log-solutions-cantiere.firebasestor` | `BUCKET_NAME = "log-solutions-sviluppo.firebasestor` | Divergenza | 
| `functions/main.py` | 1466 | `const url = `https://europe-west1-{PROJECT_ID}.clo` | `(assente)` | Divergenza | 
| `functions/main.py` | 1556 | `const url = `https://europe-west1-{PROJECT_ID}.clo` | `(assente)` | Divergenza | 
| `functions/main.py` | 1667 | `const resp = await fetch("https://europe-west1-log` | `(assente)` | Divergenza | 
| `functions/main.py` | 4853 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4868 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4880 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4885 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4890 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4895 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4900 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4909 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4917 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4952 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4957 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 4962 | `@https_fn.on_call(region="europe-west1", memory=op` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4967 | `@https_fn.on_call(region="europe-west1", memory=op` | `Rileva quali blocchi hanno nuovi dati in split_ddt` | Divergenza | 
| `functions/main.py` | 4985 | `@https_fn.on_call(region="europe-west1", memory=op` | `# Controlliamo CATTEL` | Divergenza | 
| `functions/main.py` | 5141 | `@https_fn.on_call(region="europe-west1", memory=op` | `viaggi_ref = db.collection('clienti').document('DN` | Divergenza | 
| `functions/main.py` | 5230 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 5249 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 5342 | `@https_fn.on_call(region="europe-west1", memory=op` | `# Elimina da viaggi ddt` | Divergenza | 
| `functions/main.py` | 5405 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 5522 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 5604 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 5725 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 5833 | `@https_fn.on_request(region="europe-west1", memory` | `(assente)` | Divergenza | 
| `functions/main.py` | 5928 | `@https_fn.on_request(region="europe-west1", memory` | `(assente)` | Divergenza | 
| `functions/main.py` | 5981 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `functions/main.py` | 6147 | `@https_fn.on_call(region="europe-west1", memory=op` | `(assente)` | Divergenza | 
| `frontend/elaborazione.html` | 391 | `(assente)` | `const functions = getFunctions(app, "europe-west1"` | Divergenza | 
| `frontend/firebase-config.js` | 25 | `(assente)` | `window.location.hostname === 'localhost' \|\|` | Divergenza | 
| `frontend/firebase-config.js` | 33 | `(assente)` | `console.log("[Firebase Config] Connesso alla PRODU` | Divergenza | 
| `frontend/mappa_zone.html` | 3866 | `(assente)` | `const functions = getFunctions(app, "europe-west1"` | Divergenza | 
| `functions/main.py` | 1456 | `(assente)` | `const url = `https://europe-west1-{PROJECT_ID}.clo` | Divergenza | 
| `functions/main.py` | 1546 | `(assente)` | `const url = `https://europe-west1-{PROJECT_ID}.clo` | Divergenza | 
| `functions/main.py` | 1657 | `(assente)` | `const resp = await fetch("https://europe-west1-log` | Divergenza | 
| `functions/main.py` | 4567 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4582 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4594 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4599 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4604 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4609 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4614 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4623 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4631 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4666 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4671 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4676 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4681 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4699 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4855 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 4944 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5060 | `for tenant in ["DNR", "CATTEL", "GRAN CHEF", "BAUE` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5123 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5240 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5322 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5443 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5551 | `(assente)` | `@https_fn.on_request(region="europe-west1", memory` | Divergenza | 
| `functions/main.py` | 5646 | `(assente)` | `@https_fn.on_request(region="europe-west1", memory` | Divergenza | 
| `functions/main.py` | 5699 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `functions/main.py` | 5865 | `(assente)` | `@https_fn.on_call(region="europe-west1", memory=op` | Divergenza | 
| `check_cantiere.py` | 24 | `jobs_ref = db.collection('clienti').document('DNR'` | `(assente)` | Divergenza | 
| `check_cantiere_offline.py` | 15 | `jobs_ref = db.collection('clienti').document('DNR'` | `(assente)` | Divergenza | 
| `check_cantiere_offline2.py` | 15 | `jobs_ref = db.collection('clienti').document('DNR'` | `(assente)` | Divergenza | 
| `check_cantiere_offline2.py` | 69 | `if etichetta == 'CATTEL':` | `(assente)` | Divergenza | 
| `check_cantiere_offline2.py` | 71 | `if etichetta == 'GRAND_CHEF':` | `(assente)` | Divergenza | 
| `check_deliveries.py` | 5 | `doc = db.collection("clienti").document("DAC").col` | `(assente)` | Divergenza | 
| `core_genera_completo_giornata.py` | 1 | `def core_genera_completo_giornata(data_consegna, t` | `(assente)` | Divergenza | 
| `core_genera_completo_giornata.py` | 5 | `path_base = f'{tenant}/REPORTS/{data_consegna}' if` | `(assente)` | Divergenza | 
| `core_genera_completo_giornata.py` | 34 | `for doc in db.collection('clienti').document('DNR'` | `(assente)` | Divergenza | 
| `core_genera_completo_giornata.py` | 69 | `match = next((d for d in deliveries_all if str(d.g` | `(assente)` | Divergenza | 
| `core_genera_completo_giornata.py` | 79 | `match = next((d for d in deliveries_all if str(d.g` | `(assente)` | Divergenza | 
| `core_genera_completo_giornata.py` | 122 | `doc_ref = get_db().collection('clienti').document(` | `(assente)` | Divergenza | 
| `create_user.js` | 13 | `const dipendenteRef = db.collection('clienti').doc` | `(assente)` | Divergenza | 
| `fix_anomalie.py` | 12 | `r"\1\2const activeTenant = localStorage.getItem('a` | `(assente)` | Divergenza | 
| `fix_anomalie.py` | 16 | `# 2. Replace hardcoded DNR in onSnapshot paths wit` | `(assente)` | Divergenza | 

*(Mostrate prime 100 divergenze reali tra i due branch)*

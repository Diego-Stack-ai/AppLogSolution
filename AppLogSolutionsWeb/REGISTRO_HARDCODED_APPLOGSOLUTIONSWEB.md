# REGISTRO HARDCODED - AppLogSolutionsWeb

Sintesi decisionale basata sulle EVIDENZE REALI (riferimento `EVIDENZE_HARDCODED_APPLOGSOLUTIONSWEB.md`).

| ID | Gravità | File | Riga | Funzione | Valore reale | Chiamanti/consumer | Rischio verificato | Gruppo | Azione |
|----|---------|------|------|----------|--------------|--------------------|--------------------|--------|--------|
| HC-01 | Critico | `.firebaserc` | 3 | Config | `log-solution-60007` | Firebase CLI | Merge errato sovrascrive target prod | 1. Correggere prima della Prod | Escludere da merge o isolare alias |
| HC-02 | Medio | `functions/main.py` | 125 | get_tenant | `'DNR'` | Endpoint HTTP vari | Dati salvati in DNR di default | 2. Correggere dopo rilascio | Imporre validazione tenant strict |
| HC-03 | Basso | `.github/workflows/deploy.yml` | 26 | CI CD | `log-solution-60007` | GitHub Actions | Nessuno (Intenzionale su main) | 3. Mantenere | Lasciare invariato |
| HC-04 | Alto | `scripts/core_genera_completo_giornata.py` | 45 | Path config | `G:\\Il mio Drive\\...` | Script offline | Crash se eseguito su PC diverso | 1. Correggere prima della Prod | Usare os.path o parametri |
| HC-05 | Medio | `frontend/script.js` | 7 | Cache init | `v3.00` | Service Worker | Cache stale se non in sync | 3. Mantenere | Aggiornare solo via bump_version.py |

## Giudizio Finale
- **Bloccanti dimostrati:** Percorsi assoluti Windows negli script offline (`core_genera_completo_giornata.py`). Il file `.firebaserc` contiene il project di prod come default in main, che non deve mai essere sovrascritto da cantiere.
- **Elementi non bloccanti (Debito Tecnico):** I fallback a `DNR` in `functions/main.py` sono diffusi ma servono attualmente la continuità operativa finché il frontend non diventerà rigoroso nell'invio del payload.
- **Hardcoded legittimi:** L'ID di progetto in `.github/workflows/deploy.yml` è corretto e intenzionale.
- **Punti da verificare:** I chiamanti esatti dei fallback DNR nei form UI del frontend richiedono un test E2E per garantire che inviino esplicitamente il `tenant`.

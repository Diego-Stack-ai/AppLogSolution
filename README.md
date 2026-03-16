AppLogSolution
==============

Sistema per la gestione delle consegne (frutta/latte alle scuole) e la relativa app web di consultazione.

Struttura del progetto
----------------------

- **backend**  
  Configurazioni lato server (es. credenziali Firebase Admin, NON tracciate su Git).

- **dati**  
  Script, dati sorgente e output relativi alle consegne. In particolare:
  - `CONSEGNE/CONSEGNE_<data>/` – pipeline per una specifica data (PDF DDT divisi, script Python, file Excel, JSON, ecc.).
  - `CONSEGNE/DDT-ORIGINALI/` – PDF originali dei DDT per frutta/latte.
  - Altri file Excel/report di supporto (rientri, orari mancanti, aggiornamento articoli, ecc.).

- **docs**  
  Documentazione del dominio CONSEGNE e dei flussi dati. Il file principale è:
  - `Gestione CONSEGNE.md` – descrive struttura cartelle, pipeline di elaborazione e il file JSON unificato da usare come “API dati”.

- **webapp**  
  App web front‑end (solo HTML/JS/CSS) che utilizza i dati prodotti dalla pipeline:
  - Pagine principali: `index.html`, `login.html`, `dashboard.html`, `clienti.html`, `visualizzazione.html`, `impostazioni.html`, `inserimento.html`, `mappa_consegne.html`.
  - Script: `firebase-config.js`, `firebase-auth-sync.js`, `script.js`.
  - Stili: `styles.css`.

Prerequisiti
------------

- Git installato.
- Python (per eseguire la pipeline in `dati/CONSEGNE`, se necessario).
- Un progetto Firebase configurato (le credenziali reali NON vanno tracciate nel repository).

Avvio rapido
------------

1. **Clona il repository**

   ```bash
   git clone https://github.com/Diego-Stack-ai/AppLogSolution.git
   cd AppLogSolution
   ```

2. **Pipeline dati (opzionale, se devi rigenerare i dati consegne)**  
   Vedi `docs/Gestione CONSEGNE.md` per i dettagli su:
   - dove posizionare i PDF dei DDT,
   - come lanciare gli script in `dati/CONSEGNE/CONSEGNE_<data>/`,
   - come ottenere il file JSON unificato dei punti di consegna.

3. **Avvio dell’app web**  
   Apri `webapp/index.html` in un browser (o servi la cartella `webapp` con un semplice server statico) dopo aver configurato `firebase-config.js` con il tuo progetto Firebase.

Note su sicurezza e segreti
---------------------------

- I file di credenziali sensibili (es. `backend/config/log-solution-60007-firebase-adminsdk-*.json`) **non sono tracciati** da Git e non devono essere committati.
- Per condividere la configurazione, utilizzare eventualmente file di esempio (es. `firebase-config.example.js`) senza chiavi reali.


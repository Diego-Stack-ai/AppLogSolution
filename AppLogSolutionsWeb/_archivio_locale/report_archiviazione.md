# Report di Archiviazione e Pulizia Codebase (Preparazione alla Produzione)

Questo documento analizza lo stato della codebase del progetto **AppLogSolutions Web** e traccia tutte le operazioni di pulizia e archiviazione effettuate per snellire l'applicazione in vista del deploy in produzione.

In conformità con le linee guida, tutti i file identificati come obsoleti, di test o non referenziati **non sono stati eliminati**, ma spostati nella cartella `_archivio_locale` mantenendo la gerarchia originale delle directory.

---

## 1. Elenco Completo dei File e Cartelle Spostati

### Dalla Root Generale (`G:\Il mio Drive\App`)
* `Nuovo Documento di testo.txt`: Appunti di analisi architetturale e logistica (Haversine vs Google Directions).
* `compare.py`: Vecchio script Python standalone per il confronto di directory locali (`AppLogSolution` vs `AppLogSolutions`).

### Dalla Root di Progetto (`G:\Il mio Drive\App\AppLogSolutionsWeb`)
* `ReportPianificazione (5).xlsx`: Foglio di calcolo Excel temporaneo (10.5 KB) usato per test locali.
* `scratch/` (cartella): Directory contenente 50 script Python di ispezione/seeding/migrazione, screenshot di test (`map_test_screenshot.png`) e log di vecchie esecuzioni (`10_runs_log.txt`, `test_log.txt`).
* `brain/` (cartella): Directory di sistema generata da precedenti conversazioni di agenti AI (`5b331969-a116-4371-8a75-148d78b153a6`) contenente log e scratch non pertinenti al funzionamento dell'app in produzione.

### Dal Frontend (`G:\Il mio Drive\App\AppLogSolutionsWeb\frontend`)
I seguenti file sono script Python monouso creati in passate sessioni AI per applicare fix o generare template HTML/CSS. Non sono utilizzati dall'applicazione web:
* `add_debug_alerts.py`
* `apply_modal_presenze.py`
* `bump.py`
* `fix_buttons.py`
* `fix_close_dettagli.py`
* `fix_css.py`
* `fix_ids.py`
* `fix_ids2.py`
* `fix_modifica_e_css.py`
* `fix_open_dettagli.py`
* `fix_presenze.py`
* `generate_crud.py`
* `update_presenze.py`
* `update_presenze2.py`
* `update_presenze3.py`
* `update_presenze4.py`
* `update_presenze5.py`
* `update_version.py`
* `fatturazione_mappe/` (cartella): Cartella vuota e non referenziata.

---

## 2. Motivo della Classificazione come "Inutilizzati"

1. **Script di Automazione e Fix Passati (`*.py` in frontend e root):** L'applicazione web è un progetto HTML/JS/CSS puro per il frontend e Python (Cloud Functions `main.py`) per il backend. Gli script Python presenti in `frontend/` servivano esclusivamente ad agenti AI o sviluppatori per manipolare stringhe o fare refactoring automatico.
2. **Documentazione non referenziata e fogli Excel:** File come `Nuovo Documento di testo.txt` e `ReportPianificazione (5).xlsx` appartengono a fasi di analisi o a travaso dati manuale/locale, completamente svincolati dal codice web che si interfaccia unicamente con Firebase/Firestore.
3. **Cartelle Temporanee (`scratch`, `brain`, `fatturazione_mappe`):** Contengono log, esperimenti Selenium, screenshot e dump JSON di test. La loro presenza appesantisce inutilmente l'alberatura del progetto e il processo di indicizzazione/deploy.

---

## 3. Analisi dei Dubbi, Rischi e File Mantenuti Attivi

In conformità alla regola *"se un file è dubbio, non spostarlo e segnalarlo nel report"*, sono stati condotti controlli rigorosi sui seguenti elementi, che **SONO STATI MANTENUTI NELLA LORO POSIZIONE ORIGINALE**:

### A. `credenziali_dipendenti.csv` (in `AppLogSolutionsWeb`)
* **Stato:** Mantenuto in `AppLogSolutionsWeb/credenziali_dipendenti.csv`.
* **Motivo del dubbio/rischio:** Sebbene non sia importato o letto direttamente dal codice frontend/backend (ed è correttamente ignorato in `.gitignore`), contiene informazioni anagrafiche e credenziali di vitale importanza per l'amministratore del sistema.
* **Valutazione del rischio:** Poiché la cartella `_archivio_locale` è destinata a essere eliminata in futuro, spostare questo file nell'archivio temporaneo comporterebbe il rischio inaccettabile di perdita definitiva delle credenziali dei dipendenti.

### B. `bump_version.py` (in `AppLogSolutionsWeb` e `frontend`)
* **Stato:** Mantenuti attivi nelle rispettive posizioni.
* **Motivo del dubbio/rischio:** `AGENTS.md` definisce una procedura tassativa per il deploy e l'aggiornamento della versione (`?v=X.XX`). Questi script racchiudono la logica di parsing e incremento per `sw.js`, `script.js` e i file HTML. Rimuoverli rischierebbe di interrompere i flussi di deploy futuri degli agenti o dell'operatore.

### C. `mappe_autisti/` e `distinte/` (in `frontend`)
* **Stato:** Mantenuti attivi in `frontend/mappe_autisti/` e `frontend/distinte/`.
* **Motivo del dubbio/rischio:** Contengono oltre 100 file HTML statici di mappe di consegna e file di testo come `LINK_WHATSAPP_AUTISTI.txt`. Pur sembrando generati staticamente nel mese di maggio/giugno, rappresentano URL di produzione inviati agli autisti tramite WhatsApp. Spostarli causerebbe un errore 404 (Not Found) a chiunque tenti di accedere ai link di viaggio in corso o passati.

### D. `functions/caches/`
* **Stato:** Mantenuto attivo in `functions/caches/`.
* **Motivo del dubbio/rischio:** Contiene file JSON di grandi dimensioni (`distanze_reali_cache.json`, `directions_cache.json`). Sono cache vitali interrogate da `functions/main.py` per evitare chiamate ripetitive e costose alle API di Google Maps/Directions, come documentato anche nell'architettura del sistema.

### E. File di Configurazione e CI/CD (`.env`, `cors.json`, `firebase.json`, `.github`, ecc.)
* **Stato:** Mantenuti attivi.
* **Motivo:** Essenziali per la configurazione di Firebase, le regole di sicurezza Firestore/Storage, l'autenticazione e il deploy automatico via GitHub Actions.

---

## 4. Conclusione e Prossimi Passi

L'applicazione è ora alleggerita da file di sviluppo temporanei e codice di scratch, mantenendo al contempo intatti i file anagrafici sensibili e gli storici operativi delle mappe autisti. La build e i flussi CI/CD rimangono perfettamente intatti e pronti per la produzione.

# Architettura Multi-Tenant: Mappa e Piano di Migrazione

*Questo documento è la memoria storica e la mappa strutturale per il passaggio dell'infrastruttura AppLogSolutions da Monolitica (centrata su DNR) a Multi-Tenant (DNR, Gran Chef, Cattel, Bauer, ecc.).*

---

## 0. Glossario Aziendale (Domain Knowledge)
Per evitare ambiguità storiche, stabiliamo la seguente nomenclatura:
*   **Clienti (Tenant / Progetti):** Le aziende mandanti che vi affidano il lavoro di logistica (es. DNR, Cattel, Gran Chef, Bauer). Nel database sono identificati anche come `progetti`.
*   **Punti di Consegna:** Le destinazioni fisiche dove gli autisti consegnano la merce (spesso chiamati erroneamente "clienti" perché sono i clienti di DNR/Cattel). 
*   **Sorgenti Dati:** Ogni Cliente ha logiche di importazione diverse:
    *   **DNR:** Importa tramite lettura di complessi "lenzuoloni" PDF divisi in *Progetto Frutta* e *Progetto Latte*. 
        * *Nota Tecnica di Unificazione:* Nel backend (`main.py`), i DDT della frutta e del latte vengono processati separatamente, ma poi l'algoritmo utilizza i campi `codice_frutta` e `codice_latte` dell'anagrafica per fonderli in un **singolo Punto di Consegna** sulla mappa. Questo merge interno (stesso cliente, merci diverse) è una logica esclusiva di DNR.
    *   **Cattel e Gran Chef:** Importano i viaggi/punti di consegna tramite file Excel. A differenza di DNR, se ci sono due consegne per la stessa pizzeria in due Excel diversi, al momento l'app crea due Punti di Consegna separati.
    *   **Bauer:** Al momento non gestito (non si importa nulla). Sarà oggetto di un nuovo studio dedicato.

## 0.1 L'Obiettivo Finale: Isolamento Dati vs. Ottimizzazione Globale (Cross-Tenant)
Sebbene i dati (Database e Storage) debbano essere salvati in compartimenti separati per ogni Cliente in fase di importazione (aggiungendo la "firma" di chi sono), **il vero scopo operativo dell'applicazione è globale**. 
Molto spesso i Punti di Consegna di DNR, Cattel e Gran Chef coincidono fisicamente (es. stesso ristorante) o sono vicini. 
L'obiettivo supremo dell'app in pianificazione è permettere all'operatore di caricare i dati di tutti i clienti e **vedere una Mappa Unica Giornaliera** con tutti i Punti di Consegna (identificati da icone diverse per cliente). L'operatore potrà poi unire pacchi di DNR e Cattel sullo stesso furgone per ottimizzare i costi e i percorsi aziendali.

L'architettura Multi-Tenant dovrà quindi permettere la lettura combinata dei dati di più Tenant quando ci si trova nelle pagine di pianificazione e mappa.

---

## 1. Mappa Attuale del Sistema (Contesto Firebase e Storage)

### 1.1 Collezioni Firestore (Database)
Attualmente quasi tutti i dati operativi sono ancorati al nodo `clienti/DNR/`.

*   **Radici di Tenant (Hardcoded su DNR):**
    *   `clienti/[TENANT]/raccolta clienti`: L'anagrafica di tutte le destinazioni.
    *   `clienti/[TENANT]/codici articoli`: Il catalogo dei prodotti (pesi, conversioni).
    *   `clienti/[TENANT]/ddt`: I documenti di trasporto caricati dal gestionale.
    *   `clienti/[TENANT]/viaggi ddt`: I viaggi giornalieri pianificati.
    *   `clienti/DNR/rientri ddt`: La gestione delle anomalie e resi (Nota: **Esclusiva DNR**, altri clienti emettono nuovi DDT per le rese).

*   **Radici Globali (Condivise, NON legate a Tenant):**
    *   `dipendenti`: Autisti, impiegati e amministratori (Rubrica globale).
    *   `mezzi`: Flotta veicoli (Rubrica globale).
    *   `giustificativi`: Ferie, malattie, presenze.
    *   `progetti`: Il Registro Centrale dei Tenant (DNR, Cattel, Gran Chef). Qui dentro salviamo le loro impostazioni contrattuali (il **prezzario**, tariffe per patente, costo a collo, viaggi predefiniti, ecc.). Questi dati restano globali perché servono all'Amministrazione per la fatturazione.
    *   `scaletta_*` e `navetta_*`: Configurazioni di routing per le navette e spole interne.
    *   `magazzini_sedi`: I magazzini e hub di partenza della merce.
    *   `stats_monitoring`, `stats_operative`: Le metriche di utilizzo delle funzioni.
    *   `config`: Permessi (es. `permessi_dashboard`).

### 1.2 Storage (File Fisici)
*   **Bucket:** `log-solution-60007.firebasestorage.app`
*   **Cartelle Operative (Attualmente globali/mischiate):**
    *   `REPORTS/[data]/`: File JSON di calcolo e PDF distinte per i magazzinieri.
    *   `split_ddt/[data]/`: I PDF originali tagliati per autista.
    *   `CONSEGNE/CONSEGNE_[data]/`: I PDF finali e le mappe generate (HTML).
*   **Cartelle Globali da Mantenere:**
    *   `caches/`, `caches_backup/`: Le cache della Matrice di Google (Condivise, fa risparmiare soldi su tutti i tenant).

### 1.3 Frontend (Script e UI)
La logica è distribuita su molti script che interrogano Firestore usando `collection(db, "clienti", "DNR", ...)`.
*   **Core State & Auth:** `firebase-auth-sync.js` (I listener in realtime), `firestore-service.js`, `script.js`.
*   **Interfaccia Utente (Le Pagine):** `elaborazione.html`, `fatturazione.html`, `gestione.html`, `gestione_anomalie.html`, `gestione_articoli.html`, `gestione_nuovi_clienti.html`, `gestione_orari.html`, `gestione_rientri.html`, `impostazioni.html`, `link_viaggi.html`, `mappa_google.html`, `mappa_zone.html`, `pianificazione.html`, `presenze.html`, `dashboard.html`.

### 1.4 Backend (Cloud Functions)
*   **File:** `functions/main.py` (nella cartella AppLogSolutionsWeb)
*   **Logica:** Attualmente `main.py` fa riferimenti statici (`document('DNR')`) e salva su Storage in cartelle globali. Le funzioni dovranno accettare un parametro `tenant` dal frontend.

---

## 2. Strategia di Migrazione (Piano a Capitoli)

Per evitare interruzioni del servizio, affronteremo la transizione un capitolo alla volta, collaudando tutto su branch `sviluppo` prima di unire su `main`.

### Capitolo 1: Global State del Tenant (Frontend)
*   **Obiettivo:** Il sistema deve sapere quale "azienda" sta gestendo in un dato momento.
*   **Azione:** Inserimento di un selettore (Dropdown) "Tenant Attivo" globale (es. nella Navbar).
*   **Azione:** Memorizzazione persistente in `localStorage` in modo che passando da `dashboard.html` a `pianificazione.html` l'impostazione non vada persa.

### Capitolo 2: Astrazione Frontend
*   **Obiettivo:** Rimuovere l'hardcoding di `DNR` in tutte le pagine HTML e JS.
*   **Azione:** Modifica di `firebase-auth-sync.js`. I listener (`onSnapshot`) dovranno essere distrutti e ricreati dinamicamente al cambio del tenant.
*   **Azione:** Ricerca e sostituzione a cascata di `collection(db, "clienti", "DNR", ...)` in ogni file HTML e JS, utilizzando il `localStorage` o lo State Manager del Capitolo 1.

### Capitolo 3: Astrazione Backend e Storage
*   **Obiettivo:** Le Cloud Functions devono elaborare i dati nel "silos" corretto.
*   **Azione:** Aggiornamento delle chiamate `httpsCallable` nel frontend per passare il payload `{ tenant_id: currentTenant }`.
*   **Azione:** Refactoring esteso di `main.py` per usare `tenant_id` nei riferimenti Firestore.
*   **Azione:** Isolamento dello Storage. Le cartelle diventeranno: `[tenant_id]/REPORTS/...` e `[tenant_id]/CONSEGNE/...`.

### Capitolo 4: Dashboard, Mappa Globale e Sicurezza
*   **Obiettivo:** Raggiungere l'obiettivo supremo: l'unificazione visiva per l'ottimizzazione logistica, pur mantenendo separati i database.
*   **Azione:** La pagina di Pianificazione e le Mappe HTML dovranno essere in grado di effettuare il "fetch" parallelo dei `viaggi ddt` e dei `punti di consegna` di TUTTI i Tenant attivi (DNR + Cattel + Gran Chef) per la data selezionata.
*   **Azione:** Differenziare visivamente i Punti di Consegna sulla mappa globale tramite icone dedicate al Tenant di appartenenza.
*   **Azione:** Permettere all'algoritmo di unione viaggi di mescolare viaggi di Tenant diversi sullo stesso Autista/Mezzo (salvando però i riferimenti corretti ai database di origine).
*   **Azione:** Le fatturazioni e le statistiche operative dovranno essere visualizzabili "Per Tenant" o "Globali" a scelta.

---

## 3. Log Operativo delle Modifiche (Changelog Vivo)
*Qui terremo traccia delle modifiche completate file per file. Ogni volta che modificheremo uno script a cascata, lo segneremo qui per memoria storica.*

*   [ ] **Capitolo 1:** (In attesa di inizio lavori)
*   [ ] **Capitolo 2:** (In attesa di inizio lavori)
*   [ ] **Capitolo 3:** (In attesa di inizio lavori)
*   [ ] **Capitolo 4:** (In attesa di inizio lavori)

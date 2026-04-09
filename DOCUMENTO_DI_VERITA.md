# AppLogSolutions – Documento di Verità

## 1. Descrizione Generale dell'App
AppLogSolutions è una piattaforma ibrida (Web App + Backend On-Premise) sviluppata per digitalizzare le operazioni di logistica e trasporti, comprese fatturazione, viaggi e distribuzione autisti.

- **Scopo:** Automatizzare l’inserimento dei turni degli autisti, generare percorsi ottimizzati dalle bolle di consegna (Excel/PDF), calcolare distanze e tempi per rendicontare lavoro e fatturazione.
- **Cosa fa:** Permette agli impiegati di configurare dati e inviare fogli viaggio tramite PWA. Gli autisti possono consuntivare l’inizio/fine dei giri. Il Backend Python esegue geolocalizzazione indirizzi (usando API Google Maps) ed estrazione o riordino delle coordinate (tramite *Google OR-Tools* e formule geometriche come *Haversine*).
- **Destinatari:** Amministrazione e logistica base (creano liste e fatture), e Autisti mobili (eseguono percorsi e consuntivano orari via app/link).

---

## 2. Architettura del Progetto
### Stack attuale
- **Frontend Cloud:** `frontend/` PWA Vanilla JS altamente performante (senza framework monolitici), ospitata integralmente su Google Firebase Hosting. Utilizza Firebase SDK per l'Auth (gestendo il login) e Cloud Firestore per dati anagrafici e tracking in realtime. I meccanismi offline sono garantiti da Service Workers (`sw.js`).
- **Backend Operativo:** L'elaborazione sfrutta codice Python (`Fatturazione/`, `Progetto Scuole/`) usando librerie come `pandas` (per tabelle), `or-tools` (per i problemi di routing/TSP) e `requests`. 
- **Servizi Esterni:** Ecosystem serverless Firebase, API Google Maps (Geocoding assistito e link statici su mappe stradali).

### Architettura Ibrida Disaccoppiata
- Cloud (Firestore + App Hosting).
- Dati/Backup Logico (Excel Master salvati su archivi storage o file system Google Drive collegato in locale).
- Locale Processing (esecuzione di procedure via `.bat` che innescano Python su PC d'ufficio).
- Interfaccia intermedia (Flask locale sulla porta 5000 per instradare chiamate dal driver su IP interno aziendale in modo "legacy" - vedi `8_server_mobile_autisti.py`).

---

## 3. Flusso Operativo
Il software è logicamente diviso in due macro flussi paralleli ma complementari:
- **Modulo Fatturazione:** Prende l'input dai crudi Excel gestionali giornalieri e dall'anagrafica Master. Esegue raggruppamento e stima kilometrica calcolando rotte ottime (OR-Tools TSP). Successivamente inietta la fine logica per creare la fatturazione (tenendo conto di weekend o festività cattoliche con il motore temporale). Cache: `CACHE_CONSEGNE_TOP.json` impedisce di rifare geocoding abusivo e a pagamento sui clienti già analizzati.
- **Modulo Progetto Scuole:** Riceve DDT/Distinte miste per i plessi educativi (LATTE/FRUTTA), filtra e auto-aggiunge le coordinate mancanti via dizionario (`geocode_cache.json`), elabora il circuito stradale dal deposito di partenza (es. Veggiano) e distribuisce di conseguenza i nuovi Packing List per i magazzinieri e i vettori (`9_genera_distinte_da_viaggi.py`).

1. **Aggiornamento Dati:** Import PDF/DDT/Excel in sistema locale.
2. **Generazione Tappe Back-office:** I `.bat` lanciano gli script Python, che verificano i clienti con la Cache Geocoding Avanzata e geolocalizzano i nuovi indirizzi mancanti.
3. **Pianificazione Percorsi e Distinte:** Python calcola un instradamento continuo. I documenti cartacei digitalizzati vengono auto-reimpaginati sulle tabelle riordinate seguendo i progressivi del camion.
4. **App Autisti:** PWA su mobile permette login, selezione turno e Start. Il tasto “Vai dal cliente” reindirizza fluidamente un Deep URL unito alle coordinate sul Navigator Standard dello smartphone.
5. **Rendicontazione Finale:** Python unisce i resoconti elaborando date valide lavorative (skippando festività).

---

## 4. Analisi del Codice
### Frontend
- `script.js`: Wizard interattivo "Inizio-Fine", calcolo timer ordinarie/straordinari, `sessionStorage` persistente della PWA per evitare reload bozze accidentali in movimento.
- `sw.js` & `manifest.json`: Gestione offline, caching profondo di risorse e installabilità del sistema operativo su Homescreen.

### Backend
- Moduli `.py` sequenziali in base e sottocartelle (es. `1_Riepiloghi_Giornalieri.py`, `3_Crea_Percorso_Google_Diretto.py`, `Estrai_Anagrafica_Clienti.py`).
- Flusso dati che lavora leggendo e droppando i DataFrame di Pandas convertendo tabelle Excel.

---

## 5. Stato Attuale & Avanzamenti
- **Completato Base Tecnica:** Disattivata la vecchia e costosa chiamata "Google Matrix Direction" tra istituti scolastici, avendo uniformato il motore logico e vettoriale di distanza adottando l'equazione approssimata *Haversine* + *OR-tools TSP*, abbattendo il costo API a 0 in fase di calcolo percorso. Anagrafica Master integrata e precaricata con chiavi cache di 25 clienti complessi per tagliare gli errori storici.
- **Da Affinare Primario (Bottleneck):** Disconnessione asincrona estrema tra l'ecosistema in locale `Excel.xlsx` e il real-time Data in Cloud `Firestore`. Devono ancora convivere due poli differenti di update.
- **Assenza di Start Hub/Cruscotto:** Attualmente tutto l'onere dell'esecuzione (import, geocodifiche) dipendono ad intermittenza da PC fisici d'ufficio e prompt MS-DOS `.bat`. 

---

## 6. Logica di Business
- Modello RBAC (Roles): `impiegata`, `amministratore`, `autista`. I ruoli bloccano e sbloccano aree GUI della PWA in automatico.
- Autisti hanno rigorosamente accesso esclusivamente alla macro della rendicontazione o lista percorsi a loro assegnata. Nessuna facoltà editoriale sui registri.

---

## 7. Linee Guida di Integrabilità Backend Futuro
- Abbandono esecuzioni vincolate a partizioni NTFS precise locali (es. lo split dei path `G:\Il mio Drive\...`).
- **Puntamento a Cloud Serverless API:** HTTP requests emesse nativamente dalla dashboard amministrativa WebApp invocano i moduli asincroni Python (su piattaforme Cloud Run o Cloud Functions Gen 2), potendo gestire stream di caricamento file direttamente sui Bucket di Firebase Storage, neutralizzando l'esigenza di computer fisici base accesi in azienda.

---

## 8. Problemi Potenziali Riscontrati
- **Falle di Sicurezza Rilevate:** Private API Key per Google Maps visibili completamente in _clear text_ e _hardcoded_ nel file sorgente degli applicativi. Interdizione mancante sul microservizio IP interno (Nessuna validazione Token).
- **Race Condition / Concurrency Lock Files:** L'aggiornamento massivo e simultaneo di fogli d'estensione `.xlsx` (scrittura multipla Pandas To_Excel) genera blocco per file read-only qualora impiegate diverse entrino nel medesimo file da cartella condivisa di Drive Desktop.

---

## 9. Azioni E Roadmap (I Miglioramenti Consigliati)

🎯 **Priorità Immediata - Refactoring .ENV**
- Spostamento massivo ed espulsione delle configurazioni Firebase e delle API Key Google private dai file tracciati a Git o statici, proteggendole sotto standard `.env`.

📁 **Unificatore del Database (Database Shift)**
- Centralizzazione progressiva delle strutture preminenti: Clienti Master, Liste di Viaggio, Dizionari (Cache Geoloc) sradicate dagli Excel base e spostate massivamente su `Cloud Firestore` NoSQL rendendo l'ambiente "Single Source Of Truth".

☁️ **Orchestrazione Automatica (Admin PWA Clicks)**
- Costruzione, all'interno della pagina PWA di logistica, del pannello Cruscotto (es. tab `/admin/processi`), retto da bottoni pulsanti invocatori:
  - "Carica & Leggi Distinta DDT"
  - "Geolocalizza Automatica Nuovi Plottaggi"
  - "Esegui OR-Tools Per Generazione Auto-Mappe"

---

## 10. Funzionalità ed Evoluzioni Future
- **Migrazione Mobile Verso FLUTTER / DART:** Il porting progressivo ed unicamente limitato al Client Navigatore Mobile da _HTML PWA_ a _Framework Nativi Flutter_. L'introduzione di un sistema compilato abilita lo stream di "Background Tracker GPS" essenziale perché Firestore possa aggiornare ai terminali in centrale il ping posizione autista, interdicendo il congelamento batteria e i killing tabs subìti dai Web Browser su iOS/Android.
- **Computer Vision ed OCR Mobile:** Unione fotocamera App: l'autista acquisisce ddt cartacei -> il sistema Cloud Storage lo manda a Python che estrae i valori, conferma match firma consegna ed archivia formalmente dentro Google Drive come log storico.

---

## 11. Note di UX / Interfaccia Sulle Mappe
- La visualizzazione "Mappe Interattive" va mantenuta sobria per non stressare attivamente gli operatori alla guida. Rotte colme (20-30 fermate) escludono l'uso di mappe in embed sovraccaricate.
- L'intento focale è mantenere una UI snella list-based dove le Mappe vengono evocate solo esplicitamente su touch della singola riga. Il pulsante “Vai dal cliente” sparerà l'Intents Universale per aprire esclusivamente la pinboard nell'Applicazione Ufficiale Navigation Google Maps.
- Aggiunta richiesta: Highlighting Cromatico (Es. righe sbarrate per le fermate visitate o raggruppamento per vicinanze zonali).

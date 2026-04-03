# Progetto Log Solution

Il sistema logistico è suddiviso in 3 macro aree indipendenti ma interconnesse da uno strato di frontend (Firebase App). Sfrutta Python come motore backend per l'elaborazione dei dati ed algoritmi di intelligenza per il Routing (tramite *Google OR-Tools*), Firebase per il database NoSQL/Hosting e un'App Mobile Progressiva (PWA) sviluppata in Vanilla JS, HTML e API Google Maps per la gestione ed inseguimento delle operazioni sul campo.

Di seguito il dettaglio funzionale analizzato dalle directory di progetto:

## 1. Modulo "FATTURAZIONE"
Questo modulo si occupa dell’elaborazione mensile contabile, della referenziazione clienti e del calcolo del chilometraggio ottimizzato.

**Input**
* **File giornalieri Excel (`Riepiloghi_Giornalieri`):** File tabellari esportati dal gestionale con il dettaglio delle consegne, vettori previsti e codice cliente.
* **`Anagrafica_Clienti_Master.xlsx`:** File anagrafico sorgente estratto dai report e unificato come vocabolario dei database.

**Elaborazioni (Librerie: *Pandas, Openpyxl, OR-Tools, Requests*)**
* `1_Riepiloghi_Giornalieri.py`: Estrae i dati mensili o raggruppa le intestazioni di base.
* `Estrai_Anagrafica_Clienti.py`: Legge ogni viaggio, raccogliendo ragioni sociali e stringhe di indirizzi non univoche ricompattandole nel file Master.
* `2_Calcola_KM_Mensili.py`: Effettua la stima chilometrica.
* `3_Crea_Percorso_Google_Diretto.py`: Prende gli indirizzi dai viaggi, prima cerca nella cache e poi geocodifica (via API Google Maps). Ordina le tappe con l'algoritmo TSP tramite Google OR-Tools. Successivamente modella template statici HTML in stile Card che incorporano gli URL per attivare G-Maps Navigatore.
* **File `CACHE_CONSEGNE_TOP.json`:** È il dizionario persistente essenziale (Key: "indirizzo stringa" -> Value: {lat, lng}). Ferma le chiamate a pagamento e uniforma gli errori.
* `4_Compila_Fatturazione.py`: Crea automatismi di billing per fatturazione iniettando dati (potenzialmente su `FATTURAZIONE 2026.gsheet` / GESTIONE.xlsx o file finale).

**Output**
* Mappe interattive ad uso dei Driver esportate in `frontend/fatturazione_mappe`.
* Link WhatsApp raggruppati da mandare ai dipendenti.
* File contabili riepilogativi generati a fine mese.

---

## 2. Modulo "PROGETTO SCUOLE"
A differenza di fatturazione, questa pipeline si concentra sulle rotte operative dinamiche derivanti in tempo reale da liste miste (PDF bolle o fogli sparsi per Latte/Frutta).

**Input**
* **Distinte / DDT** (dentro le cartelle LATTE/FRUTTA). Forse PDF o file tabellari di ritorno pre-consegne.
* **`mappatura_destinazioni.xlsx`**: File master delle geolocalizzazioni o database con le informazioni dei plessi scolastici.

**Elaborazioni (Backend in Cartella `PROGRAMMA`)**
L'elaborazione sfrutta interfacce a blocco via File `.bat` eseguite progressivamente dall'ufficio:
* `1_AGGIORNA_DATI` a `(1_2_3_4)_estrai_ddt_consegne.py`: Processa il PDF/OCR/Excel dei DDT. Estrae codici prodotti, scuole e distinte e le unificata in un dizionario unificato Python (`3_crea_lista_unificata.py`).
* `4_mappa_zone_google.py`: Geocodifica le scuole mancanti via Google API sfruttando il file `geocode_cache.json`.
* `6_genera_percorsi_veggiano.py`: Ricrea i routing dal deposito di Veggiano sempre utilizzando Google OR-Tools.
* `7_genera_mappe_mobile_autisti.py`: Identico approccio mappale, dove le stampe HTML statiche o JSON dinamici sono distribuiti sotto `/mappe_autisti/` su Firebase.
* `9_genera_distinte_da_viaggi.py`: Riorganizza i dati dei viaggi ottimizzati per rigenerare PDF "Packing List" ad uso magazzinieri o vettori, riordinati *esattamente* nel flusso stradale previsto.
* `10_sync_coordinate_da_cloud.py`: Legge coordinate real-time ri-iniettate dai fattorini durante i giri.

**Output**
* Manifest e liste di imballo PDF.
* Report anomalie/mancanze in `.xlsx`. 
* Cartelle Firebase riempite con i giri aggiornati.

---

## 3. Frontend / App Mobile (Cartella `frontend`)
Si tratta dell'applicazione lato client ospitata integralmente su Google Firebase Hosting (gestito da `firebase.json`). Permette agli autisti di tracciare consegne e visualizzare dashboard.

**Librerie Client Importate**
* Nessun framework pesante come React o Vue -> Vanilla Javascript (performance assolute).
* SDK Ufficiale Firebase Modules (`firebase-app.js`, `firebase-auth.js`, `firebase-firestore.js` distribuiti via CDN).
* Google Maps JS Async defer library.

**Componenti Chiave JSON**
* `manifest.json`: Tratta questo sito frontend come una Progressive Web App (PWA). Permette all'autista di "Aggiungi a schermata Home" il sito e nascondere il browser.
* `firebase.json`: Regole di hosting cloud.

**Flusso Logico e File Funzionali**
* **Autenticazione & Stato**: (`login.html` + `firebase-auth-sync.js`) Identifica l'utente/driver e il suo livello di accesso in sicurezza.
* **Rilevazione in Background**: L'app vive di GPS (`gps-tracker.js`). Monitora posizione (`navigator.geolocation.watchPosition`), traccia latitudine e longitudine in streaming continuo (catturando un ping logico temporizzato) e logga su `Firestore database` per report in base-ufficio.
* **Interfaccia Utente**: `dashboard.html` espone i cruscotti, `clienti.html`, `inserimento.html`, e `visualizzazione.html` operano e renderizzano tramite `script.js` e `ui-render.js` lo stato operativo in tempo reale. Le operazioni "Consegnato", "Foto", o "Fix Coordinata di Consegna" generano payload JSON direttamente nel Firestore di cloud o localStorage offline.

## Sintesi e Prossimi Passi
L'App attualmente ha solide basi per la pianificazione server-side distribuendo mappe su Firebase per l'utilizzo mobile.

---

## 🚧 ROADMAP & TASK TRACKING
*Questa sezione viene aggiornata man mano per tracciare cosa vogliamo fare e i traguardi raggiunti in modo da avere l'intero progetto all'interno di un unico file.*

### ✅ Fatto (Completato)
- **Unificazione Pipeline Algoritmica:** Disattivazione del sistema Google Matrix a pagamento nelle rotte delle scuole e uniformazione all'algoritmo Haversine + OR-Tools (che azzera i costi API per calcolo matrici). Adesso Scuole e Fatturazione usano la stessa identica base matematica fulminea.
- **Aggiornamento Anagrafica Master:** Geocodifica e inserimento di 25 nuovi indirizzi corretti nel file `Anagrafica_Clienti_Master.xlsx` sostituendo i precedenti formati errati.
- **Cache Geocoding Avanzata:** Scrittura dei 25 indirizzi aggiornati nel dizionario `CACHE_CONSEGNE_TOP.json` per pre-risolvere le bolle generanti futuri errori.

### ⏳ Da Fare (To-Do)
- **Rifacimento Frontend / UI:** Sviluppo della nuova Web App in HTML/Vanilla JS (dashboard operativa).
- **Integrazione Backend Python in Cloud:** Migrazione degli script locali Python (OR-Tools, Pandas, Haversine) su un ambiente nativo cloud (Firebase Cloud Functions Gen 2 / Cloud Run). In questo modo, il calcolo dei percorsi avverrà direttamente online tramite tablet senza passare per il PC dell'ufficio.
- **Gestione Stoccaggio (Storage Routing):** Predisposizione delle logiche per far processare i PDF Cloud al backend per trasferirli / storicizzarli poi automaticamente su Google Drive, sollevando Firebase dai pesi di storage.

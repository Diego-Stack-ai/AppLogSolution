# Workflow Automazione Logistica (AppLogSolution)

Questo documento descrive il processo di automazione per l'estrazione dei DDT, l'unificazione dei dati e la generazione della mappa interattiva.

## 🚀 La Catena di Elaborazione (Pipeline)

Il cuore del sistema è lo script orchestratore: **`(1_2_3_4)_estrai_ddt_consegne.py`**. 
Lanciando questo singolo file, il sistema esegue automaticamente i seguenti passaggi:

### 1. Preparazione e Pulizia (Step 0)
Per garantire che i dati siano sempre aggiornati e non "sporcati" da sessioni precedenti, lo script elimina i file temporanei della stessa data (`xlsx`, `json`, `html`, `kml`) prima di iniziare.

### 2. Estrazione DDT (Script 1 integrato)
- Scansiona le cartelle `FRUTTA` e `LATTE`.
- Estrae i dati (Data Consegna, Luogo Destinazione P-codice) dai PDF.
- Divide i PDF originali in singoli file rinominati per una facile consultazione.

### 3. Creazione Punti Consegna (Script 2)
- Incrocia i dati estratti con il file master `mappatura_destinazioni.xlsx`.
- Genera il file `punti_consegna.xlsx` aggregando indirizzi e nomi completi.

### 4. Unificazione e Geocodifica (Script 3)
- Consolida le liste e calcola le coordinate geografiche (Latitudine/Longitudine).
- Gestisce i "rientri" e genera il master file `punti_consegna_unificati.json`.

### 5. Generazione Mappa e KML (Script 4)
- Crea il file statico `4_mappa_zone_google.html` (interattivo).
- Crea il file `zone_google_DATA.kml` per Google Maps/Earth.

---

## 🛡️ Meccanismi di Robustezza (Cosa abbiamo risolto)

Per rendere il sistema affidabile su ogni computer e su Google Drive, abbiamo implementato:

- **Determinismo**: Ogni run è pulito e ripetibile, senza file orfani.
- **Sync Lag Protection**: Lo script attende 1.5 secondi tra un passaggio e l'altro e dispone di un "secondo tentativo automatico" se Google Drive è lento a scrivere l'HTML.
- **Indipendenza dall'Ambiente**: Lo script 4 è stato reso "intelligente": genera la mappa batch anche se Flask non è installato, evitando errori rossi nel terminale.
- **Pulizia Chirurgica**: Vengono eliminati dalle cartelle sorgente solo i PDF effettivamente elaborati.

---

## 📖 Istruzioni per l'Uso

### Elaborazione Giornaliera
1. Mettere i PDF in `FRUTTA` e `LATTE`.
2. Aprire il terminale nella cartella `dati`.
3. Lanciare: `python "(1_2_3_4)_estrai_ddt_consegne.py"`

### Apertura Mappa Interattiva
Dopo l'elaborazione, per modificare le zone o spostare i punti:
1. Lanciare: `python 4_mappa_zone_google.py`
2. Aprire il browser all'indirizzo indicato (solitamente `http://127.0.0.1:5000`).

---
*Ultimo aggiornamento: 24 Marzo 2026*

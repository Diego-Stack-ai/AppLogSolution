# Gestione CONSEGNE – Note per altri progetti
Questo file spiega cosa serve sapere a un nuovo agente / progetto per usare i dati della cartella `CONSEGNE` e degli script attuali.
---
## 1. Struttura cartelle principali
Radice (esempio):
- `c:\Gestione DDT viaggi\`
  - `Programma\` – tutti gli script Python
  - `CONSEGNE\`
    - `DDT-ORIGINALI\`
      - `FRUTTA\` – PDF multipagina originali
      - `LATTE\` – PDF multipagina originali
    - `CONSEGNE_16-03-2026\`, `CONSEGNE_09-03-2026\`, … – una cartella per ogni data
Dentro ogni `CONSEGNE_<data>`:
- `DDT-ORIGINALI-DIVISI\`
  - `FRUTTA\` – DDT singoli frutta (1 pagina)
  - `LATTE\` – DDT singoli latte (1 pagina)
- `punti_consegna_frutta.xlsx`
- `punti_consegna_latte.xlsx`
- **`punti_consegna_unificati.json`**  ← file “centrale” da usare in altri progetti
- (output di servizio, rigenerabili):
  - `mappa_consegne_<data>.html`
  - `consegne_app_<data>.html`
  - `punti_consegna_<data>.kml`
---
## 2. Script principali
Cartella: `Programma\`
- `estrai_ddt_consegne.py`
  - Input: `CONSEGNE/DDT-ORIGINALI/FRUTTA` e `LATTE`
  - Estrae tutti i DDT singoli e crea:
    - `CONSEGNE/CONSEGNE_<data>/DDT-ORIGINALI-DIVISI/FRUTTA`
    - `CONSEGNE/CONSEGNE_<data>/DDT-ORIGINALI-DIVISI/LATTE`
  - Alla fine lancia `crea_punti_consegna.py` e poi `crea_lista_punti_unificata.py`.
- `crea_punti_consegna.py`
  - Legge i PDF divisi (frutta/latte) + `mappatura_destinazioni.xlsx`
  - Crea:
    - `CONSEGNE_<data>/punti_consegna_frutta.xlsx`
    - `CONSEGNE_<data>/punti_consegna_latte.xlsx`
  - Raggruppa per riga di mappatura (stesso destinatario).
- `crea_lista_punti_unificata.py`
  - Input:
    - `punti_consegna_frutta.xlsx`
    - `punti_consegna_latte.xlsx`
    - `mappatura_destinazioni.xlsx`
  - Output:
    - **`CONSEGNE_<data>/punti_consegna_unificati.json`**
  - Unisce frutta+latte sulla stessa riga di `mappatura_destinazioni` (stesso indirizzo/punto).
  - Ogni punto contiene:
    - `nome`, `tipologia`, `indirizzo`
    - `lat`, `lon` (da mappatura)
    - `codice_frutta`, `codice_latte`
    - `orario_min`, `orario_max`
    - `codici_ddt_frutta`, `codici_ddt_latte`
    - `data_consegna`
    - `geo_query_nome_indirizzo`, `geo_query_indirizzo` (stringhe per geocoding)
- `crea_mappa_consegne.py`
  - Input: `CONSEGNE_<data>/punti_consegna_unificati.json`
  - Output:
    - `mappa_consegne_<data>.html` – mappa Leaflet (PC)
    - `consegne_app_<data>.html` – mini app HTML per telefono (lista + navigazione + “Consegna completata” salvata in localStorage)
    - `punti_consegna_<data>.kml` – KML per Google My Maps
### Geocoding (coordinate)
Regola per ogni punto:
1. Se in `mappatura_destinazioni.xlsx` ci sono coordinate (colonne M,N: latitudine, longitudine) → **usa quelle**.
2. Se mancano:
   - prova **Nominatim** con `geo_query_nome_indirizzo` (C + D + indirizzo)
   - se non trova, prova con `geo_query_indirizzo` (solo indirizzo)
   - se ancora non trova, prova **Photon (Komoot)** con indirizzo
3. Se neanche Photon trova, il punto resta senza coordinate (comparirà solo nel JSON, non nelle mappe).
La cache per il geocoding è in `geocode_cache.json` (si può cancellare per rifare i tentativi).
---
## 3. File “ufficiale” da usare in altri progetti
Per qualsiasi **nuova app / backend / servizio** che deve sapere i punti di consegna, usa:
- **`CONSEGNE/CONSEGNE_<data>/punti_consegna_unificati.json`**
Struttura (semplificata):
```json
{
  "data_consegna": "16-03-2026",
  "punti": [
    {
      "nome": "Scuola X",
      "tipologia": "",
      "indirizzo": "Via ..., CAP Città (PV)",
      "lat": 45.123,
      "lon": 12.345,
      "codice_frutta": "p1234",
      "codice_latte": "p5678",
      "orario_min": "08:00",
      "orario_max": "10:00",
      "codici_ddt_frutta": ["p1234"],
      "codici_ddt_latte": ["p5678"],
      "data_consegna": "16-03-2026",
      "geo_query_nome_indirizzo": "Nome + indirizzo",
      "geo_query_indirizzo": "Solo indirizzo"
    }
  ]
}
Questo JSON è la “API dati” del progetto CONSEGNE.

4. Batch disponibili
Nella root del progetto:

avvia_estrai_ddt_consegne.bat

Uso:
avvia_estrai_ddt_consegne.bat 16-03-2026
Effetto:
Estrae DDT singoli
Crea punti_consegna_frutta.xlsx e punti_consegna_latte.xlsx
Crea punti_consegna_unificati.json per quella data
avvia_mappa_consegne.bat

Uso:
avvia_mappa_consegne.bat 16-03-2026
oppure solo avvia_mappa_consegne.bat (se esiste una sola cartella CONSEGNE_<data>)
Effetto:
Legge punti_consegna_unificati.json
Crea/aggiorna mappa_consegne_<data>.html, consegne_app_<data>.html, punti_consegna_<data>.kml
5. Cosa è “di prova” e può essere cancellato / rigenerato
Per ogni data CONSEGNE_<data>:

Dati “sorgente / ufficiali”

DDT-ORIGINALI-DIVISI\FRUTTA\ e LATTE\
punti_consegna_frutta.xlsx
punti_consegna_latte.xlsx
punti_consegna_unificati.json ← usare questo nei nuovi progetti
Output di servizio (rigenerabili)

mappa_consegne_<data>.html
consegne_app_<data>.html
punti_consegna_<data>.kml
Se si cancellano gli HTML/KML, basta rilanciare avvia_mappa_consegne.bat per ricrearli.

6. Come collegare questo progetto da un altro
Opzioni tipiche:

Stesso workspace
Aprire la stessa cartella (c:\Gestione DDT viaggi\) nel nuovo progetto → il nuovo agente vede direttamente tutto.

Cartella condivisa dati
Spostare CONSEGNE\ e gli script comuni in una cartella condivisa (es. c:\Gestione condivisa DDT\) e leggere i file da lì tramite percorsi assoluti.

Solo JSON
Nel nuovo progetto leggere direttamente:

c:\Gestione DDT viaggi\CONSEGNE\CONSEGNE_<data>\punti_consegna_unificati.json
e costruire l’app/servizio sopra questi dati.
Fine note CONSEGNE.


# Modulo Geocoding - Gestione DDT Viaggi

Converte indirizzi in coordinate GPS (lat/lon) tramite Nominatim (OpenStreetMap).

## Installazione

```bat
pip install -r requirements.txt
```

## Esecuzione principale (mappatura_destinazioni.xlsx)

```bat
cd geocoding_project
python geocoding_consegne.py
```

- Input/Output: `mappatura_destinazioni.xlsx` (cartella padre)
- Cache: `geocode_cache.json` (evita richieste ripetute)
- Report non trovati: `geocode_report_non_trovati.xlsx`
- Colonne risultato: M=Latitudine, N=Longitudine, O=Stato geocoding

## Struttura

```
geocoding_project/
├── geocoding_consegne.py   ← script principale
├── src/
│   ├── geocoder_consegne.py  (cache, Excel, report)
│   └── geocoder.py           (modulo base)
├── data/                     (opzionale, per test)
└── requirements.txt
```

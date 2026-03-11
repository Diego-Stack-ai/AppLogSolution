# Struttura cartelle

```
Gestione DDT viaggi/
├── avvia_distinta.bat          # Avvio principale (distinta + DDT originali)
├── mappatura_destinazioni.xlsx # Mappatura codici (input)
├── mappatura_destinazioni - da aggiustare.xlsx
├── rientri_ddt.xlsx            # Rientri da integrare (input)
├── DDT frutta/                 # PDF DDT frutta (input)
├── DDT latte/                  # PDF DDT latte (input)
├── Giri lavorati/              # Output: DDT-{data}/, RIEPILOGO/, DDT-ORIGINALI/
│
├── nuovi_codici_consegna.xlsx       # Report codici non in mappatura
├── report_orari_mancanti.xlsx       # Report orari da aggiornare
├── report_rientri_non_integrabili.xlsx
├── geocode_cache.json               # Cache geocoding
├── geocode_report_non_trovati.xlsx
│
└── Programma/                       # Script
    ├── crea_distinta_magazzino.py
    ├── crea_ddt_originali.py
    ├── allinea_nomi_mappatura.py
    ├── allinea_nomi_completati.txt
    ├── requirements.txt
    │
    └── geocoding_project/
        ├── geocoding_consegne.py
        ├── src/geocoder_consegne.py
        └── ...
```

## Esecuzione script

| Script | Comando |
|--------|---------|
| Distinta + DDT | `avvia_distinta.bat` |
| Allinea nomi | `py -3 Programma\allinea_nomi_mappatura.py` |
| Geocoding | `py -3 Programma\geocoding_project\geocoding_consegne.py` |

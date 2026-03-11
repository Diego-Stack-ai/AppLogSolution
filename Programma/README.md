# Gestione DDT Viaggi

Sistema per la gestione delle consegne frutta/latte alle scuole: distinte magazzino, DDT per territorio, rientri, geocoding.

## Avvio

```batch
avvia_distinta.bat
```

Esegue: `crea_distinta_magazzino` → `crea_ddt_originali`

## Struttura

Vedi **STRUCTURA.md** (root) per la mappa completa.

- **Programma/** – Script, cache geocode, report (nuovi_codici, report_orari, report_rientri)

## Integrazione GitHub

Repository: [Diego-Stack-ai/Gestione-DDT-Viaggi](https://github.com/Diego-Stack-ai/Gestione-DDT-Viaggi)

### Salvataggio modifiche

```batch
git add .
git commit -m "Descrizione modifiche"
git push
```

## Altri script

| Script | Comando |
|--------|---------|
| Allinea nomi | `avvia_allinea_nomi.bat` oppure `py -3 Programma\allinea_nomi_mappatura.py` |
| Geocoding | `avvia_geocoding.bat` oppure `py -3 Programma\geocoding_project\geocoding_consegne.py` |

## Documentazione

- **DOCUMENTAZIONE_ESTRAZIONE_PDF.md** – Estrazione dati dal PDF (destinatario, indirizzo, zona, orari)

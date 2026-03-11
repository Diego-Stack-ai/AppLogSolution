#!/usr/bin/env python3
"""
Geocoding indirizzi di consegna (600-700 scuole).
- Legge Excel con codice, nome, indirizzo, CAP, città, provincia
- Geocodifica solo i NUOVI indirizzi (cache)
- Salva lat/lon nel file Excel
- Report indirizzi non trovati: geocode_report_non_trovati.xlsx
"""
import sys
from pathlib import Path

# Path progetto
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from geocoder_consegne import process_excel

# Configurazione: tutto in root (Gestione DDT viaggi)
ROOT_DIR = PROJECT_DIR.parent.parent
INPUT_EXCEL = ROOT_DIR / "mappatura_destinazioni.xlsx"
CACHE_PATH = ROOT_DIR / "geocode_cache.json"
REPORT_PATH = ROOT_DIR / "geocode_report_non_trovati.xlsx"
# Oppure un file nella cartella data:
# INPUT_EXCEL = PROJECT_DIR / "data" / "indirizzi_consegne.xlsx"


def main():
    if not INPUT_EXCEL.exists():
        print(f"File non trovato: {INPUT_EXCEL}")
        print("Modifica INPUT_EXCEL in geocoding_consegne.py con il path corretto.")
        return 1

    print("Geocoding indirizzi di consegna")
    print(f"Input: {INPUT_EXCEL}")
    print("(Cache: geocode_cache.json nella cartella principale - non ripete richieste per indirizzi già fatti)")
    print()

    stats = process_excel(
        input_path=INPUT_EXCEL,
        output_path=INPUT_EXCEL,  # sovrascrive con lat/lon in colonne M, N, O
        cache_path=CACHE_PATH,
        report_path=REPORT_PATH,
        sheet_name=0,  # primo foglio
    )

    print(f"Righe totali:     {stats['total_rows']}")
    print(f"Nuovi geocodificati: {stats['geocoded_new']}")
    print(f"Da cache:         {stats['from_cache']}")
    print(f"Non trovati:      {stats['not_found']}")
    if stats["not_found"] > 0:
        print(f"\nReport non trovati: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

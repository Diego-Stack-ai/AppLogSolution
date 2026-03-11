"""
Script principale per il geocoding degli indirizzi.
Legge da data/input_addresses.xlsx e salva in data/geocoded_addresses.xlsx.
"""
import sys
from pathlib import Path

# Aggiunge la cartella src al path
SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
INPUT_FILE = DATA_DIR / "input_addresses.xlsx"
OUTPUT_FILE = DATA_DIR / "geocoded_addresses.xlsx"

from geocoder import geocode_dataframe, load_addresses, save_geocoded


def main():
    print("Geocoding indirizzi - Nominatim (OpenStreetMap)")
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()

    if not INPUT_FILE.exists():
        print(f"ERRORE: File di input non trovato: {INPUT_FILE}")
        print("        Creare input_addresses.xlsx con colonne: street, house_number, postal_code, city, province")
        return 1

    df = load_addresses(INPUT_FILE)
    print(f"Indirizzi da processare: {len(df)}")

    # Colonne attese (con alias per flessibilità)
    required = ["street", "postal_code", "city", "province"]
    for col in required:
        if col not in df.columns:
            print(f"ERRORE: Colonna mancante: {col}")
            return 1

    # house_number opzionale
    if "house_number" not in df.columns:
        df["house_number"] = ""

    result = geocode_dataframe(df)
    save_geocoded(result, OUTPUT_FILE)

    found = result["latitude"].notna().sum()
    print(f"\nCompletato: {found}/{len(result)} indirizzi geocodificati.")
    print(f"Salvato in: {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

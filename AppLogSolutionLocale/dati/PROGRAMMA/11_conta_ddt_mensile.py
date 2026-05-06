#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERRORE: Libreria pdfplumber mancante. Esegui: pip install pdfplumber")
    sys.exit(1)

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"

# Codici area speciali
SPECIALI_FRUTTA = {"3198", "3199"}
SPECIALI_LATTE  = {"4199"}

# Regex per trovare il codice area (es: G3109 o Q4199)
AREA_RE = re.compile(r'(?:conto di|ordine e conto di)\s+([A-Z])(\d{4,5})', re.I)

def estrai_codice_area(pdf_path):
    """Apre il PDF ed estrae il numero del codice area."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text() or ""
            match = AREA_RE.search(text)
            if match:
                return match.group(2)
    except:
        pass
    return None

def main():
    print("\n" + "="*65)
    print("   CONTEGGIO DDT MENSILE - FRUTTA vs LATTE")
    print("="*65)

    mese = input("\nInserisci il mese da cercare (es. 04): ").strip()
    if not mese or len(mese) != 2:
        print("Mese non valido.")
        return

    anno = "2026"
    pattern_mese = f"-{mese}-{anno}"

    cartelle_mese = []
    if not CONSEGNE_DIR.exists(): return
    for d in CONSEGNE_DIR.iterdir():
        if d.is_dir() and d.name.startswith("CONSEGNE_") and pattern_mese in d.name:
            cartelle_mese.append(d)

    if not cartelle_mese:
        print(f"Nessuna cartella per {mese}/{anno}.")
        return

    # Contatori
    stats = {
        "FRUTTA": {"standard": 0, "speciali": 0, "dettaglio": {"3198": 0, "3199": 0}},
        "LATTE":  {"standard": 0, "speciali": 0, "dettaglio": {"4199": 0}}
    }
    orfani = 0

    print(f"\nScansione in corso...")

    for cartella in sorted(cartelle_mese):
        divisi = cartella / "DDT-ORIGINALI-DIVISI"
        if not divisi.exists(): continue
        
        for tipo in ["FRUTTA", "LATTE"]:
            folder_tipo = divisi / tipo
            if not folder_tipo.exists(): continue
            
            pdfs = list(folder_tipo.glob("*.pdf"))
            print(f"  - {cartella.name} [{tipo}]: {len(pdfs)} file", end="\r")
            
            for p in pdfs:
                area = estrai_codice_area(p)
                
                if tipo == "FRUTTA":
                    if area in SPECIALI_FRUTTA:
                        stats["FRUTTA"]["speciali"] += 1
                        stats["FRUTTA"]["dettaglio"][area] += 1
                    else:
                        stats["FRUTTA"]["standard"] += 1
                        if not area: orfani += 1
                else: # LATTE
                    if area in SPECIALI_LATTE:
                        stats["LATTE"]["speciali"] += 1
                        stats["LATTE"]["dettaglio"][area] += 1
                    else:
                        stats["LATTE"]["standard"] += 1
                        if not area: orfani += 1

    print("\n" + "-"*65)
    print(f" RIEPILOGO MENSILE {mese}/{anno}")
    print("-" * 65)

    print(f"\n SEZIONE FRUTTA")
    print(f"   - DDT Standard Frutta:     {stats['FRUTTA']['standard']}")
    print(f"   - DDT Speciali (3198/3199): {stats['FRUTTA']['speciali']}")
    if stats['FRUTTA']['speciali'] > 0:
        print(f"     [Dettaglio: Area 3198={stats['FRUTTA']['dettaglio']['3198']} | Area 3199={stats['FRUTTA']['dettaglio']['3199']}]")

    print(f"\n SEZIONE LATTE")
    print(f"   - DDT Standard Latte:      {stats['LATTE']['standard']}")
    print(f"   - DDT Speciali (4199):      {stats['LATTE']['speciali']}")

    tot_totale = stats['FRUTTA']['standard'] + stats['FRUTTA']['speciali'] + \
                 stats['LATTE']['standard'] + stats['LATTE']['speciali']
    
    print("\n" + "-"*65)
    print(f" TOTALE GENERALE MESE: {tot_totale} DDT")
    if orfani > 0:
        print(f"  Attenzione: {orfani} DDT senza codice area (conteggiati come Standard)")
    print("="*65 + "\n")
    input("Premi INVIO per uscire...")

if __name__ == "__main__":
    main()

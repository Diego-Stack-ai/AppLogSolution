#!/usr/bin/env python3
"""Lista tutti i DDT che contengono FVNS-03-FOLDER e FVNS-03-MAGAZINE."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pdfplumber
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DDT_DIR = BASE / "CONSEGNE" / "CONSEGNE_13-04-2026" / "DDT-ORIGINALI-DIVISI"

risultati = {"FVNS-03-FOLDER": [], "FVNS-03-MAGAZINE": []}

for sub in sorted(DDT_DIR.iterdir()):
    if not sub.is_dir():
        continue
    for pdf_path in sorted(sub.glob("*.pdf")):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("FVNS-03-") and i + 1 < len(lines):
                            next_word = lines[i+1].strip().split()[0] if lines[i+1].strip() else ""
                            full_code = f"FVNS-03-{next_word}"
                            if full_code in risultati:
                                codice_punto = pdf_path.stem.split("_")[0]  # es. p2128
                                risultati[full_code].append(f"{pdf_path.name} ({sub.name}) -> punto {codice_punto}")
        except:
            pass

print("=== DDT contenenti FVNS-03-FOLDER ===")
if risultati["FVNS-03-FOLDER"]:
    for r in risultati["FVNS-03-FOLDER"]:
        print(f"  {r}")
    print(f"  TOTALE: {len(risultati['FVNS-03-FOLDER'])} DDT")
else:
    print("  Nessuno trovato")

print(f"\n=== DDT contenenti FVNS-03-MAGAZINE ===")
if risultati["FVNS-03-MAGAZINE"]:
    for r in risultati["FVNS-03-MAGAZINE"]:
        print(f"  {r}")
    print(f"  TOTALE: {len(risultati['FVNS-03-MAGAZINE'])} DDT")
else:
    print("  Nessuno trovato")

# Riepilogo
print(f"\n=== RIEPILOGO ===")
print(f"FVNS-03-FOLDER:   {len(risultati['FVNS-03-FOLDER'])} DDT")
print(f"FVNS-03-MAGAZINE: {len(risultati['FVNS-03-MAGAZINE'])} DDT")

# Verifica: ci sono DDT dove appaiono ENTRAMBI?
folder_files = {r.split(" ")[0] for r in risultati["FVNS-03-FOLDER"]}
magazine_files = {r.split(" ")[0] for r in risultati["FVNS-03-MAGAZINE"]}
entrambi = folder_files & magazine_files
if entrambi:
    print(f"\nDDT con ENTRAMBI ({len(entrambi)}): {', '.join(sorted(entrambi))}")

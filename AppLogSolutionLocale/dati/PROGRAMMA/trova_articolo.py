#!/usr/bin/env python3
"""Lista tutti i DDT che contengono FVNS-03-FOLDER e FVNS-03-MAGAZINE."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pdfplumber
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DDT_DIR = BASE / "CONSEGNE" / "CONSEGNE_13-04-2026" / "DDT-ORIGINALI-DIVISI"

# --- SORGENTE DI VERITÀ ---
ARTICOLI_NOTI = {
    "10-FLYER", "10-GEL", "10-MANIFESTO", "10-AT-01", "10-BICC", "10-CUCCH", "10-PIATTO",
    "AP-SU-PC", "FO-DI-PV-04-LB", "FO-DI-GP-01-NI", "FVNS-03", "FVNS-03-", 
    "LT-AQ-04-LV", "LT-AQ-04-LB", "LT-AQ-04-LS", "LT-DL-02-LC", "LT-ES-04-LS", "LT-ESL-IN-LB", 
    "MA-T-LI-L3-NA", "ME-T-DI-V0-NA", "ME-S-BI-L3-NA", "PE-T-DI-L3-NA",
    "YO-BI-MN-04-LB", "YO-DL-02-LC", "FI-Z-BI-L3-NA", "FR-M-BI-L3-NI",
    "LNS-04-GADGET", "LNS-04-", "CA-Z-BI-L3-NA", "KI-S-BI-L3-NA"
}

def is_primary_code(text):
    if not text: return False
    text = text.strip().upper()
    if text in ARTICOLI_NOTI: return True
    for prefix in ARTICOLI_NOTI:
        if prefix.endswith('-') and text.startswith(prefix):
            return True
    return False

# Codici da cercare (Esempio: ora puoi cercare il codice COMPLETO)
CERCASI = ["FVNS-03-FOLDER", "FVNS-03-MAGAZINE", "LNS-04-GADGET", "LNS-04-POSTER"]
risultati = {c: [] for c in CERCASI}

print(f"Ricerca articoli {CERCASI} in corso...")

for sub in sorted([d for d in DDT_DIR.iterdir() if d.is_dir()]):
    for pdf_path in sorted(sub.glob("*.pdf")):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for tab in tables:
                        if not tab or len(tab) < 2: continue
                        current_block = None
                        for row in tab[1:]:
                            if not row or not row[0]: continue
                            lines = [l.strip() for l in str(row[0]).split('\n') 
                                     if l.strip() and not l.strip().startswith("Codice:")]
                            if not lines: continue
                            
                            if is_primary_code(lines[0]):
                                current_block = lines
                            elif current_block:
                                current_block.extend(lines)
                            
                            if current_block:
                                full_code = "-".join(current_block).replace("--", "-")
                                full_code = re.sub(r'-+', '-', full_code).strip('-')
                                if full_code in risultati:
                                    info = f"{pdf_path.name} ({sub.name}) -> {pdf_path.stem.split('_')[0]}"
                                    if info not in risultati[full_code]:
                                        risultati[full_code].append(info)
        except: continue

for code, ddt_list in risultati.items():
    print(f"\n=== DDT contenenti {code} ===")
    if ddt_list:
        for r in ddt_list: print(f"  {r}")
        print(f"  TOTALE: {len(ddt_list)} DDT")
    else: print("  Nessuno trovato")


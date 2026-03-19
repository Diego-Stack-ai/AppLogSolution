#!/usr/bin/env python3
import sys
from pathlib import Path
import pdfplumber
import re

BASE_GIRI = Path(r"c:\Gestione DDT viaggi\Giri lavorati")
TARGET_DATES = ["12-03-2026", "16-03-2026", "17-03-2026", "18-03-2026", "19-03-2026"]
TARGET_CODES = ["FO-DI-PV-04-LB", "FO-DI-GP-01-NI"]

def analizza_pdf(pdf_path):
    risultati = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_idx, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if not tables:
                    continue
                for t in tables:
                    if not t or len(t) < 2:
                        continue
                    # Cerchiamo la riga con il codice
                    for row in t[1:]:
                        if not row or len(row) < 4:
                            continue
                        cell0 = str(row[0] or "").strip()
                        # Match del codice (può contenere "Codice: ...")
                        if any(tc in cell0 for tc in TARGET_CODES):
                            codice_trovato = next(tc for tc in TARGET_CODES if tc in cell0)
                            qty_raw = str(row[3] or "").strip().replace("\n", " ")
                            conf_raw = str(row[5] or "").strip().replace("\n", " ") if len(row) > 5 else "-"
                            risultati.append({
                                "file": pdf_path.name,
                                "codice": codice_trovato,
                                "qty": qty_raw,
                                "conf": conf_raw
                            })
    except Exception as e:
        print(f"Errore su {pdf_path.name}: {e}")
    return risultati

def main():
    print(f"Analisi articoli {TARGET_CODES} nei DDT dal 12 al 19 Marzo...\n")
    tot_trovati = []
    
    for date_str in TARGET_DATES:
        folder = BASE_GIRI / f"DDT-{date_str}" / "DDT-ORIGINALI"
        if not folder.exists():
            print(f"Cartella non trovata: {folder}")
            continue
        
        print(f"Scansione {date_str}...")
        pdfs = list(folder.glob("*.pdf"))
        for p in pdfs:
            res = analizza_pdf(p)
            tot_trovati.extend(res)

    print("\nRISULTATI ESTRAZIONE:")
    print("-" * 100)
    print(f"{'Codice':<20} | {'Quantità (Grezza)':<30} | {'Confezionamento'}")
    print("-" * 100)
    
    visti = set()
    for r in tot_trovati:
        chiave = (r['codice'], r['qty'], r['conf'])
        if chiave not in visti:
            print(f"{r['codice']:<20} | {r['qty']:<30} | {r['conf']}")
            visti.add(chiave)

if __name__ == "__main__":
    main()

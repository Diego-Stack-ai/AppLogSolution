import pdfplumber
import sys
from pathlib import Path
import re

def find_novembre():
    base_dir = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\CONSEGNE")
    folders = list(base_dir.rglob("DDT-ORIGINALI-DIVISI"))
    if not folders:
        print("Nessuna cartella trovata")
        return
        
    for folder in folders:
        pdfs = list(folder.rglob("*.pdf"))
        print(f"[{folder.parent.name}] Trovati {len(pdfs)} PDF divisi.", flush=True)
        
        for p in pdfs:
            try:
                with pdfplumber.open(p) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text and "NOVEMBRE" in text.upper():
                            print(f"\n>>>> HO TROVATO 'NOVEMBRE' NEL FILE: {p}")
                            lines = text.split("\n")
                            for line in lines:
                                if "NOVEMBRE" in line.upper():
                                    print("  >>", line)
                                else:
                                    print("    ", line)
                            
                            # Cerchiamo codice destinazione
                            matches = re.findall(r"p\d{4,5}", text, re.I)
                            print(f"Codici papabili trovati in questo file: {set(matches)}")
            except Exception as e:
                pass

if __name__ == "__main__":
    find_novembre()

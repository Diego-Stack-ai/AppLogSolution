import os
import re
import pdfplumber
from pathlib import Path

base_dir = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\CONSEGNE\CONSEGNE_15-04-2026\DDT-ORIGINALI-DIVISI")

zone_trovate = set()

for subdir in ["FRUTTA", "LATTE"]:
    folder = base_dir / subdir
    if not folder.exists():
        continue
    for f in folder.glob("*.pdf"):
        try:
            with pdfplumber.open(f) as pdf:
                text = pdf.pages[0].extract_text()
                # Cerchiamo vari pattern, es: G3203, Q3204.
                # A volte c'è una lettera seguita da 4 cifre
                match = re.search(r"conto di\s+([A-Z]?)(\d{4})", text, re.IGNORECASE)
                if match:
                    zona = match.group(2)
                    zone_trovate.add(zona)
                else:
                    # Alternativa, cerchiamo semplicemente un blocco di 4 cifre dopo "conto di"
                    match_alt = re.search(r"conto di\s+.*?(\d{4})", text, re.IGNORECASE)
                    if match_alt:
                        zona = match_alt.group(1)
                        zone_trovate.add(zona)
        except Exception as e:
            print(f"Errore su {f.name}: {e}")

print("ZONE REALMENTE TROVATE NEI PDF:")
print(sorted(list(zone_trovate)))

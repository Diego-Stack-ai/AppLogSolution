#!/usr/bin/env python3
"""
Verifica l'estrazione del campo "A chi va consegnato" dal PDF DDT.
Esegui: py -3 Programma/verifica_estrazione_destinatario.py

Mostra le prime righe estratte dal blocco "Luogo di destinazione" per verificare
che destinatario = lines[i+1] e indirizzo = lines[i+2] siano corretti.
"""
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("pip install pdfplumber")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
DDT_FRUTTA = BASE_DIR / "DDT frutta"
DDT_LATTE = BASE_DIR / "DDT latte"
LUOGO_RE = re.compile(r'[Ll]uogo [Dd]i [Dd]estinazione:\s*(p\d{4,5})')


def _estrai_blocco(text: str) -> list[str]:
    """Stesso filtro di crea_distinta_magazzino."""
    idx = text.find("Luogo di destinazione")
    if idx < 0:
        return []
    blocco = text[idx : idx + 650]
    return [ln.strip() for ln in blocco.split("\n") if ln.strip() and not ln.strip().upper().startswith("RESPONSABILE")]


def main():
    pdfs = list(DDT_FRUTTA.glob("*.pdf")) if DDT_FRUTTA.exists() else []
    if not pdfs:
        pdfs = list(DDT_LATTE.glob("*.pdf")) if DDT_LATTE.exists() else []
    if not pdfs:
        print("Nessun PDF in DDT frutta o DDT latte.")
        return 1

    pdf_path = sorted(pdfs)[0]
    print(f"Analisi: {pdf_path.name}\n")

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages[:3]):  # prime 3 pagine
            text = page.extract_text() or ""
            lines = _estrai_blocco(text)
            if not lines:
                continue

            print(f"--- Pagina {page_idx + 1} ---")
            for i, ln in enumerate(lines[:10]):
                marker = ""
                if LUOGO_RE.search(ln):
                    marker = "  ← LUOGO_RE (destinatario=riga successiva)"
                elif i > 0 and LUOGO_RE.search(lines[i - 1]):
                    marker = "  ← DESTINATARIO (A chi va consegnato)"
                elif i > 1 and LUOGO_RE.search(lines[i - 2]):
                    marker = "  ← INDIRIZZO"
                print(f"  {i}: {ln[:70]}{marker}")
            print()

    print("Verifica: se DESTINATARIO non è il nome scuola, il layout PDF è diverso dall'atteso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

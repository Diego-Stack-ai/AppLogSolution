#!/usr/bin/env python3
"""
Confronta la struttura del blocco "Luogo di destinazione" tra PDF frutta e latte.
Esegui: py -3 Programma/verifica_struttura_frutta_vs_latte.py

Verifica se dopo "Luogo di destinazione: pXXXX" c'è:
- Frutta: nome cliente
- Latte: Cf (codice fiscale)
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

# Possibili pattern CF (Codice Fiscale)
CF_LIKE = re.compile(r'^(Cf|C\.F\.|CF|Partita\s+Iva|P\.?\s*I\.?)\s*[:\s]', re.I)
CF_16_CHARS = re.compile(r'^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$', re.I)


def _estrai_blocco(text: str) -> list[str]:
    idx = text.find("Luogo di destinazione")
    if idx < 0:
        return []
    blocco = text[idx : idx + 650]
    return [ln.strip() for ln in blocco.split("\n") if ln.strip() and not ln.strip().upper().startswith("RESPONSABILE")]


def _assomiglia_cf(riga: str) -> bool:
    """Riga potrebbe essere CF/Partita Iva."""
    if not riga or len(riga) > 50:
        return False
    if CF_LIKE.match(riga):
        return True
    # CF italiano: 16 caratteri alfanumerici
    s = riga.replace(" ", "").replace(".", "")
    if len(s) == 16 and s.isalnum():
        return True
    return False


def analizza_pdf(pdf_path: Path, etichetta: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {etichetta}: {pdf_path.name}")
    print('='*60)

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages[:2]):
            text = page.extract_text() or ""
            lines = _estrai_blocco(text)
            if not lines:
                continue
            print(f"\n  --- Pagina {page_idx + 1} ---")
            for i, ln in enumerate(lines[:12]):
                marker = ""
                if LUOGO_RE.search(ln):
                    marker = "  [LUOGO]"
                elif i > 0 and LUOGO_RE.search(lines[i - 1]):
                    is_cf = _assomiglia_cf(ln)
                    marker = "  [riga dopo LUOGO]" + ("  <<< CF?" if is_cf else "  <<< NOME?")
                elif i > 1 and LUOGO_RE.search(lines[i - 2]):
                    marker = "  [2 righe dopo]"
                elif i > 2 and LUOGO_RE.search(lines[i - 3]):
                    marker = "  [3 righe dopo]"
                print(f"    {i}: {ln[:65]}{marker}")


def main():
    pdf_frutta = list(DDT_FRUTTA.glob("*.pdf")) if DDT_FRUTTA.exists() else []
    pdf_latte = list(DDT_LATTE.glob("*.pdf")) if DDT_LATTE.exists() else []

    if not pdf_frutta:
        print("Nessun PDF in DDT frutta")
    else:
        analizza_pdf(sorted(pdf_frutta)[0], "FRUTTA")

    if not pdf_latte:
        print("Nessun PDF in DDT latte")
    else:
        analizza_pdf(sorted(pdf_latte)[0], "LATTE")

    print("\n" + "="*60)
    print("Se in LATTE la riga dopo LUOGO è CF, serve logica diversa per destinatario.")
    print("="*60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

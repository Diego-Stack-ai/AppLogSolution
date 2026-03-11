#!/usr/bin/env python3
"""
Scompose i PDF frutta e latte in DDT singoli (un file per pagina).
Eseguito dopo crea_distinta_magazzino: usa i file in {data}-DDT-ORIGINALI.
Nome file: {data}_p{luogo}.pdf (es. 10-03-2026_p3123.pdf).
Duplicati (stesso data+luogo) non vengono creati. Elimina i file originali (multi-pagina) alla fine.
"""

import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("pip install pypdf")
    sys.exit(1)

# Cartella principale (parent di Programma/)
BASE_DIR = Path(__file__).parent.parent
GIRI_LAVORATI_DIR = BASE_DIR / "Giri lavorati"

DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'[Ll]uogo [Dd]i [Dd]estinazione:\s*([pP]\d{4,5})')


def _estrai_data_luogo(text: str) -> tuple[str | None, str | None]:
    """Estrae (data, luogo) da una pagina DDT. data in formato DD-MM-YYYY."""
    data = None
    m = DATA_DDT_RE.search(text)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    luogo_m = LUOGO_RE.search(text)
    luogo = luogo_m.group(1).lower() if luogo_m else None
    return (data, luogo)


def _trova_cartella_originali() -> Path | None:
    """Trova in Giri lavorati la cartella DDT-ORIGINALI più recente (cartella DDT-(data) con data modifica maggiore)."""
    if not GIRI_LAVORATI_DIR.exists():
        return None
    cartelle_ddt = [d for d in GIRI_LAVORATI_DIR.iterdir() if d.is_dir() and d.name.startswith("DDT-")]
    if not cartelle_ddt:
        return None
    cartella_recente = max(cartelle_ddt, key=lambda p: p.stat().st_mtime)
    orig = cartella_recente / "DDT-ORIGINALI"
    return orig if orig.exists() else None


def _pdf_originali(cartella: Path) -> list[Path]:
    """Ritorna i PDF multi-pagina da scomporre (i 2 file messi da crea_distinta)."""
    pdfs = []
    for p in cartella.glob("*.pdf"):
        try:
            n = len(PdfReader(p).pages)
            if n > 1:
                pdfs.append(p)
        except Exception:
            pass
    return pdfs


def main():
    originali_dir = _trova_cartella_originali()
    if not originali_dir:
        print("Nessuna cartella DDT-ORIGINALI trovata. Eseguire prima crea_distinta_magazzino.")
        return

    pdf_originali = _pdf_originali(originali_dir)
    if not pdf_originali:
        print(f"{originali_dir.name}: nessun PDF multi-pagina da scomporre.")
        return

    print(f"\n--- crea_ddt_originali: {originali_dir.name} ---")
    creati = 0
    saltati_duplicati = 0
    saltati_senza_dati = 0
    visti: set[tuple[str, str]] = set()

    for pdf_path in pdf_originali:
        try:
            reader = PdfReader(pdf_path)
        except Exception as e:
            print(f"  Errore lettura {pdf_path.name}: {e}")
            continue

        try:
            import pdfplumber
        except ImportError:
            print("  pip install pdfplumber (necessario per estrarre data/luogo)")
            return

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                data, luogo = _estrai_data_luogo(text)
                if not data or not luogo:
                    saltati_senza_dati += 1
                    continue
                chiave = (data, luogo)
                if chiave in visti:
                    saltati_duplicati += 1
                    continue
                visti.add(chiave)

                nome_file = f"{data}_{luogo}.pdf"
                out_path = originali_dir / nome_file
                try:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    with open(out_path, "wb") as f:
                        writer.write(f)
                    creati += 1
                except Exception as e:
                    print(f"  Errore salvataggio {nome_file}: {e}")

    # Elimina i file originali (multi-pagina)
    eliminati = 0
    for p in pdf_originali:
        try:
            p.unlink()
            eliminati += 1
            print(f"  Eliminato: {p.name}")
        except Exception as e:
            print(f"  Errore eliminazione {p.name}: {e}")

    print(f"\nCreati {creati} DDT singoli. Saltati {saltati_duplicati} duplicati, {saltati_senza_dati} senza data/luogo.")
    if eliminati > 0:
        print(f"Eliminati {eliminati} file originali.")


if __name__ == "__main__":
    main()

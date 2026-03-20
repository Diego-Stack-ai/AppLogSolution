#!/usr/bin/env python3
"""
Estrae tutti i DDT dai PDF in CONSEGNE/DDT-ORIGINALI/FRUTTA e LATTE,
salvandoli in CONSEGNE/CONSEGNE_{data}/DDT-ORIGINALI-DIVISI/FRUTTA e LATTE.

Crea automaticamente la struttura:
  CONSEGNE_{data}/
  ├── DDT-ORIGINALI-DIVISI/
  │   ├── FRUTTA/
  │   └── LATTE/
  ├── punti_consegna_frutta.xlsx
  └── punti_consegna_latte.xlsx

Uso: py estrai_ddt_consegne.py [data]
     data opzionale (es. 16-03-2026); se assente, ricavata dal primo PDF.

FRUTTA: DDT doppi - solo pagine dispari. LATTE: tutte le pagine.
I file originali NON vengono modificati.
"""

import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("pip install pypdf")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
INPUT_FRUTTA = BASE_DIR / "FRUTTA"
INPUT_LATTE = BASE_DIR / "LATTE"

DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'(?:[Ll]uogo [Dd]i [Dd]estinazione|[Cc]odice [Dd]estinazione):\s*([pP]\d{4,5})')


def _estrai_data_luogo(text: str) -> tuple[str | None, str | None]:
    """Estrae (data, luogo) da una pagina DDT. data in formato DD-MM-YYYY."""
    data = None
    m = DATA_DDT_RE.search(text)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    luogo_m = LUOGO_RE.search(text)
    luogo = luogo_m.group(1).lower() if luogo_m else None
    return (data, luogo)


def _ricava_data_da_pdf() -> str | None:
    """Ricava la data dal primo PDF in FRUTTA o LATTE."""
    import pdfplumber
    for cart in (INPUT_FRUTTA, INPUT_LATTE):
        if not cart.exists():
            continue
        for pdf_path in sorted(cart.glob("*.pdf")):
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        data, _ = _estrai_data_luogo(text)
                        if data:
                            return data
            except Exception:
                pass
    return None


def _estrai_da_cartella(
    cartella_input: Path,
    cartella_output: Path,
    etichetta: str,
    data_consegna: str,
    *,
    frutta_duplicata: bool = False,
) -> tuple[int, int, int, int]:
    """
    Estrae DDT da tutti i PDF nella cartella input, salva in output.
    frutta_duplicata=True: solo pagine dispari (1,3,5...) con verifica che la pari successiva sia identica.
    Ritorna (creati, saltati_duplicati, saltati_senza_dati, coppie_verificate).
    """
    if not cartella_input.exists():
        print(f"  Cartella non trovata: {cartella_input}")
        return (0, 0, 0, 0)

    cartella_output.mkdir(parents=True, exist_ok=True)
    pdf_files = list(cartella_input.glob("*.pdf"))
    if not pdf_files:
        print(f"  Nessun PDF in {cartella_input.name}")
        return (0, 0, 0, 0)

    try:
        import pdfplumber
    except ImportError:
        print("  pip install pdfplumber (necessario per estrarre data/luogo)")
        return (0, 0, 0, 0)

    creati = 0
    saltati_senza_dati = 0
    visti: dict[tuple[str, str], int] = {}
    coppie_verificate = 0
    avvisi_verifica = []

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
        except Exception as e:
            print(f"  Errore lettura {pdf_path.name}: {e}")
            continue

        with pdfplumber.open(pdf_path) as pdf:
            indici_da_processare = range(0, len(pdf.pages))
            if frutta_duplicata:
                indici_da_processare = range(0, len(pdf.pages), 2)

            for i in indici_da_processare:
                if i >= len(pdf.pages):
                    break
                page = pdf.pages[i]
                text = page.extract_text() or ""
                data, luogo = _estrai_data_luogo(text)
                if not data or not luogo:
                    saltati_senza_dati += 1
                    continue
                
                # FILTRO DATA: se la data del PDF non è quella richiesta, salta
                if data != data_consegna:
                    continue

                if frutta_duplicata and i + 1 < len(pdf.pages):
                    text_pari = pdf.pages[i + 1].extract_text() or ""
                    data_pari, luogo_pari = _estrai_data_luogo(text_pari)
                    if data_pari and luogo_pari and data == data_pari and luogo == luogo_pari:
                        coppie_verificate += 1
                    else:
                        avvisi_verifica.append(
                            f"    ATTENZIONE: pagina {i+2} diversa da {i+1} "
                            f"(dispari={luogo}_{data}, pari={luogo_pari or '?'}_{data_pari or '?'})"
                        )

                chiave = (data, luogo)
                contatore = visti.get(chiave, 0) + 1
                visti[chiave] = contatore

                if contatore > 1:
                    nome_file = f"{luogo}_{data}_{contatore}.pdf"
                else:
                    nome_file = f"{luogo}_{data}.pdf"

                out_path = cartella_output / nome_file
                try:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    with open(out_path, "wb") as f:
                        writer.write(f)
                    creati += 1
                    if creati <= 5 or creati % 20 == 0:
                        print(f"    {nome_file}")
                except Exception as e:
                    print(f"  Errore salvataggio {nome_file}: {e}")

    for avv in avvisi_verifica[:5]:
        print(avv)
    if len(avvisi_verifica) > 5:
        print(f"    ... altri {len(avvisi_verifica) - 5} avvisi")

    return (creati, sum(1 for c in visti.values() if c > 1), saltati_senza_dati, coppie_verificate)


def main():
    data_arg = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if data_arg and re.match(r"^\d{2}-\d{2}$", data_arg):
        data_arg = f"{data_arg}-2026"
    data_consegna = data_arg or _ricava_data_da_pdf()
    if not data_consegna:
        print("Data non specificata e non ricavabile dai PDF. Uso: py estrai_ddt_consegne.py 16-03-2026")
        return 1

    output_base = CONSEGNE_DIR / f"CONSEGNE_{data_consegna}"
    output_frutta = output_base / "DDT-ORIGINALI-DIVISI" / "FRUTTA"
    output_latte = output_base / "DDT-ORIGINALI-DIVISI" / "LATTE"

    print("\n--- Estrazione DDT CONSEGNE (FRUTTA e LATTE) ---\n")
    print(f"Output: {output_base}\n")

    # FRUTTA (DDT doppi: solo pagine dispari 1,3,5...)
    print("FRUTTA (solo pagine dispari - DDT doppi per stampa):")
    print(f"  Input:  {INPUT_FRUTTA}")
    print(f"  Output: {output_frutta}")
    c_f, d_f, s_f, ver_f = _estrai_da_cartella(
        INPUT_FRUTTA, output_frutta, "FRUTTA", data_consegna, frutta_duplicata=True
    )
    print(f"  Creati: {c_f} | Saltati senza data/luogo: {s_f}")
    print(f"  Verifica coppie dispari/pari identiche: {ver_f}")
    print()

    # LATTE (tutte le pagine)
    print("LATTE (tutte le pagine):")
    print(f"  Input:  {INPUT_LATTE}")
    print(f"  Output: {output_latte}")
    c_l, d_l, s_l, ver_l = _estrai_da_cartella(INPUT_LATTE, output_latte, "LATTE", data_consegna)
    print(f"  Creati: {c_l} | Saltati senza data/luogo: {s_l}\n")

    print(f"--- Totale: {c_f + c_l} DDT creati ---")
    
    # Pulizia cartelle di input
    print("\nPulizia cartelle di input...")
    for cartella in (INPUT_FRUTTA, INPUT_LATTE):
        if not cartella.exists():
            continue
        for pdf_path in cartella.glob("*.pdf"):
            try:
                pdf_path.unlink()
                print(f"  Rimosso sorgente: {pdf_path.name}")
            except Exception as e:
                print(f"  Errore rimozione {pdf_path.name}: {e}")
    print("Cartelle di input pulite.\n")


    # Ripristino e potenziamento automatismo: esegui l'intera catena
    if c_f + c_l > 0:
        import subprocess
        scripts = [
            ("2_crea_punti_consegna.py", "Generazione punti consegna..."),
            ("3_crea_lista_unificata.py", "Unificazione punti e rientri..."),
            ("4_crea_mappa_consegne.py", "Generazione mappe e app...")
        ]
        
        for script_name, msg in scripts:
            prog = BASE_DIR / script_name
            if prog.exists():
                print(f"{msg}")
                r = subprocess.run([sys.executable, str(prog), data_consegna], cwd=BASE_DIR)
                if r.returncode != 0:
                    print(f"Errore durante l'esecuzione di {script_name}. Interruzione catena.\n")
                    break
            else:
                print(f"Script {script_name} non trovato. Salto passaggio.\n")
        
        print("\n=== ELABORAZIONE COMPLETA ===\n")


if __name__ == "__main__":
    main()

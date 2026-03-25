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
import subprocess
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
    """
    if not cartella_input.exists():
        print(f"  Cartella non trovata: {cartella_input}")
        return (0, 0, 0, 0)

    cartella_output.mkdir(parents=True, exist_ok=True)
    pdf_files = list(cartella_input.glob("*.pdf"))
    if not pdf_files:
        print(f"  Nessun PDF in {cartella_input.name}")
        return (0, 0, 0, 0)

    import pdfplumber
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

                nome_file = f"{luogo}_{data}_{contatore}.pdf" if contatore > 1 else f"{luogo}_{data}.pdf"
                out_path = cartella_output / nome_file
                
                try:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    with open(out_path, "wb") as f:
                        writer.write(f)
                    creati += 1
                    if creati <= 3 or creati % 50 == 0:
                        print(f"    {nome_file}")
                except Exception as e:
                    print(f"  Errore salvataggio {nome_file}: {e}")

    for avv in avvisi_verifica[:3]:
        print(avv)
    return (creati, sum(1 for c in visti.values() if c > 1), saltati_senza_dati, coppie_verificate)


def _pulisci_sorgenti(cartella_input: Path, data_consegna: str):
    """Rimuove solo i PDF che contengono la data elaborata."""
    import pdfplumber
    rimossi = 0
    for pdf_path in cartella_input.glob("*.pdf"):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                trovata = False
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    d, _ = _estrai_data_luogo(text)
                    if d == data_consegna:
                        trovata = True
                        break
                if trovata:
                    pdf.close()
                    pdf_path.unlink()
                    rimossi += 1
        except Exception as e:
            print(f"  Errore pulizia {pdf_path.name}: {e}")
    return rimossi


def _pulisci_output(output_base: Path, data_consegna: str):
    """
    Elimina i file di output della run precedente per la data indicata,
    garantendo una elaborazione sempre pulita e deterministica.
    NON elimina la sottocartella DDT-ORIGINALI-DIVISI.
    """
    file_da_pulire = [
        output_base / "punti_consegna.xlsx",
        output_base / "punti_consegna_unificati.json",
        output_base / "4_mappa_zone_google.html",
        output_base / f"zone_google_{data_consegna.replace('-', '_')}.kml",
    ]
    rimossi = []
    for f in file_da_pulire:
        if f.exists():
            try:
                f.unlink()
                rimossi.append(f.name)
            except Exception as e:
                print(f"  ⚠️  Impossibile eliminare {f.name}: {e}")
    if rimossi:
        print(f"  🧹 Pulizia run precedente: {', '.join(rimossi)}")
    else:
        print(f"  ✓ Nessun file precedente da pulire.")


def main():
    data_arg = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if data_arg and re.match(r"^\d{2}-\d{2}$", data_arg):
        data_arg = f"{data_arg}-2026"
    
    data_consegna = data_arg or _ricava_data_da_pdf()

    # Se non trovo PDF e non ho passato una data come argomento, mi fermo.
    if not data_consegna:
        print("\n❌ Nessun PDF trovato nelle cartelle sorgente (FRUTTA/LATTE) e nessuna data specificata.")
        print("   Lo script non ha dati da elaborare. Esco.\n")
        return 0

    output_base = CONSEGNE_DIR / f"CONSEGNE_{data_consegna}"
    
    # Se la cartella esiste già e sto cercando di ricrearla automaticamente dai PDF, mi fermo.
    # Se invece l'utente ha passato la data esplicita (data_arg), allora procedo (forzo ricalcolo).
    if output_base.exists() and not data_arg:
        print(f"\n⚠️  La cartella {output_base.name} esiste già.")
        print("   Se vuoi rigenerare i file per questa data, usa: python \"(1_2_3)_estrai_ddt_consegne.py\" " + data_consegna + "\n")
        return 0

    output_frutta = output_base / "DDT-ORIGINALI-DIVISI" / "FRUTTA"
    output_latte = output_base / "DDT-ORIGINALI-DIVISI" / "LATTE"

    print(f"\n{'='*50}")
    print(f"  PIPELINE CONSEGNE — {data_consegna}")
    print(f"{'='*50}\n")

    # STEP 0: pulizia output precedenti → run deterministico
    print("📂 Pulizia output precedenti...")
    _pulisci_output(output_base, data_consegna)
    print()

    print(f"\n--- Estrazione DDT CONSEGNE ({data_consegna}) ---\n", flush=True)
    print(f"Output: {output_base}\n", flush=True)

    print("FRUTTA (solo pagine dispari):")
    c_f, d_f, s_f, ver_f = _estrai_da_cartella(INPUT_FRUTTA, output_frutta, "FRUTTA", data_consegna, frutta_duplicata=True)
    print(f"  Estratti: {c_f} | Verifica coppie: {ver_f}")

    print("LATTE (tutte le pagine):")
    c_l, d_l, s_l, ver_l = _estrai_da_cartella(INPUT_LATTE, output_latte, "LATTE", data_consegna)
    print(f"  Estratti: {c_l}")

    print(f"\n--- Totale: {c_f + c_l} DDT estratti ---")
    
    print("\nPulizia selettiva sorgenti...")
    r = _pulisci_sorgenti(INPUT_FRUTTA, data_consegna) + _pulisci_sorgenti(INPUT_LATTE, data_consegna)
    print(f"Rimossi {r} file sorgente elaborati.\n")

    # Catena completa 2→3→4
    # Il 4 usa --no-serve: genera HTML+KML senza avviare Flask (non blocca)
    # Flask si avvia separatamente con: python 4_mappa_zone_google.py
    scripts = [
        ("2_crea_punti_consegna.py",  [data_consegna],               "⚙️  Creazione punti consegna..."),
        ("3_crea_lista_unificata.py", [data_consegna],               "🔗  Lista unificata e rientri..."),
        ("4_mappa_zone_google.py",    [data_consegna, "--no-serve"], "🗺️  Generazione mappa HTML+KML..."),
    ]

    ok = True
    import time
    for script_name, extra_args, msg in scripts:
        prog = BASE_DIR / script_name
        if not prog.exists():
            print(f"⚠️  {script_name} non trovato. Salto.\n", flush=True)
            continue
        print(msg, flush=True)
        # Piccolo ritardo per permettere al file system (Google Drive) di aggiornarsi
        time.sleep(1.5)
        result = subprocess.run([sys.executable, str(prog)] + extra_args, cwd=BASE_DIR)
        if result.returncode != 0:
            print(f"❌ Errore in {script_name} (exit {result.returncode}). Interruzione.\n", flush=True)
            ok = False
            break

    # CONTROLLO FINALE E POSSIBILE RE-RUN dello script 4 (se Google Drive ha avuto un ritardo)
    json_out = CONSEGNE_DIR / f"CONSEGNE_{data_consegna}" / "punti_consegna_unificati.json"
    mappa_html = CONSEGNE_DIR / f"CONSEGNE_{data_consegna}" / "4_mappa_zone_google.html"
    
    if ok and not mappa_html.exists():
        print("⚠️  Mappa non rilevata sul disco. Attendo sincronizzazione e riprovo...", flush=True)
        time.sleep(3.0)
        if not mappa_html.exists():
            print("🚀 Rilancio generazione mappa (tentativo 2)...", flush=True)
            subprocess.run([sys.executable, str(BASE_DIR / "4_mappa_zone_google.py"), data_consegna, "--no-serve"], cwd=BASE_DIR)
    print(f"\n{'✅' if ok else '⚠️ '} =========================================")
    print(f"   ELABORAZIONE {'COMPLETATA' if ok else 'INCOMPLETA'}")
    print(f"   Data:   {data_consegna}")
    if json_out.exists():
        import json as _json
        n = len(_json.loads(json_out.read_text("utf-8")).get("punti", []))
        print(f"   Punti:  {n} punti consegna generati")
    if mappa_html.exists():
        print(f"   Mappa:  {mappa_html.name} creata ✅")
    print(f"")
    print(f"   Per aprire la MAPPA INTERATTIVA esegui:")
    print(f"   python 4_mappa_zone_google.py")
    print(f"✅ =========================================\n")



if __name__ == "__main__":
    main()

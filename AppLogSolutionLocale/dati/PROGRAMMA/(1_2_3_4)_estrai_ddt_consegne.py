#!/usr/bin/env python3
"""
(1_2_3_4)_estrai_ddt_consegne.py
════════════════════════════════
Estrae tutti i DDT dai PDF in CONSEGNE/DDT-ORIGINALI/FRUTTA e LATTE.
Identifica nuovi clienti ed estrae automaticamente i loro dati (Indirizzo, CAP, Orari, ecc.).

Uso: py (1_2_3_4)_estrai_ddt_consegne.py [data]
"""

import re
import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("pip install pypdf")
    sys.exit(1)

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
INPUT_FRUTTA = BASE_DIR / "FRUTTA"
INPUT_LATTE = BASE_DIR / "LATTE"
MAPPATURA_XLSX = PROG_DIR / "mappatura_destinazioni.xlsx"

# Regex per estrazione dati
DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'(?:[Ll]uogo [Dd]i [Dd]estinazione|[Cc]odice [Dd]estinazione):\s*([pP]\d{4,5})')
CAP_RE = re.compile(r"\b(\d{5})\b")
PROVINCIA_RE = re.compile(r"\(([A-Z]{2})\)")
CAUSALE_RE = re.compile(r'(?:conto di|ordine e conto di)\s+([A-Z]\d{4})(?:\s+H(\d{2}))?(?:\s+(\d{3}))?', re.I)
NUM_DDT_RE = re.compile(r'DDT\s*[Nn][°º\.\s]*([A-Za-z0-9/-]+)', re.I)


def _estrai_data_luogo(text: str) -> tuple[str | None, str | None, str | None]:
    """Estrae (data, luogo, num_ddt) da una pagina DDT. data in formato DD-MM-YYYY."""
    data = None
    m = DATA_DDT_RE.search(text)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    luogo_m = LUOGO_RE.search(text)
    luogo = luogo_m.group(1).lower() if luogo_m else None
    
    num_m = NUM_DDT_RE.search(text)
    num_ddt = num_m.group(1).replace("/", "-") if num_m else "UNK"
    
    return (data, luogo, num_ddt)


def _estrai_dati_consegna_da_testo(text: str, codice: str, da_frutta: bool) -> dict:
    """Estrae destinatario, indirizzo, CAP, città, provincia e orari dal testo di una pagina DDT."""
    res = {"dest": "", "ind": "", "cap": "", "cit": "", "prov": "", "om": "", "oM": "14:00"}
    if codice.lower() not in text.lower():
        return res
    
    idx_l = text.find("Luogo di destinazione")
    if idx_l < 0: return res

    # 1. Nome e Indirizzo
    if da_frutta:
        blocco = text[idx_l : idx_l + 650]
        lines = [ln.strip() for ln in blocco.split("\n") if ln.strip()]
        for i, ln in enumerate(lines):
            if LUOGO_RE.search(ln):
                if i + 1 < len(lines): res["dest"] = lines[i + 1].strip().title()
                if i + 2 < len(lines): res["ind"] = lines[i + 2].strip().title()
                break
    else:
        idx_causale = text.upper().find("CAUSALE DEL TRASPORTO")
        blocco = text[:idx_causale] if idx_causale > 0 else text[idx_l : idx_l + 900]
        for ln in blocco.split("\n"):
            ln = ln.strip()
            cf_m = re.match(r"^[Cc]\.?[Ff]\.?\s+", ln)
            if cf_m: res["dest"] = ln[cf_m.end():].strip().title()
            else:
                albo_m = re.match(r"^[Aa]lbo\s+", ln, re.I)
                if albo_m: res["ind"] = ln[albo_m.end():].strip().title()

    # 2. CAP, Provincia, Città
    idx_resp = text.upper().find("RESPONSABILE DEL TRASPORTO")
    blocco_prov = text[idx_resp:] if idx_resp >= 0 else text
    
    for prov_m in PROVINCIA_RE.finditer(blocco_prov):
        sigla = prov_m.group(1)
        if sigla == "MN" and ("Pomponesco" in blocco_prov[max(0, prov_m.start()-40):prov_m.start()] or "46030" in blocco_prov):
            continue
        res["prov"] = sigla
        caps = list(CAP_RE.finditer(blocco_prov[:prov_m.start()]))
        if caps:
            res["cap"] = caps[-1].group(1)
            pre = blocco_prov[caps[-1].end() : caps[-1].end() + 60]
            citta_m = re.search(r"\s*[-]?\s*([A-Za-zÀ-ÿ\s'.]+?)\s*\([A-Z]{2}\)", pre)
            if citta_m: res["cit"] = citta_m.group(1).strip().title()
        break
        
    # 3. Orari
    idx_c = text.upper().find("CAUSALE DEL TRASPORTO")
    if idx_c >= 0:
        sezione = text[idx_c:idx_c+150]
        m = CAUSALE_RE.search(sezione)
        if m:
            if m.group(2): res["oM"] = f"{int(m.group(2)):02d}:00"
            if m.group(3):
                s = m.group(3)
                if len(s) == 3: res["om"] = f"{int(s[0]):02d}:{int(s[1:3]):02d}"
    return res


def _ricava_date_da_pdf() -> list[str]:
    """Raccoglie TUTTE le date distinte trovate nei PDF di FRUTTA e LATTE."""
    import pdfplumber
    date_trovate: set[str] = set()
    for cart in (INPUT_FRUTTA, INPUT_LATTE):
        if not cart.exists(): continue
        for pdf_path in sorted(cart.glob("*.pdf")):
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        data, _, _ = _estrai_data_luogo(text)
                        if data: date_trovate.add(data)
            except: pass
    return sorted(date_trovate)


def _leggi_codici_mappatura() -> dict:
    """Restituisce {codice: (row_idx, om_frutta, oM_frutta, om_latte, oM_latte)}."""
    if not MAPPATURA_XLSX.exists(): return {}
    try:
        from openpyxl import load_workbook
        wb = load_workbook(MAPPATURA_XLSX, read_only=True, data_only=True)
        ws = wb.active
        headers = [str(c.value or "").strip() for c in ws[1]]
        col_om_f = next((i for i, h in enumerate(headers) if h == "Orario min Frutta"), 10)
        col_oM_f = next((i for i, h in enumerate(headers) if h == "Orario max Frutta"), 11)
        col_om_l = next((i for i, h in enumerate(headers) if h == "Orario min Latte"),  12)
        col_oM_l = next((i for i, h in enumerate(headers) if h == "Orario max Latte"),  13)
        codici = {}
        for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
            vals = [c.value for c in row]
            def _v(x): return str(x).strip() if x is not None else ""
            c_f = _v(vals[0]).lower()
            c_l = _v(vals[1]).lower() if len(vals) > 1 else ""
            om_f = _v(vals[col_om_f]) if col_om_f < len(vals) else ""
            oM_f = _v(vals[col_oM_f]) if col_oM_f < len(vals) else ""
            om_l = _v(vals[col_om_l]) if col_om_l < len(vals) else ""
            oM_l = _v(vals[col_oM_l]) if col_oM_l < len(vals) else ""
            if c_f and c_f != "p00000": codici[c_f] = (row_idx, om_f, oM_f, om_l, oM_l)
            if c_l and c_l != "p00000": codici[c_l] = (row_idx, om_f, oM_f, om_l, oM_l)
        wb.close()
        return codici
    except Exception as e:
        print(f"⚠️ Errore mappatura: {e}")
        return {}


def _aggiorna_orari_mappatura(row_idx: int, orario_min: str, orario_max: str, tipo: str):
    """Scrive Orario min/max sulla colonna FRUTTA o LATTE in mappatura_destinazioni.xlsx."""
    if not MAPPATURA_XLSX.exists() or not row_idx: return
    tipo_cap = tipo.capitalize()  # "Frutta" o "Latte"
    try:
        from openpyxl import load_workbook
        wb = load_workbook(MAPPATURA_XLSX)
        ws = wb.active
        headers = [str(c.value or "").strip() for c in ws[1]]
        col_om = next((i + 1 for i, h in enumerate(headers) if h == f"Orario min {tipo_cap}"), None)
        col_oM = next((i + 1 for i, h in enumerate(headers) if h == f"Orario max {tipo_cap}"), None)
        if col_om is None or col_oM is None:
            print(f"    ⚠️  Colonne orario {tipo_cap} non trovate in mappatura.")
            return
        if orario_min: ws.cell(row=row_idx, column=col_om, value=orario_min)
        if orario_max: ws.cell(row=row_idx, column=col_oM, value=orario_max)
        wb.save(MAPPATURA_XLSX)
        print(f"    ✅ Mappatura [{tipo_cap}] riga {row_idx}: min={orario_min or '—'}  max={orario_max or '—'}")
    except PermissionError:
        print(f"    ⚠️  mappatura_destinazioni.xlsx e' aperto — orari non aggiornati.")
    except Exception as e:
        print(f"    ⚠️  Errore aggiornamento orari: {e}")


def _verifica_nuovi_clienti(dati_nuovi: dict):
    if not dati_nuovi: return True
    print("\n" + "!"*60)
    print(f"🛑 RILEVATI {len(dati_nuovi)} NUOVI CODICI CLIENTE:")
    for cod, info in sorted(dati_nuovi.items()):
        print(f"   - {cod} ({info['tipo']}): {info['dest']} - {info['cit']}")
    print("!"*60 + "\n")
    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Nuovi Codici"
        headers = ["Codice Frutta", "Codice Latte", "A chi va consegnato", "Tipologia grado", "Indirizzo", "CAP", "Città", "Provincia",
                  "Tipologia consegna", "Tipologia consegna.1", "Email", "Sito web", "Orario min", "Orario max"]
        ws.append(headers)
        for cod, info in sorted(dati_nuovi.items()):
            row = [""] * 14
            if info["tipo"] == "FRUTTA": row[0] = cod
            else:                        row[1] = cod
            row[2], row[4], row[5], row[6], row[7], row[12], row[13] = info["dest"], info["ind"], info["cap"], info["cit"], info["prov"], info["om"], info["oM"]
            ws.append(row)
        hp = BASE_DIR / "nuovi_codici_consegna.xlsx"
        wb.save(hp)
        print(f"📄 File generato: {hp.name}\n💡 Copia i dati in mappatura_destinazioni.xlsx per proseguire.\n")
    except Exception as e: print(f"⚠️ Errore excel: {e}")
    return False


def _estrai_da_cartella(cart_in: Path, cart_out: Path, etichetta: str, date_valide: set[str], mappati: dict, *, duplicata: bool = False):
    """Estrae DDT da tutti i PDF accettando qualsiasi data presente in date_valide."""
    nuovi_dati = {}
    aggiornati_orari: set[int] = set()  # row_idx già aggiornati in questa esecuzione
    if not cart_in.exists(): return 0, 0, nuovi_dati
    cart_out.mkdir(parents=True, exist_ok=True)
    pdf_files = list(cart_in.glob("*.pdf"))
    if not pdf_files: return 0, 0, nuovi_dati
    import pdfplumber
    creati = 0
    visti = {}
    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            with pdfplumber.open(pdf_path) as pdf:
                gruppi_locali = {}
                for i in range(0, len(pdf.pages), 2 if duplicata else 1):
                    text = pdf.pages[i].extract_text() or ""
                    d, l, num_ddt = _estrai_data_luogo(text)
                    if not d or not l or d not in date_valide: continue  # accetta tutte le date valide
                    if l not in mappati and l not in nuovi_dati:
                        nuovi_dati[l] = _estrai_dati_consegna_da_testo(text, l, duplicata)
                        nuovi_dati[l]["tipo"] = etichetta
                    elif l in mappati:
                        # Cliente noto: verifica se orario nel DDT e' diverso dalla mappatura
                        row_idx_m, om_f, oM_f, om_l, oM_l = mappati[l]
                        # Seleziona i valori correnti per il tipo in elaborazione
                        om_mappa = om_f if etichetta == "FRUTTA" else om_l
                        oM_mappa = oM_f if etichetta == "FRUTTA" else oM_l
                        if row_idx_m not in aggiornati_orari:
                            idx_c = text.upper().find("CAUSALE DEL TRASPORTO")
                            if idx_c >= 0:
                                m_c = CAUSALE_RE.search(text[idx_c:idx_c+150])
                                if m_c:
                                    oM_ddt = f"{int(m_c.group(2)):02d}:00" if m_c.group(2) else ""
                                    om_ddt = ""
                                    if m_c.group(3):
                                        s = m_c.group(3)
                                        if len(s) == 3: om_ddt = f"{int(s[0]):02d}:{int(s[1:3]):02d}"
                                        elif len(s) == 4: om_ddt = f"{int(s[:2]):02d}:{int(s[2:]):02d}"
                                    needs_update = (
                                        (oM_ddt and oM_ddt != oM_mappa) or
                                        (om_ddt and om_ddt != om_mappa)
                                    )
                                    if needs_update:
                                        print(f"    [ORARIO {etichetta}] {l}: DDT({om_ddt or '-'}/{oM_ddt or '-'}) vs Mappatura({om_mappa or '-'}/{oM_mappa or '-'})")
                                        _aggiorna_orari_mappatura(row_idx_m, om_ddt or None, oM_ddt or None, etichetta)
                                        # Aggiorna in-memoria per tipo corretto
                                        if etichetta == "FRUTTA":
                                            mappati[l] = (row_idx_m, om_ddt or om_f, oM_ddt or oM_f, om_l, oM_l)
                                        else:
                                            mappati[l] = (row_idx_m, om_f, oM_f, om_ddt or om_l, oM_ddt or oM_l)
                                        aggiornati_orari.add(row_idx_m)
                                        
                    chiave = (l, d, num_ddt)
                    if chiave not in gruppi_locali:
                        gruppi_locali[chiave] = PdfWriter()
                    gruppi_locali[chiave].add_page(reader.pages[i])
                    if duplicata and i + 1 < len(pdf.pages):
                        gruppi_locali[chiave].add_page(reader.pages[i+1])
                        
                # Scrittura dei PDF accorpati per questo documento master
                for (l, d, num_ddt), writer in gruppi_locali.items():
                    chiave_globale = (l, d, num_ddt)
                    cnt = visti.get(chiave_globale, 0) + 1
                    visti[chiave_globale] = cnt
                    
                    fname = f"{l}_{d}_{num_ddt}_{cnt}.pdf" if cnt > 1 else f"{l}_{d}_{num_ddt}.pdf"
                    with open(cart_out / fname, "wb") as f:
                        writer.write(f)
                    creati += 1
                    if creati <= 3 or creati % 50 == 0: print(f"    {fname}")
        except Exception as e: print(f"  Errore {pdf_path.name}: {e}")
    return creati, sum(1 for c in visti.values() if c > 1), nuovi_dati


def _pulisci_sorgenti(cart_in: Path, date_valide: set[str]):
    """Elimina i PDF sorgenti che contengono pagine di qualsiasi data elaborata."""
    import pdfplumber
    rimossi = 0
    for p in cart_in.glob("*.pdf"):
        try:
            with pdfplumber.open(p) as pdf:
                if any(_estrai_data_luogo(pg.extract_text() or "")[0] in date_valide for pg in pdf.pages):
                    pdf.close(); p.unlink(); rimossi += 1
        except: pass
    return rimossi


def _pulisci_output(base: Path, data_v: str):
    for f in [base/"punti_consegna.xlsx", base/"punti_consegna_unificati.json", base/"4_mappa_zone_google.html", base/f"zone_google_{data_v.replace('-', '_')}.kml"]:
        if f.exists():
            try: f.unlink()
            except: pass


# --- ARTICOLI NOTI (SORGENTE DI VERITÀ) ---
ARTICOLI_NOTI = {
    "10-FLYER", "10-GEL", "10-MANIFESTO", "10-AT-01", "10-BICC", "10-CUCCH", "10-PIATTO",
    "AP-SU-PC", "FO-DI-PV-04-LB", "FO-DI-GP-01-NI", "FVNS-03", "FVNS-03-", 
    "LT-AQ-04-LV", "LT-AQ-04-LB", "LT-AQ-04-LS", "LT-DL-02-LC", "LT-ES-04-LS", "LT-ESL-IN-LB", 
    "MA-T-LI-L3-NA", "ME-T-DI-V0-NA", "ME-S-BI-L3-NA", "PE-T-DI-L3-NA",
    "YO-BI-MN-04-LB", "YO-DL-02-LC", "FI-Z-BI-L3-NA", "FR-M-BI-L3-NI",
    "LNS-04-GADGET", "LNS-04-", "CA-Z-BI-L3-NA", "KI-S-BI-L3-NA", "ME-S-DI-L3-NA", "FO-DI-AS-04-LV",
    "AL-M-BI-L3-NI", "SUCCO-REC",
}

def _is_primary_code(text: str) -> bool:
    """Verifica se una stringa corrisponde a un codice base noto (Sorgente di Verità)."""
    if not text: return False
    t = text.strip().upper()
    if t in ARTICOLI_NOTI: return True
    for prefix in ARTICOLI_NOTI:
        if prefix.endswith('-') and t.startswith(prefix.upper()):
            return True
    return False


def _normalizza_cella_codice_base(raw: str) -> str:
    """
    Dato il contenuto grezzo di una cella Cod. Articolo,
    restituisce SOLO il codice_base (prima riga significativa, filtro metadati).
    Uguale alla logica in 9_genera_distinte_da_viaggi.py.
    """
    righe = [l.strip() for l in raw.split('\n')
             if l.strip() and not l.strip().startswith("Codice:")]
    if not righe: return ""
    # La prima riga è sempre il codice base
    return righe[0]


def _verifica_nuovi_articoli(base):
    """
    Verifica la presenza di codici articolo non presenti in ARTICOLI_NOTI.
    Usa logica column-based: estrae la colonna Cod. Articolo dalle tabelle PDF
    e confronta il codice_base (NON la variante) con la Sorgente di Verita'.
    Questo evita falsi positivi per varianti note (es. FVNS-03-FOLDER e' noto
    perche' il suo codice_base FVNS-03- e' in ARTICOLI_NOTI).
    """
    print("Verifica articoli (logica column-based)...")
    import pdfplumber

    codici_base_trovati = set()
    divisi = base / "DDT-ORIGINALI-DIVISI"
    if not divisi.exists(): return True

    for p in divisi.rglob("*.pdf"):
        try:
            with pdfplumber.open(p) as pdf:
                for pg in pdf.pages:
                    tables = pg.extract_tables()
                    if not tables: continue
                    # Cerca la tabella con "Cod. Articolo"
                    tab = next((t for t in tables if t and len(t) > 1
                                and "Cod. Articolo" in " ".join(str(c or "") for c in t[0])), None)
                    if not tab: continue
                    for row in tab[1:]:
                        if not row or not row[0]: continue
                        codice_base = _normalizza_cella_codice_base(str(row[0]))
                        if codice_base:
                            codici_base_trovati.add(codice_base)
        except: continue

    # Confronta i codici_base trovati con ARTICOLI_NOTI
    nuovi = {c for c in codici_base_trovati if not _is_primary_code(c)}

    if nuovi:
        print("\n" + "!"*60 + f"\n[!] NUOVI ARTICOLI RILEVATI: {', '.join(sorted(nuovi))}\n" + "!"*60 + "\n")
        try:
            from openpyxl import Workbook
            wb = Workbook(); ws = wb.active; ws.title = "Nuovi Articoli"
            ws.append(["Codice Articolo", "Data Rilevamento", "Azione"])
            for c in sorted(nuovi):
                ws.append([c, datetime.now().strftime("%d/%m/%Y"), "Aggiungere a ARTICOLI_NOTI"])
            rp = BASE_DIR / "nuovi_articoli_rilevati.xlsx"
            wb.save(rp)
            print(f"Report salvato: {rp.name}")
        except Exception as e:
            print(f"Errore salvataggio report: {e}")
        return False

    print(f"Articoli OK. ({len(codici_base_trovati)} codici base verificati)\n")
    return True


def main():
    # ── Determina le date valide ────────────────────────────────────────────
    arg = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if arg:
        # Supporta: "27-03", "27-03-2026", "27-03-2026_28-03-2026"
        date_valide: set[str] = set()
        for parte in arg.split("_"):
            if re.match(r"^\d{2}-\d{2}$", parte): parte = f"{parte}-2026"
            date_valide.add(parte)
    else:
        date_list = _ricava_date_da_pdf()
        if not date_list: return print("❌ Nessun PDF trovato.")
        date_valide = set(date_list)

    # ── Nome cartella: singola o doppia data ────────────────────────────────
    data_label = "_".join(sorted(date_valide))   # es. "30-03-2026" o "30-03-2026_31-03-2026"
    base = CONSEGNE_DIR / f"CONSEGNE_{data_label}"
    if base.exists() and not arg:
        return print(f"⚠️ Cartella {base.name} esiste già. Passa la data come argomento per forzare.")

    _pulisci_output(base, data_label)
    nd = len(date_valide)
    print(f"\n--- Estrazione DDT ({data_label}) — {nd} data{'e' if nd > 1 else ''} ---\n")
    if nd > 1:
        print(f"  ℹ️  Date rilevate: {', '.join(sorted(date_valide))} → elaborazione accorpata\n")

    out_f = base / "DDT-ORIGINALI-DIVISI" / "FRUTTA"
    out_l = base / "DDT-ORIGINALI-DIVISI" / "LATTE"
    mappati = _leggi_codici_mappatura()
    res_f = _estrai_da_cartella(INPUT_FRUTTA, out_f, "FRUTTA", date_valide, mappati, duplicata=True)
    res_l = _estrai_da_cartella(INPUT_LATTE,  out_l, "LATTE",  date_valide, mappati)

    if not _verifica_nuovi_clienti({**res_f[2], **res_l[2]}): sys.exit(1)
    if not _verifica_nuovi_articoli(base): sys.exit(1)

    print("Pulizia sorgenti e avvio pipeline...")
    _pulisci_sorgenti(INPUT_FRUTTA, date_valide)
    _pulisci_sorgenti(INPUT_LATTE,  date_valide)
    time.sleep(1)

    for s in ["2_crea_punti_consegna.py", "3_crea_lista_unificata.py"]:
        p = PROG_DIR / s
        if p.exists():
            print(f"⚙️ {s}...")
            subprocess.run([sys.executable, str(p), data_label], cwd=BASE_DIR)

    p_mappa = PROG_DIR / "4_mappa_zone_google.py"
    if p_mappa.exists():
        print(f"⚙️ 4_mappa_zone_google.py (generazione file, server disabilitato)...")
        subprocess.run([sys.executable, str(p_mappa), data_label, "--no-serve"], cwd=BASE_DIR)

    print(f"\n✅ COMPLETATO ({data_label})!")

if __name__ == "__main__": main()

#!/usr/bin/env python3
"""
9_genera_distinte_da_viaggi.py
══════════════════════════════
Legge viaggi_giornalieri_OTTIMIZZATO.json (generato da 8_genera_json_ottimizzato.py)
e per ogni viaggio:
  1. Trova i PDF DDT individuali in DDT-ORIGINALI-DIVISI/{FRUTTA,LATTE}/
  2. Estrae e consolida gli articoli (logica da crea_distinta_magazzino)
  3. Genera una distinta PDF per viaggio nell'ORDINE OTTIMIZZATO
  4. Assembla un Master PDF unico

NOTA ORDINE CARICO MAGAZZINO:
  - L'ordine nel JSON è l'ordine di CONSEGNA (fermata 1 = prima consegna)
  - Il magazziniere carica AL CONTRARIO: ultima fermata = primo caricato sul furgone

VERIFICA ORFANI:
  - Dopo aver processato tutti i viaggi, lo script verifica che non ci siano
    PDF DDT nella cartella che non sono stati assegnati a nessun viaggio.

Uso: py 9_genera_distinte_da_viaggi.py [data]
     es: py 9_genera_distinte_da_viaggi.py 26-03-2026
"""

import json
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

# --- CONFIGURAZIONE ---
PROG_DIR     = Path(__file__).resolve().parent
BASE_DIR     = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
RIENTRI_XLSX = BASE_DIR / "rientri_ddt.xlsx"
CODICE_VUOTO = "p00000"

# Importa logica estrazione articoli da crea_distinta_magazzino
DISTINTA_MOD = BASE_DIR / "crea_distinta_magazzino.py"

# --- DATABASE ARTICOLI (allineato a crea_distinta_magazzino) ---
ARTICOLI_NOTI = frozenset({
    "ME-T-DI-V0-NA", "PE-T-DI-L3-NA", "10-GEL", "10-FLYER", "10-MANIFESTO", "LT-DL-02-LC", "LT-ES-04-LS",
    "LT-ESL-IN-LB", "LT-AQ-04-LV", "YO-BI-MN-04-LB", "YO-DL-02-LC", "AP-SU-PC", "FO-DI-PV-04-LB",
    "CA-Z-BI-L3-NA", "FO-DI-GP-01-NI", "FVNS-03-GADGET", "KI-S-BI-L3-NA", "FVNS-03-POSTER"
})

CODICE_MAP = {
    "FVNS-03-POSTER": ("10-MANIFESTO", "Manifesto programma"),
}

CONSOLIDAMENTO = {
    "LT-ES-04-LS":   ("Fardelli",  "Bottiglie", 10),
    "LT-ESL-IN-LB":  ("Fardelli",  "Bottiglie",  6),
    "YO-BI-MN-04-LB":("Cartoni",   "Cluster",   10),
    "YO-DL-02-LC":   ("Cartoni",   "Porzioni",   6),
    "AP-SU-PC":      ("Cartoni",   "Porzioni",  24),
    "FO-DI-GP-01-NI":("Colli",     "Buste",     16),
    "FO-DI-PV-04-LB":("Colli",     "Fette",     20),
}

UNITA_QTY = r"(Confezioni|Confezione|confezioni|confezione|Colli|Collo|colli|collo|Brick|brick|Fardelli|Fardello|fardelli|fardello|Bottiglie|Bottiglia|bottiglie|bottiglia|Cartoni|Cartone|cartoni|cartone|Cluster|cluster|Porzioni|Porzione|porzioni|porzione|Fascette|Fascetta|fascette|fascetta|Manifesti|Manifesto|manifesti|manifesto|Fette|Fetta|fette|fetta|Buste|Busta|buste|busta|pz)"
CONF_PATTERN = r"[\d,\.]+\s*(?:Porzioni?|Bottiglie?|Cluster|Fetta?)\s*/\s*\w+"
SCAD_RE = re.compile(r"Scad\.\s*min\.\s*(\d{2}/\d{2}/\d{4})", re.I)


# ──────────────────────────────────────────────────────────────────────────────
# UTILITÀ
# ──────────────────────────────────────────────────────────────────────────────

def _normalizza_unita(u: str) -> str:
    u = u.strip().lower()
    mapping = {
        "bottiglia": "Bottiglie", "bottiglie": "Bottiglie",
        "fardello": "Fardelli",   "fardelli": "Fardelli",
        "cartone": "Cartoni",     "cartoni": "Cartoni",
        "cluster": "Cluster",
        "porzione": "Porzioni",   "porzioni": "Porzioni",
        "collo": "Colli",         "colli": "Colli",
        "fetta": "Fette",         "fette": "Fette",
        "brick": "Brick",
        "confezione": "Confezioni", "confezioni": "Confezioni",
        "manifesto": "Manifesti", "manifesti": "Manifesti",
        "fascetta": "Fascette",
        "busta": "Buste",         "buste": "Buste",
        "pz": "pz"
    }
    return mapping.get(u, u.title() if u else u)


def _consolida_quantita(codice: str, lista_qty: list) -> tuple:
    if codice not in CONSOLIDAMENTO:
        by_unit = defaultdict(int)
        for qty, unit in lista_qty:
            by_unit[_normalizza_unita(unit)] += qty
        result = [(v, k) for k, v in sorted(by_unit.items()) if v > 0]
        return result, " ".join(f"{q} {u}" for q, u in result)

    unit_princ, unit_second, ratio = CONSOLIDAMENTO[codice]
    tot_princ = tot_second = 0
    for qty, unit in lista_qty:
        ul = unit.lower()
        if unit_princ.lower() in ul or ul in ("fardello", "fardelli", "cartoni", "cartone",
                                               "brick", "colli", "confezioni", "manifesti", "fascette"):
            tot_princ += qty
        else:
            tot_second += qty

    extra_princ   = tot_second // ratio
    resto_second  = tot_second % ratio
    tot_princ    += extra_princ

    result = []
    if tot_princ > 0:
        result.append((tot_princ, unit_princ))
    if resto_second > 0:
        result.append((resto_second, unit_second))
    display = " e ".join(f"{q} {u}" for q, u in result)
    return result, display


def _parse_quantita_da_cella(cell) -> list:
    if not cell or not str(cell).strip():
        return []
    text = str(cell).replace("\n", " ").replace("  ", " ")
    quantita = []
    for m in re.finditer(r"(?:^|e\s+)(\d+)\s+(" + UNITA_QTY + r")", text, re.I):
        quantita.append((int(m.group(1)), _normalizza_unita(m.group(2))))
    if not quantita and re.search(r"^(\d+)\s*$", text.strip()):
        quantita.append((int(text.strip()), "pz"))
    return quantita


def _estrai_articoli_da_tabella(page) -> list | None:
    tables = page.extract_tables()
    if not tables:
        return None
    tab = None
    for t in tables:
        if not t or len(t) < 2:
            continue
        header = " ".join(str(c or "") for c in (t[0] or []))
        if "Cod. Articolo" in header:
            tab = t
            break
    if not tab:
        return None

    articoli = []
    for row in tab[1:]:
        if not row or len(row) < 4:
            continue
        cell0 = str(row[0] or "").strip()
        if not cell0:
            continue
        codice_raw = None
        for linea in cell0.split("\n"):
            linea = linea.strip()
            if linea.startswith("Codice:"):
                continue
            if re.match(r"^[A-Z0-9]{2,}-[A-Z0-9\-]+", linea):
                codice_raw = re.match(r"^([A-Z0-9]{2,}-[A-Z0-9\-]+)", linea).group(1).strip()
                break
        if not codice_raw:
            continue
        if codice_raw == "FVNS-03-":
            codice_raw = "FVNS-03-POSTER"
        codice, _ = CODICE_MAP.get(codice_raw, (codice_raw, ""))

        try:
            kg_val = str(row[2] or "0").replace(",", ".").strip()
            kg = Decimal(kg_val) if kg_val else Decimal("0")
        except Exception:
            kg = Decimal("0")

        cell3 = row[3] if len(row) > 3 else ""
        quantita = _parse_quantita_da_cella(cell3)
        if not quantita and codice == "10-GEL":
            porz = str(row[4] or "") if len(row) > 4 else ""
            if porz.isdigit():
                quantita = [(int(porz), "pz")]
        if not quantita:
            continue

        cell1 = str(row[1] or "").strip()
        scad_m = SCAD_RE.search(cell1)
        scadenza = scad_m.group(1) if scad_m else ""
        confezionamento = str(row[5] or "").strip() if len(row) > 5 else ""

        articoli.append({
            "codice": codice, "descrizione": cell1 or codice,
            "scadenza": scadenza, "kg": kg,
            "quantita": quantita, "confezionamento": confezionamento,
        })
    return articoli if articoli else None


def _estrai_articoli_da_pagina_testo(lines: list, tipo: str) -> list:
    articoli = []
    i = 0
    while i < len(lines) and "Cod. Articolo" not in lines[i] and "Confezionamento" not in lines[i]:
        i += 1
    i += 2

    while i < len(lines):
        line = lines[i]
        if "___" in line or "Scadenza" in line:
            break
        code_m = re.match(r"^([A-Z0-9]{2,}-[A-Z0-9\-]*)", line)
        if not code_m or len(code_m.group(1)) < 4:
            i += 1
            continue
        codice_raw = code_m.group(1).strip()
        if codice_raw == "FVNS-03-":
            codice_raw = "FVNS-03-POSTER"
        codice, _ = CODICE_MAP.get(codice_raw, (codice_raw, ""))

        next_lines = []
        for k in range(i + 1, min(i + 6, len(lines))):
            stripped = lines[k].strip()
            if stripped and re.match(r"^[A-Z0-9]{2,}-[A-Z0-9\-]", stripped):
                break
            next_lines.append(lines[k])

        # Quantita dalla riga principale
        quantita = _parse_quantita_da_cella(line)
        if not quantita:
            for nl in next_lines[:3]:
                quantita = _parse_quantita_da_cella(nl)
                if quantita:
                    break

        if not quantita:
            i += 1
            continue

        scad_m = re.search(r"Scad\.\s*min\.\s*(\d{2}/\d{2}/\d{4})", " ".join([line] + next_lines), re.I)
        scadenza = scad_m.group(1) if scad_m else ""

        articoli.append({
            "codice": codice, "descrizione": codice,
            "scadenza": scadenza, "kg": Decimal("0"),
            "quantita": quantita, "confezionamento": "",
        })
        i += 1
    return articoli


def _raccogli_articoli_da_pdf(pdf_path: Path, tipo: str) -> list:
    import pdfplumber
    tutti = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                arts = _estrai_articoli_da_tabella(page)
                if arts is None:
                    text = page.extract_text() or ""
                    arts = _estrai_articoli_da_pagina_testo(text.split("\n"), tipo)
                tutti.extend(arts or [])
    except Exception as e:
        print(f"    ⚠️  Errore lettura {pdf_path.name}: {e}")
    return tutti


def _aggrega_articoli(lista: list) -> dict:
    """Aggrega articoli con lo stesso codice+scadenza sommando kg e quantita."""
    agg = {}
    for art in lista:
        chiave = (art["codice"], art["scadenza"])
        if chiave not in agg:
            agg[chiave] = {
                "codice": art["codice"],
                "descrizione": art["descrizione"],
                "scadenza": art["scadenza"],
                "kg": Decimal("0"),
                "quantita": [],
                "confezionamento": art["confezionamento"],
            }
        agg[chiave]["kg"] += art["kg"]
        agg[chiave]["quantita"].extend(art["quantita"])
        if not agg[chiave]["confezionamento"] and art["confezionamento"]:
            agg[chiave]["confezionamento"] = art["confezionamento"]
    return agg


# ──────────────────────────────────────────────────────────────────────────────
# RICERCA PDF
# ──────────────────────────────────────────────────────────────────────────────

def _carica_rientri() -> dict:
    """
    Legge rientri_ddt.xlsx e restituisce un dizionario:
        { codice_lower: 'DD-MM-YYYY' }
    Colonna A = codice consegna (es. 'p1745')
    Colonna B = data DDT originale (datetime o stringa)
    Colonna C = stato: se contiene 'allegato' (senza 'lavorazione') → già consegnato, salta.

    Il PDF fisico va cercato in:
        CONSEGNE_{data}/DDT-ORIGINALI-DIVISI/{FRUTTA o LATTE}/{codice}_{data}.pdf
    """
    if not RIENTRI_XLSX.exists():
        return {}
    try:
        from openpyxl import load_workbook
        wb = load_workbook(RIENTRI_XLSX, read_only=True, data_only=True)
        ws = wb.active
        rientri = {}
        for row in ws.iter_rows(min_row=2, values_only=True):
            codice = row[0]
            data_b = row[1]
            if not codice or not data_b:
                continue

            # ── Filtro colonna C: salta i rientri già consegnati ──────────
            stato = str(row[2] or "").strip().lower() if len(row) > 2 else ""
            if "allegato" in stato and "lavorazione" not in stato:
                continue   # già consegnato in una sessione precedente

            codice = str(codice).strip().lower()
            if hasattr(data_b, 'strftime'):
                data_str = data_b.strftime("%d-%m-%Y")
            else:
                data_str = str(data_b).strip()
            if codice and data_str:
                rientri[codice] = data_str
        wb.close()
        return rientri
    except Exception as e:
        print(f"  ⚠️  Errore lettura rientri_ddt.xlsx: {e}")
        return {}



def _trova_pdf(codice: str, data: str, cartella: Path) -> Path | None:
    """
    Cerca il PDF del cliente nella cartella specificata.
    Nome atteso: {codice}_{data}.pdf  (es. p2067_26-03-2026.pdf)

    Supporta cartelle multi-data (es. "30-03-2026_31-03-2026"):
      1. Prova la data esatta composta (es. p1745_30-03-2026_31-03-2026.pdf)
      2. Per cartelle multi-data, prova ogni singola data separata (es. p1745_30-03-2026.pdf)
      3. Fallback glob: qualsiasi file che inizia con {codice}_
    """
    if codice == CODICE_VUOTO or not codice:
        return None

    # 1. Ricerca esatta (funziona per date singole e come primo tentativo)
    p = cartella / f"{codice}_{data}.pdf"
    if p.exists():
        return p

    # 2. Se la data è multi-data (contiene "_" che separa due date DD-MM-YYYY_DD-MM-YYYY),
    #    prova ogni singola data estratta
    #    Formato atteso: "30-03-2026_31-03-2026" → ['30-03-2026', '31-03-2026']
    parti_data = re.findall(r"\d{2}-\d{2}-\d{4}", data)
    if len(parti_data) > 1:
        for d in parti_data:
            p = cartella / f"{codice}_{d}.pdf"
            if p.exists():
                return p

    # 3. Fallback glob: cerca qualsiasi file che inizia con il codice
    matches = list(cartella.glob(f"{codice}_*.pdf"))
    if matches:
        return matches[0]

    return None


def _trova_cartella(data_arg: str | None) -> Path:
    if data_arg:
        if re.match(r"^\d{2}-\d{2}$", data_arg):
            data_arg = f"{data_arg}-2026"
        p = CONSEGNE_DIR / f"CONSEGNE_{data_arg}"
        if not p.exists():
            raise FileNotFoundError(f"Cartella non trovata: {p}")
        return p
    folders = sorted(
        [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")],
        key=lambda d: d.name
    )
    if not folders:
        raise FileNotFoundError("Nessuna cartella CONSEGNE_* trovata.")
    return folders[-1]


# ──────────────────────────────────────────────────────────────────────────────
# GENERAZIONE PDF DISTINTE
# ──────────────────────────────────────────────────────────────────────────────

def _blocco_distinta(viaggio: dict, articoli_viaggio: dict, data_ddt: str, copia: int, styles, colors, mm, Paragraph, Spacer, Table, TableStyle, PageBreak):
    """Restituisce la lista di elementi Flowable per una singola copia della distinta."""
    from reportlab.lib.styles import ParagraphStyle
    st_titolo = ParagraphStyle("titolo", parent=styles["Heading1"], fontSize=14, spaceAfter=3)
    st_sub    = ParagraphStyle("sub",    parent=styles["Normal"],   fontSize=9,  spaceAfter=2)
    st_body   = ParagraphStyle("body",   parent=styles["Normal"],   fontSize=8)
    st_warn   = ParagraphStyle("warn",   parent=styles["Normal"],   fontSize=8, textColor=colors.red)

    nome_giro = viaggio.get("nome_giro", "?")
    zone      = ", ".join(viaggio.get("zone", []))
    n_fermate = viaggio.get("num_fermate", 0)
    label     = f"{'COPIA AUTISTA' if copia == 1 else 'COPIA UFFICIO'}"
    elementi  = []

    # Intestazione
    elementi.append(Paragraph(f"DISTINTA DI CARICO — {nome_giro}  [{label}]", st_titolo))
    elementi.append(Paragraph(f"Zone: {zone}  |  Fermate: {n_fermate}  |  Data: {data_ddt}", st_sub))
    elementi.append(Paragraph("⚠️  Caricare nell'ordine inverso: l'ULTIMA fermata va caricata PER PRIMA.", st_warn))
    elementi.append(Spacer(1, 4*mm))

    # ── SEZIONE 1: ARTICOLI (RICHIESTA: PRIMA IL RIEPILOGO ARTICOLI) ──
    elementi.append(Paragraph("RIEPILOGO ARTICOLI DA CARICARE PER GIRO:", st_body))
    dati_art = [["Codice Articolo", "Quantità Consolidata", "KG Totali", "Confezionamento", "Note"]]
    for (codice, scadenza), art in sorted(articoli_viaggio.items(), key=lambda x: x[0][0]):
        qty_cons, display = _consolida_quantita(codice, art["quantita"])
        kg_tot = float(art["kg"]) if art["kg"] else 0
        nota = "" if codice in ARTICOLI_NOTI else "⚠️ NUOVO"
        dati_art.append([
            codice,
            display or "—",
            f"{kg_tot:.1f}" if kg_tot else "—",
            art.get("confezionamento", "")[:30] or "—",
            nota,
        ])
    ts_art = TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#10b981")),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTSIZE",       (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fdf4")]),
        ("GRID",           (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
        ("TEXTCOLOR",      (4, 1), (4, -1),  colors.red),
        ("LEFTPADDING",    (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 3),
    ])
    t_art = Table(dati_art, colWidths=[35*mm, 40*mm, 20*mm, 50*mm, 22*mm])
    t_art.setStyle(ts_art)
    elementi.append(t_art)
    elementi.append(Spacer(1, 10*mm))

    # ── SEZIONE 2: LISTA CLIENTI ──
    elementi.append(Paragraph("ORDINE DI CARICO (carica dal basso: N.1 = ultima fermata = primo da caricare):", st_body))
    fermate     = viaggio.get("lista_punti", [])
    fermate_inv = list(reversed(fermate))

    # colonne: #, Cod.F, Cod.L, Nome, Indirizzo
    dati_fermate = [["#", "Cod. F", "Cod. L", "Nome", "Indirizzo"]]
    for idx, f in enumerate(fermate_inv, 1):
        cf = f.get("codice_frutta", "") or ""
        cl = f.get("codice_latte",  "") or ""
        dati_fermate.append([
            str(idx),
            cf if cf != CODICE_VUOTO else "—",
            cl if cl != CODICE_VUOTO else "—",
            f.get("nome", "")[:40],
            f.get("indirizzo", "")[:50],
        ])
    ts_fermate = TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#1e293b")),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTSIZE",       (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("GRID",           (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
        ("LEFTPADDING",    (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 3),
    ])
    t_fermate = Table(dati_fermate, colWidths=[8*mm, 22*mm, 22*mm, 50*mm, 65*mm])
    t_fermate.setStyle(ts_fermate)
    elementi.append(t_fermate)
    
    return elementi


def _genera_distinta_pdf(viaggio: dict, articoli_viaggio: dict, out_path: Path, data_ddt: str, pdf_ddt: list[Path]):
    """Genera il PDF della distinta di carico per un viaggio in DOPPIA COPIA + DDT allegati x2."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

    # --- Genera le due copie della distinta in un PDF temporaneo ---
    import tempfile, os
    tmp = out_path.parent / (out_path.stem + "_TMP.pdf")

    doc = SimpleDocTemplate(
        str(tmp), pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )
    styles = getSampleStyleSheet()

    elementi = []
    # Copia 1 — AUTISTA
    elementi += _blocco_distinta(viaggio, articoli_viaggio, data_ddt, 1, styles, colors, mm, Paragraph, Spacer, Table, TableStyle, PageBreak)
    elementi.append(PageBreak())
    # Copia 2 — UFFICIO
    elementi += _blocco_distinta(viaggio, articoli_viaggio, data_ddt, 2, styles, colors, mm, Paragraph, Spacer, Table, TableStyle, PageBreak)

    doc.build(elementi)

    # --- Assembla fascicoli: [Distinta Copy 1 + DDTs] + [Distinta Copy 2 + DDTs] ---
    # I DDT vengono allegati in ordine INVERSO rispetto al percorso:
    # → Nel PDF: stop N, stop N-1, ..., stop 1
    # → Dopo la stampa (i fogli escono impilati): stop 1 è in CIMA alla pila ✅
    # Così l'autista trova subito il DDT della prima consegna senza sfogliare.
    pdf_ddt_inv = list(reversed(pdf_ddt))

    try:
        from pypdf import PdfWriter, PdfReader
        writer = PdfWriter()
        reader_tmp = PdfReader(str(tmp))

        # --- BLOCCO 1: AUTISTA ---
        if len(reader_tmp.pages) > 0:
            writer.add_page(reader_tmp.pages[0])
        for pdf in pdf_ddt_inv:
            writer.append(str(pdf))

        # --- BLOCCO 2: UFFICIO ---
        if len(reader_tmp.pages) > 1:
            writer.add_page(reader_tmp.pages[1])
        else:
            writer.add_page(reader_tmp.pages[0])

        for pdf in pdf_ddt_inv:
            writer.append(str(pdf))

        with open(out_path, "wb") as f:
            writer.write(f)
        tmp.unlink(missing_ok=True)
    except Exception as e:
        # Fallback se pypdf fallisce
        import shutil
        shutil.move(str(tmp), str(out_path))
        print(f"    ⚠️  Errore assiemaggio pypdf: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    try:
        import pdfplumber
        from reportlab.lib.pagesizes import A4
    except ImportError as e:
        print(f"❌ Libreria mancante: {e}  →  pip install pdfplumber reportlab")
        sys.exit(1)

    data_arg = sys.argv[1].strip() if len(sys.argv) > 1 else None
    try:
        cartella = _trova_cartella(data_arg)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    data_ddt = cartella.name.replace("CONSEGNE_", "")
    json_path = cartella / "viaggi_giornalieri_OTTIMIZZATO.json"

    if not json_path.exists():
        print(f"❌ File non trovato: {json_path.name}")
        print("   Esegui prima: py 8_genera_json_ottimizzato.py")
        sys.exit(1)

    viaggi = json.loads(json_path.read_text(encoding="utf-8"))
    divisi_dir   = cartella / "DDT-ORIGINALI-DIVISI"
    dir_frutta   = divisi_dir / "FRUTTA"
    dir_latte    = divisi_dir / "LATTE"
    out_dir      = cartella / "DISTINTE_VIAGGIO"
    out_dir.mkdir(exist_ok=True)

    print(f"\n{'='*65}")
    print(f"  9_GENERA_DISTINTE — {data_ddt}  ({len(viaggi)} giri)")
    print(f"{'='*65}\n")

    # Carica mappa rientri: { codice: data_originale }
    rientri = _carica_rientri()
    if rientri:
        print(f"  [RIENTRI] Caricati da rientri_ddt.xlsx: {len(rientri)} codici mappati")

    # Traccia i PDF usati (per verifica orfani)
    pdf_usati: set[Path] = set()
    pdf_generati: list[Path] = []

    for viaggio in viaggi:
        nome_giro = viaggio["nome_giro"]
        zone      = ", ".join(viaggio.get("zone", []))
        punti     = viaggio.get("lista_punti", [])
        data_v    = viaggio.get("data_ddt", data_ddt)

        print(f"  📦 {nome_giro} (zone: {zone}) — {len(punti)} fermate")

        articoli_giro: list[dict] = []
        pdf_non_trovati: list[str] = []
        pdf_usati_viaggio: list[Path] = []  # PDF di questo viaggio specifico

        for punto in punti:
            cf   = punto.get("codice_frutta", "") or ""
            cl   = punto.get("codice_latte",  "") or ""
            d_p  = punto.get("data_consegna", data_v) or data_v
            nome = punto.get("nome", "?")[:40]

            # Cerca nella cartella corretta per data (supporta rientri di altre date)
            if d_p != data_v:
                cartella_r   = CONSEGNE_DIR / f"CONSEGNE_{d_p}"
                dir_frutta_r = cartella_r / "DDT-ORIGINALI-DIVISI" / "FRUTTA"
                dir_latte_r  = cartella_r / "DDT-ORIGINALI-DIVISI" / "LATTE"
            else:
                dir_frutta_r = dir_frutta
                dir_latte_r  = dir_latte

            for codice, tipo in [(cf, "FRUTTA"), (cl, "LATTE")]:
                if codice == CODICE_VUOTO or not codice:
                    continue

                pdf = None
                tipo_trovato = tipo

                if codice.lower() in rientri:
                    # ── RIENTRO: cerca SOLO nella cartella della data storica (col. B) ──
                    # Mai nella cartella corrente: il DDT di rientro è per definizione
                    # archiviato nella cartella della sua data originale.
                    data_rientro = rientri[codice.lower()]
                    cart_storica = CONSEGNE_DIR / f"CONSEGNE_{data_rientro}" / "DDT-ORIGINALI-DIVISI"
                    for sotto in ["FRUTTA", "LATTE"]:
                        pdf = _trova_pdf(codice, data_rientro, cart_storica / sotto)
                        if pdf:
                            tipo_trovato = sotto
                            break
                else:
                    # ── CONSEGNA NORMALE: cerca nella cartella della sessione corrente ──
                    cart_tipo = dir_frutta_r if tipo == "FRUTTA" else dir_latte_r
                    pdf = _trova_pdf(codice, d_p, cart_tipo)

                if pdf:
                    pdf_usati.add(pdf)
                    pdf_usati_viaggio.append(pdf)
                    articoli = _raccogli_articoli_da_pdf(pdf, tipo_trovato)
                    articoli_giro.extend(articoli)
                    n_art = len(articoli)
                    is_rientro = codice.lower() in rientri
                    tag = f" [RIENTRO←{rientri[codice.lower()]}]" if is_rientro else ""
                    print(f"       ✅ {nome:<40} {codice} ({tipo_trovato}){tag} → {n_art} art.")
                else:
                    pdf_non_trovati.append(f"{codice} ({tipo})")
                    print(f"       ⚠️  {nome:<40} {codice} ({tipo}) → PDF non trovato")

        # Aggrega articoli del viaggio
        articoli_agg = _aggrega_articoli(articoli_giro)
        print(f"       → Totale articoli distinti: {len(articoli_agg)}")

        # Genera PDF distinta
        sanitized = re.sub(r'[\\/*?:"<>|]', '_', nome_giro)
        zone_str  = "_".join(viaggio.get("zone", []))
        pdf_name  = f"DISTINTA_{sanitized}_Zone_{zone_str}.pdf"
        out_pdf   = out_dir / pdf_name

        try:
            _genera_distinta_pdf(viaggio, articoli_agg, out_pdf, data_ddt, list(pdf_usati_viaggio))
            pdf_generati.append(out_pdf)
            print(f"       📄 Salvato: {pdf_name} (doppia copia + {len(pdf_usati_viaggio)} DDT x2)\n")
        except Exception as e:
            print(f"       ❌ Errore PDF: {e}\n")

    # ── Assembla Master PDF ──
    if pdf_generati:
        try:
            from pypdf import PdfWriter
            master_path = cartella / f"MASTER_DISTINTE_{data_ddt}.pdf"
            writer = PdfWriter()
            for p in pdf_generati:
                writer.append(str(p))
            with open(master_path, "wb") as f:
                writer.write(f)
            print(f"  📚 Master PDF: {master_path.name}")
        except ImportError:
            print("  ⚠️  pypdf non installato — Master PDF non generato (pip install pypdf)")
        except Exception as e:
            print(f"  ⚠️  Errore Master PDF: {e}")

    # ── Verifica orfani ──
    print(f"\n  🔍 Verifica DDT orfani...")
    tutti_pdf: list[Path] = []
    for d in [dir_frutta, dir_latte]:
        if d.exists():
            tutti_pdf.extend(d.glob("*.pdf"))

    orfani = [p for p in tutti_pdf if p not in pdf_usati]
    if orfani:
        print(f"  ⚠️  {len(orfani)} PDF non assegnati a nessun viaggio:")
        for p in sorted(orfani):
            print(f"       - {p.parent.name}/{p.name}")
    else:
        print(f"  ✅ Tutti i PDF DDT sono stati assegnati a un viaggio.")

    # ── Riepilogo finale ──
    print(f"\n{'='*65}")
    print(f"  ✅ COMPLETATO!")
    print(f"     Distinte generate: {len(pdf_generati)}")
    print(f"     Cartella output:   {out_dir.name}")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()

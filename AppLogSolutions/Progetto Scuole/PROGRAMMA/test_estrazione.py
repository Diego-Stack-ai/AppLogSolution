#!/usr/bin/env python3
"""
Test column-based blindato: ogni riga della tabella = un articolo indipendente.
Nessuna state machine. Verifica codice_base + variante_raw su PDF reali.
"""
import re, sys
from decimal import Decimal
from pathlib import Path
import pdfplumber

# ── Sorgente di Verita' ─────────────────────────────────────────────────────
ARTICOLI_NOTI = frozenset({
    "10-FLYER", "10-GEL", "10-MANIFESTO", "10-AT-01", "10-BICC", "10-CUCCH", "10-PIATTO",
    "AP-SU-PC", "FO-DI-PV-04-LB", "FO-DI-GP-01-NI", "FVNS-03", "FVNS-03-",
    "LT-AQ-04-LV", "LT-DL-02-LC", "LT-ES-04-LS", "LT-ESL-IN-LB",
    "MA-T-LI-L3-NA", "ME-T-DI-V0-NA", "ME-S-BI-L3-NA", "PE-T-DI-L3-NA",
    "YO-BI-MN-04-LB", "YO-DL-02-LC", "FI-Z-BI-L3-NA", "FR-M-BI-L3-NI",
    "LNS-04-GADGET", "LNS-04-", "CA-Z-BI-L3-NA", "KI-S-BI-L3-NA"
})

UNITA_QTY = r"(?:Confezioni|Confezione|Colli|Collo|Brick|Fardelli|Fardello|Bottiglie|Bottiglia|Cartoni|Cartone|Cluster|Porzioni|Porzione|Fascette|Fascetta|Manifesti|Manifesto|Fette|Fetta|Buste|Busta|pz)"
SCAD_RE = re.compile(r"Scad\.\s*min\.\s*(\d{2}/\d{2}/\d{4})", re.I)

def _is_primary_code(text):
    if not text: return False
    t = text.strip().upper()
    if t in ARTICOLI_NOTI: return True
    for prefix in ARTICOLI_NOTI:
        if prefix.endswith('-') and t.startswith(prefix.upper()):
            return True
    return False

def _normalizza_unita(u):
    m = {"bottiglia":"Bottiglie","bottiglie":"Bottiglie","fardello":"Fardelli","fardelli":"Fardelli",
         "cartone":"Cartoni","cartoni":"Cartoni","cluster":"Cluster","porzione":"Porzioni","porzioni":"Porzioni",
         "collo":"Colli","colli":"Colli","fetta":"Fette","fette":"Fette","brick":"Brick",
         "confezione":"Confezioni","confezioni":"Confezioni","manifesto":"Manifesti","manifesti":"Manifesti",
         "fascetta":"Fascette","busta":"Buste","buste":"Buste","pz":"pz"}
    return m.get(u.strip().lower(), u.title())

def _parse_qty(cell):
    if not cell or not str(cell).strip(): return []
    text = str(cell).replace("\n", " ")
    out = []
    for m in re.finditer(r"(\d+)\s+(" + UNITA_QTY + r")", text, re.I):
        out.append((int(m.group(1)), _normalizza_unita(m.group(2))))
    if not out and re.fullmatch(r"\d+", text.strip()):
        out.append((int(text.strip()), "pz"))
    return out

def _normalizza_cella_codice(raw):
    righe = [l.strip() for l in raw.split('\n')
              if l.strip() and not l.strip().startswith("Codice:")]
    if not righe: return "", ""
    codice_base, idx_base = "", 0
    for i, r in enumerate(righe):
        if _is_primary_code(r):
            codice_base, idx_base = r.strip(), i
            break
    if not codice_base:
        codice_base, idx_base = righe[0], 0
    variante_raw = " ".join(righe[idx_base + 1:]).strip()
    variante_raw = re.sub(r'\s+', ' ', variante_raw)
    variante_raw = re.sub(r'-{2,}', '-', variante_raw).strip('-').strip()
    return codice_base, variante_raw

def _estrai_da_pagina(page):
    tables = page.extract_tables()
    if not tables: return []
    tab = next((t for t in tables if t and len(t) > 1
                and "Cod. Articolo" in " ".join(str(c or "") for c in t[0])), None)
    if not tab: return []
    risultato = []
    for row in tab[1:]:
        if not row or len(row) < 4: continue
        raw_codice = str(row[0] or "").strip()
        if not raw_codice: continue
        codice_base, variante_raw = _normalizza_cella_codice(raw_codice)
        if not codice_base: continue
        descrizione = re.sub(r'\s+', ' ', str(row[1] or "").replace('\n', ' ')).strip()
        try: kg = Decimal(str(row[2] or "0").replace(",", ".").strip() or "0")
        except: kg = Decimal("0")
        quantita = _parse_qty(str(row[3] or "").strip())
        if not quantita and "10-GEL" in codice_base:
            porz = str(row[4] or "").strip() if len(row) > 4 else ""
            if porz.isdigit(): quantita = [(int(porz), "pz")]
        if not quantita: continue
        risultato.append({"codice_base": codice_base, "variante_raw": variante_raw, "descrizione": descrizione, "quantita": quantita})
    return risultato

def main():
    try:
        DDT_DIR = Path(r"g:\Il mio Drive\App\AppLogSolution\dati\CONSEGNE\CONSEGNE_13-04-2026\DDT-ORIGINALI-DIVISI")
        test_pdfs = []
        for sub in ["FRUTTA", "LATTE"]:
            folder = DDT_DIR / sub
            if folder.exists():
                test_pdfs.extend([(p, sub) for p in sorted(folder.glob("*.pdf"))[:5]])

        if not test_pdfs:
            print("Nessun PDF trovato nella cartella 13-04-2026.")
            return

        print(f"Test column-based su {len(test_pdfs)} PDF...")
        output = [f"Test column-based su {len(test_pdfs)} PDF", "=" * 65]
        totale, aggregato = 0, {}

        for pdf_path, tipo in test_pdfs:
            articoli = []
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        articoli.extend(_estrai_da_pagina(page))
            except Exception as e:
                msg = f"  WARN {pdf_path.name}: {e}"
                print(msg); output.append(msg); continue

            header = f"\n[{tipo}] {pdf_path.name}  ({len(articoli)} articoli)"
            print(header); output.append(header)
            
            for a in articoli:
                var_tag = f" | variante=[{a['variante_raw']}]" if a['variante_raw'] else ""
                lines = [f"  codice_base={a['codice_base']}{var_tag}", f"  desc={a['descrizione'][:55]}", f"  qty={a['quantita']}", ""]
                for l in lines: print(l); output.append(l)
                chiave = (a["codice_base"], a["variante_raw"])
                if chiave not in aggregato:
                    aggregato[chiave] = {"base": a["codice_base"], "var": a["variante_raw"], "qty": []}
                aggregato[chiave]["qty"].extend(a["quantita"])
                totale += 1

        footer = ["=" * 65, f"Totale articoli estratti: {totale}", f"\nChiavi di aggregazione uniche ({len(aggregato)}):"]
        for f in footer: print(f); output.append(f)
        
        for (base, var), rec in sorted(aggregato.items()):
            line = f"  {base}{' + ['+var+']' if var else ''}  -> totale qty={rec['qty']}"
            print(line); output.append(line)

        with open("report_test.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(output))
        print(f"\nReport salvato in: {Path('report_test.txt').absolute()}")

    except Exception as e:
        print(f"\n!!! ERRORE CRITICO !!!\n{e}")
    finally:
        input("\n--- FINE. Premi INVIO per chiudere questa finestra ---")

if __name__ == "__main__":
    main()

import re
import io
import pdfplumber
from pypdf import PdfReader, PdfWriter

# --- REGEX DAL LEGACY ---
DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'(?:[Ll]uogo [Dd]i [Dd]estinazione|[Cc]odice [Dd]estinazione):\s*([pP]\d{4,5})')
CAP_RE = re.compile(r"\b(\d{5})\b")
PROVINCIA_RE = re.compile(r"\(([A-Z]{2})\)")
CAUSALE_RE = re.compile(r'(?:conto di|ordine e conto di)\s+([A-Z]\d{4})(?:\s+H(\d{2}))?(?:\s+(\d{3}))?', re.I)
NUM_DDT_RE = re.compile(r'DDT\s*[Nn][°º\.\s]*([A-Za-z0-9/-]+)', re.I)

def estrai_data_luogo(text: str) -> tuple[str | None, str | None, str | None]:
    data = None
    m = DATA_DDT_RE.search(text)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    luogo_m = LUOGO_RE.search(text)
    luogo = luogo_m.group(1).lower() if luogo_m else None
    
    num_m = NUM_DDT_RE.search(text)
    num_ddt = num_m.group(1).replace("/", "-") if num_m else "UNK"
    return (data, luogo, num_ddt)

def estrai_dati_consegna(text: str, codice: str, da_frutta: bool) -> dict:
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

def processa_pdf_in_memoria(pdf_bytes: bytes, etichetta: str, db_mappati: dict) -> dict:
    """
    Riceve i bytes del PDF intero, lo splitta in base alla logica legacy.
    Ritorna:
    {
      "split_files": { "P01234_14-05-2026_DDT-1.pdf": <BytesIO object>, ... },
      "nuovi_dati": { "P01234": {...} },
      "deliveries": [ ... ]
    }
    """
    nuovi_dati = {}
    deliveries_list = []
    split_files = {}
    visti = {}
    blocchi = {}
    
    reader = PdfReader(io.BytesIO(pdf_bytes))
    
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i in range(len(pdf.pages)):
            text = pdf.pages[i].extract_text() or ""
            d, l, num_ddt = estrai_data_luogo(text)
            if not d or not l: continue
            
            # Gestione anagrafica: se il codice non e' nei mappati, estraiamo
            if l not in db_mappati and l not in nuovi_dati:
                info = estrai_dati_consegna(text, l, etichetta == "FRUTTA")
                info["tipo"] = etichetta
                nuovi_dati[l] = info
                
            chiave = (l, d, num_ddt)
            if chiave not in blocchi:
                blocchi[chiave] = []
            blocchi[chiave].append((text, reader.pages[i]))
            
    # TAGLIO E SCRITTURA (In memoria)
    for chiave, lista_pagine in blocchi.items():
        writer = PdfWriter()
        l, d, num_ddt = chiave
        
        # Salva tutto il blocco intatto (la logica fascicolata FRUTTA è stata semplificata o lasciata come base: salva tutto)
        pagine_da_salvare = [p[1] for p in lista_pagine]
        for pg in pagine_da_salvare:
            writer.add_page(pg)
            
        cnt = visti.get(chiave, 0) + 1
        visti[chiave] = cnt
        fname = f"{l}_{d}_{num_ddt}_{cnt}.pdf" if cnt > 1 else f"{l}_{d}_{num_ddt}.pdf"
        
        out_stream = io.BytesIO()
        writer.write(out_stream)
        out_stream.seek(0)
        
        split_files[fname] = out_stream
        
        # Aggiungiamo ai deliveries
        deliveries_list.append({
            "codice_consegna": l,
            "data": d,
            "num_ddt": num_ddt,
            "pdf_name": fname,
            "tipo": etichetta
        })

    return {
        "split_files": split_files,
        "nuovi_dati": nuovi_dati,
        "deliveries": deliveries_list
    }

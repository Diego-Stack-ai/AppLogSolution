import io
import re
import json
import time
import math
from datetime import datetime, date
from collections import defaultdict
import firebase_admin
from firebase_admin import initialize_app, firestore, storage
from firebase_functions import https_fn, options
from pypdf import PdfReader, PdfWriter
import pdfplumber
try:
    import requests
except ImportError:
    requests = None

# --- CHIAVE API GOOGLE (da impostare nelle variabili d'ambiente della Cloud Function) ---
import os
import logging

# Configurazione logging strutturato nativo GCP
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("AppLogSolutions")

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

if not GOOGLE_MAPS_API_KEY:
    logger.error("CRITICAL: GOOGLE_MAPS_API_KEY non trovata nell'ambiente! Le API Mappe/Matrix falliranno in Cloud.")

# --- CONFIGURAZIONI ---
BUCKET_NAME = "log-solution-60007.firebasestorage.app"
DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'(?:[Ll]uogo [Dd]i [Dd]estinazione|[Cc]odice [Dd]estinazione):\s*([pP]\d{4,5})')
CAP_RE = re.compile(r"\b(\d{5})\b")
PROVINCIA_RE = re.compile(r"\(([A-Z]{2})\)")
CAUSALE_RE = re.compile(r'(?:conto di|ordine e conto di)\s+([A-Z]\d{4})(?:\s+H(\d{2}))?(?:\s+(\d{3}))?', re.I)
NUM_DDT_RE = re.compile(r'DDT\s*[Nn][°º\.\s]*([A-Za-z0-9/-]+)', re.I)

if not firebase_admin._apps:
    initialize_app()

def get_db():
    return firestore.client()

# --- GESTIONE CONFIGURAZIONI CACHE ---
_CACHED_ARTICOLI_NOTI = None
_CACHED_CONSOLIDAMENTO = None
_CACHE_TIMESTAMP = 0
CACHE_TTL = 300 # 5 minuti

def get_config_app():
    global _CACHED_ARTICOLI_NOTI, _CACHED_CONSOLIDAMENTO, _CACHE_TIMESTAMP
    now = time.time()
    
    if _CACHED_ARTICOLI_NOTI is None or _CACHED_CONSOLIDAMENTO is None or (now - _CACHE_TIMESTAMP) > CACHE_TTL:
        print("[INFO] Fetching config da Firestore (customers/DNR/anagrafica_articoli)")
        
        docs = get_db().collection('clienti').document('DNR').collection('codici articoli').stream()
        _CACHED_CONSOLIDAMENTO = {d.id: d.to_dict() for d in docs}
        
        # Merge ARTICOLI_NOTI dall'anagrafica
        noti_da_anagrafica = [d_id.upper() for d_id, data in _CACHED_CONSOLIDAMENTO.items() if data.get('is_articolo_noto') or data.get('is_wildcard_prefix')]
        _CACHED_ARTICOLI_NOTI = frozenset(noti_da_anagrafica)
            
        _CACHE_TIMESTAMP = now
        
    return _CACHED_ARTICOLI_NOTI, _CACHED_CONSOLIDAMENTO

def _estrai_data_luogo(text):
    data = None
    m = DATA_DDT_RE.search(text)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    luogo_m = LUOGO_RE.search(text)
    luogo = luogo_m.group(1).lower() if luogo_m else None
    
    num_m = NUM_DDT_RE.search(text)
    num_ddt = num_m.group(1).replace("/", "-") if num_m else "UNK"
    return data, luogo, num_ddt

def _estrai_dati_consegna_completi(text: str, codice: str, da_frutta: bool) -> dict:
    """Estrae indirizzo, cap, citta, prov e orari per nuovi clienti."""
    res = {"dest": "", "ind": "", "cap": "", "cit": "", "prov": "", "om": "", "oM": "14:00"}
    if codice.lower() not in text.lower(): return res
    
    idx_l = text.find("Luogo di destinazione")
    if idx_l < 0: return res

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

    idx_resp = text.upper().find("RESPONSABILE DEL TRASPORTO")
    blocco_prov = text[idx_resp:] if idx_resp >= 0 else text
    for prov_m in PROVINCIA_RE.finditer(blocco_prov):
        sigla = prov_m.group(1)
        if sigla == "MN" and ("Pomponesco" in blocco_prov[max(0, prov_m.start()-40):prov_m.start()] or "46030" in blocco_prov): continue
        res["prov"] = sigla
        caps = list(CAP_RE.finditer(blocco_prov[:prov_m.start()]))
        if caps:
            res["cap"] = caps[-1].group(1)
            pre = blocco_prov[caps[-1].end() : caps[-1].end() + 60]
            citta_m = re.search(r"\s*[-]?\s*([A-Za-zÀ-ÿ\s'.]+?)\s*\([A-Z]{2}\)", pre)
            if citta_m: res["cit"] = citta_m.group(1).strip().title()
        break
        
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

def _normalizza_cella_codice_base(raw: str) -> str:
    righe = [l.strip() for l in str(raw).split('\n') if l.strip() and not l.strip().startswith("Codice:")]
    if not righe: return ""
    codice_base = righe[0]
    if len(righe) > 1 and codice_base.endswith('-'):
        pezzi = righe[1].split()
        if pezzi: codice_base += pezzi[0]
    return codice_base

def _is_primary_code(t, db_articoli):
    t = str(t).strip().upper()
    if t in db_articoli: return True
    for key in db_articoli:
        if key.endswith('-') and t.startswith(key.upper()): return True
    return False

def _processa_pdf_core_logic(pdf_bytes: bytes, etichetta: str, db_mappati: dict, db_articoli: dict) -> dict:
    nuovi_dati = {}
    nuovi_orari = {}
    nuovi_articoli = {}
    deliveries_list = []
    split_files = {}
    visti = {}
    blocchi = {}
    
    reader = PdfReader(io.BytesIO(pdf_bytes))
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for i in range(len(pdf.pages)):
            pg = pdf.pages[i]
            text = pg.extract_text() or ""
            d, l, num_ddt = _estrai_data_luogo(text)
            if not d or not l: continue
            
            if l not in db_mappati and l not in nuovi_dati:
                info = _estrai_dati_consegna_completi(text, l, etichetta == "FRUTTA")
                info["tipo"] = etichetta
                nuovi_dati[l] = info
            elif l in db_mappati and l not in nuovi_orari:
                # Confronto Orari
                om_mappa = db_mappati[l].get(f"orario_min_{etichetta.lower()}") or ""
                oM_mappa = db_mappati[l].get(f"orario_max_{etichetta.lower()}") or ""
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
                        
                        if (oM_ddt and oM_ddt != oM_mappa) or (om_ddt and om_ddt != om_mappa):
                            nuovi_orari[l] = {
                                "cliente": db_mappati[l].get("cliente", ""),
                                "citta": db_mappati[l].get("citta", ""),
                                "orario_min_mappa": om_mappa,
                                "orario_max_mappa": oM_mappa,
                                "orario_min_ddt": om_ddt,
                                "orario_max_ddt": oM_ddt,
                                "data_rilevazione": d,
                                "tipo": etichetta
                            }

            # Estrazione Articoli
            try:
                tables = pg.extract_tables()
                if tables:
                    tab = next((t for t in tables if t and len(t) > 1 and "Cod. Articolo" in " ".join(str(c or "") for c in t[0])), None)
                    if tab:
                        for row in tab[1:]:
                            if row and row[0]:
                                cod_base = _normalizza_cella_codice_base(str(row[0]))
                                if cod_base and cod_base not in nuovi_articoli:
                                    if not _is_primary_code(cod_base, db_articoli):
                                        nuovi_articoli[cod_base] = {
                                            "codice_rilevato": cod_base,
                                            "rilevato_il": d,
                                            "ddt_rif": num_ddt,
                                            "cliente_rif": l,
                                            "tipo": etichetta
                                        }
            except Exception as e:
                print(f"[WARN] Errore estrazione articoli pagina {i}: {e}")
                
            chiave = (l, d, num_ddt)
            if chiave not in blocchi: blocchi[chiave] = []
            blocchi[chiave].append((text, reader.pages[i]))
            
    for chiave, lista_pagine in blocchi.items():
        writer = PdfWriter()
        l, d, num_ddt = chiave
        pagine_da_salvare = [p[1] for p in lista_pagine]
        for pg in pagine_da_salvare: writer.add_page(pg)
            
        cnt = visti.get(chiave, 0) + 1
        visti[chiave] = cnt
        fname = f"{l}_{d}_{num_ddt}_{cnt}.pdf" if cnt > 1 else f"{l}_{d}_{num_ddt}.pdf"
        
        out_stream = io.BytesIO()
        writer.write(out_stream)
        out_stream.seek(0)
        split_files[fname] = out_stream
        
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
        "nuovi_orari": nuovi_orari,
        "nuovi_articoli": nuovi_articoli,
        "deliveries": deliveries_list
    }

def normalize_code(raw, articoli_noti):
    righe = [l.strip() for l in str(raw).split('\n') if l.strip() and not l.strip().startswith("Codice:")]
    if not righe: return "", ""
    code_base, idx_base = "", -1
    for i, r in enumerate(righe):
        if r.upper() in articoli_noti:
            code_base, idx_base = r, i
            break
        for prefix in articoli_noti:
            if prefix.endswith('-') and r.upper().startswith(prefix):
                code_base, idx_base = r, i
                break
    if not code_base: code_base, idx_base = righe[0], 0
    variant = " ".join(righe[idx_base + 1:]).strip()
    variant = re.sub(r'\s+', ' ', variant)
    variant = re.sub(r'-{2,}', '-', variant).strip('-').strip()
    return code_base, variant

def consolidate_qty(codice, lista_qty, config):
    c = config.get(codice.lower()) or config.get(codice.upper()) or config.get(codice)
    if not c:
        by_unit = defaultdict(int)
        for q, u in lista_qty: by_unit[u] += q
        return " e ".join([f"{v} {k}" for k, v in sorted(by_unit.items())])
    
    u_princ = str(c.get('unita_principale') or c.get('Unita principale') or c.get('unita_princ') or '').strip()
    u_sec = str(c.get('unita_secondaria') or c.get('Unita secondaria') or c.get('unita_sec') or '').strip()
    ratio_raw = c.get('ratio') or c.get('Ratio') or 0
    try:
        ratio = int(ratio_raw)
    except:
        ratio = 0
        
    tot_sec = 0
    tot_princ = 0
    
    # Manteniamo le etichette originali per fallback
    primary_labels_found = []
    secondary_labels_found = []
    
    for q, u in lista_qty:
        ul = u.lower()
        if (u_princ and u_princ.lower() in ul) or ul in ("fardello", "fardelli", "cartoni", "cartone", "brick", "colli", "confezioni", "manifesti", "fascette"):
            tot_princ += q
            primary_labels_found.append(u)
        else:
            tot_sec += q
            secondary_labels_found.append(u)

    if ratio > 0:
        tot_princ += tot_sec // ratio
        resto_sec = tot_sec % ratio
    else:
        resto_sec = tot_sec
        
    res = []
    if tot_princ > 0:
        label_p = u_princ if u_princ else (primary_labels_found[0].capitalize() if primary_labels_found else "Unita'")
        res.append(f"{tot_princ} {label_p}")
    if resto_sec > 0:
        label_s = u_sec if u_sec else (secondary_labels_found[0].capitalize() if secondary_labels_found else "Pezzi")
        res.append(f"{resto_sec} {label_s}")
        
    if not res:
        return "0"
    return " e ".join(res)

def _registra_statistica(tipo_operazione, tempo_sec, errori=0):
    oggi = str(date.today())
    stats_ref = get_db().collection('stats_monitoring').document(oggi)
    
    try:
        doc = stats_ref.get()
        if doc.exists:
            d = doc.to_dict()
            tot_tempo = d.get('tempo_totale_sec', 0) + tempo_sec
            tot_ops = d.get('operazioni_totali', 0) + 1
            tot_err = d.get('errori_totali', 0) + errori
            
            # Specifiche per tipo API
            tipo_count = d.get(f'count_{tipo_operazione}', 0) + 1
            tipo_tempo = d.get(f'tempo_{tipo_operazione}', 0) + tempo_sec
            
            stats_ref.update({
                'tempo_totale_sec': tot_tempo,
                'operazioni_totali': tot_ops,
                'tempo_medio_globale': tot_tempo / tot_ops,
                'errori_totali': tot_err,
                f'count_{tipo_operazione}': tipo_count,
                f'tempo_medio_{tipo_operazione}': tipo_tempo / tipo_count,
                f'tempo_{tipo_operazione}': tipo_tempo
            })
        else:
            stats_ref.set({
                'data': oggi,
                'tempo_totale_sec': tempo_sec,
                'operazioni_totali': 1,
                'tempo_medio_globale': tempo_sec,
                'errori_totali': errori,
                f'count_{tipo_operazione}': 1,
                f'tempo_medio_{tipo_operazione}': tempo_sec,
                f'tempo_{tipo_operazione}': tempo_sec
            })
    except Exception as e:
        print(f"[ERROR] Registrazione statistiche fallita: {e}")

# --- CORE LOGIC FUNCTIONS ---

def core_check_giornaliero(uid):
    print("[INFO] Start check_giornaliero")
    db = get_db()
    
    # 1. DDT nuovi non assegnati
    ddts = list(db.collection('clienti').document('DNR').collection('ddt').stream())
    ddt_non_assegnati = sum(1 for d in ddts if d.to_dict().get('stato') != 'assegnato')

    # 2. Clienti senza coordinate
    clienti = list(db.collection('clienti').document('DNR').collection('raccolta clienti').stream())
    clienti_senza_coordinate = 0
    for c in clienti:
        data = c.to_dict()
        lat, lon = data.get('lat'), data.get('lon')
        if not lat or not lon or lat == '0' or lat == '0.0':
            clienti_senza_coordinate += 1

    # 3. Viaggi incompleti (senza ddt o non completati)
    viaggi = list(db.collection('clienti').document('DNR').collection('viaggi ddt').stream())
    viaggi_non_validi = 0
    for v in viaggi:
        data = v.to_dict()
        ddt_ids = data.get('ddt_ids', [])
        stato = data.get('status', 'bozza')
        if not ddt_ids or stato == 'bozza':
            viaggi_non_validi += 1

    status_code = "ok" if (ddt_non_assegnati == 0 and clienti_senza_coordinate == 0 and viaggi_non_validi == 0) else "attenzione"
    
    return {
        "status": status_code,
        "message": "Check completato",
        "errori": [],
        "data": {
            "ddt_non_assegnati": ddt_non_assegnati,
            "clienti_senza_coordinate": clienti_senza_coordinate,
            "viaggi_non_validi": viaggi_non_validi
        }
    }

def core_stats_giornaliere(uid):
    oggi = str(date.today())
    stats_doc = get_db().collection('stats_operative').document(oggi).get()
    if stats_doc.exists:
        data = stats_doc.to_dict()
        return {
            "status": "ok",
            "message": "Stats caricate",
            "errori": [],
            "data": {
                "ddt_elaborati_oggi": data.get('count_elabora_pdf', 0),
                "viaggi_creati_oggi": data.get('count_ottimizza_viaggio', 0),
                "errori_giornata": data.get('errori_totali', 0),
                "tempo_medio_sec": data.get('tempo_medio', 0)
            }
        }
    return {"status": "ok", "message": "Nessuna operazione oggi", "errori": [], "data": {"ddt_elaborati_oggi": 0, "viaggi_creati_oggi": 0, "errori_giornata": 0, "tempo_medio_sec": 0}}

def core_chiudi_giornata(uid):
    print("[INFO] Tentativo chiusura giornata")
    db = get_db()
    
    ddts = list(db.collection('clienti').document('DNR').collection('ddt').stream())
    ddt_non_assegnati = sum(1 for d in ddts if d.to_dict().get('stato') != 'assegnato')
    
    if ddt_non_assegnati > 0:
        return {
            "status": "errore",
            "message": "Impossibile chiudere la giornata: ci sono DDT non assegnati.",
            "errori": [f"{ddt_non_assegnati} DDT in sospeso"],
            "data": {}
        }
        
    viaggi = list(db.collection('clienti').document('DNR').collection('viaggi ddt').stream())
    viaggi_non_completati = [v.id for v in viaggi if v.to_dict().get('status') != 'completato']
    
    if viaggi_non_completati:
        return {
            "status": "errore",
            "message": "Impossibile chiudere la giornata: ci sono viaggi non completati.",
            "errori": [f"Viaggi aperti: {len(viaggi_non_completati)}"],
            "data": {}
        }
        
    # --- FINALIZZAZIONE RIENTRI ---
    try:
        # Trova tutti i codici assegnati nei viaggi completati
        codici_assegnati = set()
        data_giornata = ""
        for v in viaggi:
            v_data = v.to_dict()
            if not data_giornata and v_data.get('data'):
                data_giornata = v_data.get('data')
                
            for p in v_data.get('punti', []):
                if p.get('codice_frutta') and str(p.get('codice_frutta')) != 'p00000':
                    codici_assegnati.add(str(p['codice_frutta']).lower())
                if p.get('codice_latte') and str(p.get('codice_latte')) != 'p00000':
                    codici_assegnati.add(str(p['codice_latte']).lower())
                # Rientri associati come alert
                for r_alert in p.get('rientri_alert', []):
                    if r_alert.get('codice'):
                        codici_assegnati.add(str(r_alert['codice']).lower())

        if not data_giornata:
            from datetime import datetime
            data_giornata = datetime.now().strftime("%d-%m-%Y")
            
        rientri = list(db.collection('clienti').document('DNR').collection('rientri ddt').stream())
        for r_doc in rientri:
            r_data = r_doc.to_dict()
            stato = str(r_data.get('stato') or r_data.get('Stato') or '').strip().lower()
            if "lavorazione" in stato:
                r_cod = str(r_data.get('codice_consegna') or r_data.get('Codice consegna') or '').strip().lower()
                if r_cod in codici_assegnati:
                    db.collection('clienti').document('DNR').collection('rientri ddt').document(r_doc.id).update({
                        "Stato": f"allegato DDT {data_giornata}",
                        "stato": firestore.DELETE_FIELD
                    })
                else:
                    db.collection('clienti').document('DNR').collection('rientri ddt').document(r_doc.id).update({
                        "Stato": "",
                        "stato": firestore.DELETE_FIELD
                    })
    except Exception as e_r:
        print(f"[WARN] Errore durante aggiornamento finale rientri: {e_r}")


    return {
        "status": "ok",
        "message": "Giornata chiusa correttamente",
        "errori": [],
        "data": {}
    }


def core_elabora_pdf_estrazione(uid):
    start_time = time.time()
    print("[INFO] Start elabora_pdf_estrazione")
    
    if not uid:
        return {"status": "errore", "message": "Non autenticato", "errori": ["Manca UID"], "data": {}}

    bucket = storage.bucket(name=BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix="input_pdf_fornitore/"))
    pdf_blobs = [b for b in blobs if b.name.endswith(".pdf")]
    
    if not pdf_blobs:
        return {"status": "ok", "message": "Nessun file PDF trovato.", "errori": [], "data": {"ddt_estratti": 0}}

    visti = {}
    creati = 0
    errori_lista = []
    date_pulite = set()

    for blob in pdf_blobs:
        print(f"[INFO] Elaborando blob {blob.name}")
        is_frutta = "frutta" in blob.name.lower()
        tipo_label = "FRUTTA" if is_frutta else "LATTE"
        is_duplicata = is_frutta
        
        try:
            pdf_bytes = blob.download_as_bytes()
            reader = PdfReader(io.BytesIO(pdf_bytes))
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                step = 2 if is_duplicata else 1
                for i in range(0, len(pdf.pages), step):
                    try:
                        text = pdf.pages[i].extract_text() or ""
                        data_estratta, l, num_ddt = _estrai_data_luogo(text)
                        if not data_estratta or not l: continue
                        
                        # --- PULIZIA PREVENTIVA (Solo alla prima occorrenza di data/tipo nel job) ---
                        chiave_pulizia = (data_estratta, tipo_label)
                        if chiave_pulizia not in date_pulite:
                            print(f"[INFO] Pulizia preventiva per {data_estratta} - {tipo_label}")
                            cart_out_base = f"CONSEGNE/CONSEGNE_{data_estratta}/DDT-ORIGINALI-DIVISI/{tipo_label}/"
                            
                            # 1. Svuota Storage
                            blobs_del = bucket.list_blobs(prefix=cart_out_base)
                            for b in blobs_del: b.delete()
                            
                            # 2. Svuota Firestore (deliveries)
                            old_docs = db.collection('clienti').document('DNR').collection('deliveries')\
                                         .where('data', '==', data_estratta).where('tipo', '==', tipo_label).stream()
                            for od in old_docs: od.reference.delete()
                            
                            date_pulite.add(chiave_pulizia)

                        d = data_estratta
                        chiave = (d, l)
                        cnt = visti.get(chiave, 0) + 1
                        visti[chiave] = cnt
                        
                        fname = f"{l}_{d}_{cnt}.pdf" if cnt > 1 else f"{l}_{d}.pdf"
                        cart_out = f"CONSEGNE/CONSEGNE_{d}/DDT-ORIGINALI-DIVISI/{tipo_label}"
                        percorso_out = f"{cart_out}/{fname}"
                        
                        writer = PdfWriter()
                        writer.add_page(reader.pages[i])
                        out_io = io.BytesIO()
                        writer.write(out_io)
                        out_io.seek(0)
                        
                        out_blob = bucket.blob(percorso_out)
                        out_blob.upload_from_file(out_io, content_type="application/pdf")
                        creati += 1

                        # ── PUNTO #4: Ricerca cliente con Tripla Chiave ──────────────
                        cliente_nome = l
                        cliente_trovato = False
                        cliente_doc = None

                        # Cerca il cliente per codice (rispettando la regola p00000)
                        cliente_doc, _ = _cerca_cliente_cloud(l)

                        if cliente_doc:
                            cliente_nome = (cliente_doc.get('cliente')
                                            or cliente_doc.get('nome_consegna')
                                            or l)
                            cliente_trovato = True

                        # Determina i codici frutta/latte per costruire la chiave tripla
                        cod_frutta = l if tipo_label == "FRUTTA" else "p00000"
                        cod_latte  = l if tipo_label == "LATTE"  else "p00000"
                        if cliente_doc:
                            cod_frutta = cliente_doc.get('codice_frutta', cod_frutta)
                            cod_latte  = cliente_doc.get('codice_latte',  cod_latte)

                        stato_iniziale = "pronto" if cliente_trovato else "da_mappare"

                        get_db().collection('clienti').document('DNR').collection('ddt').add({
                            "codice_cliente": l,
                            "codice_frutta":  cod_frutta,
                            "codice_latte":   cod_latte,
                            "tripla_chiave":  _build_tripla_chiave(cod_frutta, cod_latte, cliente_nome),
                            "nome": cliente_nome,
                            "data": d,
                            "storage_path": percorso_out,
                            "tipo": tipo_label,
                            "stato": stato_iniziale
                        })

                    except Exception as ex_page:
                        err_msg = f"Errore pagina {i} in {blob.name}: {ex_page}"
                        print(f"[ERROR] {err_msg}")
                        errori_lista.append(err_msg)
                        
        except Exception as e:
            err_msg = f"Errore apertura PDF {blob.name}: {e}"
            print(f"[ERROR] {err_msg}")
            errori_lista.append(err_msg)
            
    for blob in pdf_blobs:
        try:
            archived_name = blob.name.replace("input_pdf_fornitore/", "archivio_lenzuoloni_processati/")
            bucket.copy_blob(blob, bucket, archived_name)
            blob.delete()
        except Exception as e_arch:
            print(f"[ERROR] Errore archiviazione {blob.name}: {e_arch}")

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[INFO] End elabora_pdf_estrazione. Tempo: {elapsed:.2f}s, Creati: {creati}, Errori: {len(errori_lista)}")
    
    _registra_statistica('elabora_pdf', elapsed, len(errori_lista))

    status_code = "ok" if not errori_lista else "parziale"
    if not creati and errori_lista: status_code = "errore"

    return {
        "status": status_code,
        "message": f"Taglio completato in {elapsed:.2f}s",
        "errori": errori_lista,
        "data": {
            "date_elaborate": list(date_valide),
            "ddt_estratti": creati,
            "tempo_sec": elapsed
        }
    }


# ─── PUNTO #4: PROTEZIONE TRIPLA CHIAVE ────────────────────────────────────────

def _build_tripla_chiave(cod_f: str, cod_l: str, nome: str) -> str:
    """
    Costruisce la chiave univoca: COD_F|COD_L|NOME (normalizzati lowercase).
    Questa chiave identifica univocamente il cliente anche se ha p00000 come codice.
    """
    cf = str(cod_f).strip().lower()
    cl = str(cod_l).strip().lower()
    n  = str(nome).strip().lower()
    return f"{cf}|{cl}|{n}"


def _cerca_cliente_cloud(codice: str):
    """
    Cerca un cliente in Firestore per codice (frutta o latte).
    Restituisce (doc_dict, doc_id) o (None, None).
    Il codice viene cercato in modo case-insensitive.
    IMPORTANTE: se il codice e' p00000 NON restituiamo mai un match univoco
    perche' p00000 e' un codice fittizio usato per clienti multipli.
    """
    codice_l = codice.strip().lower()

    # p00000 e' un codice fittizio: non usare come chiave di ricerca singola
    if codice_l == "p00000":
        return None, None

    db = get_db()
    col = db.collection('clienti').document('DNR').collection('raccolta clienti')

    # Cerca per codice_frutta
    for val in [codice_l, codice_l.upper()]:
        docs = list(col.where('codice_frutta', '==', val).limit(1).stream())
        if docs:
            return docs[0].to_dict(), docs[0].id

    # Cerca per codice_latte
    for val in [codice_l, codice_l.upper()]:
        docs = list(col.where('codice_latte', '==', val).limit(1).stream())
        if docs:
            return docs[0].to_dict(), docs[0].id

    return None, None


def _salva_nuovo_cliente_tripla_chiave(cod_f: str, cod_l: str, nome: str, extra: dict = None):
    """
    Crea un nuovo cliente in Firestore usando la TRIPLA CHIAVE come ID documento.
    In questo modo due clienti diversi con lo stesso p00000 NON si sovrascrivono.
    """
    chiave = _build_tripla_chiave(cod_f, cod_l, nome)
    doc_id = chiave.replace("/", "_").replace(".", "_").replace(" ", "_")[:500]
    doc_data = {
        "codice_frutta": str(cod_f).strip().lower(),
        "codice_latte":  str(cod_l).strip().lower(),
        "nome_consegna": nome,
        "cliente": nome,
        "tripla_chiave": chiave,
        "stato": "da_mappare"
    }
    if extra:
        doc_data.update(extra)
    get_db().collection('clienti').document('DNR').collection('raccolta clienti').document(doc_id).set(doc_data, merge=True)
    return doc_id



def _haversine(p1, p2):
    """Calcolo distanza in linea d'aria (fallback di emergenza)."""
    R = 6371000  # metri
    lat1, lon1 = math.radians(p1['lat']), math.radians(p1['lon'])
    lat2, lon2 = math.radians(p2['lat']), math.radians(p2['lon'])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return int(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

def _cache_key(p1, p2):
    """Chiave univoca per la coppia di punti (arrotondata a 5 decimali = ~1 metro)."""
    return f"{round(p1['lat'],5)},{round(p1['lon'],5)}_{round(p2['lat'],5)},{round(p2['lon'],5)}"

def _leggi_cache_firestore(p1, p2):
    """Legge il valore dalla cache distanze su Firestore. Restituisce dist in metri o None."""
    try:
        key = _cache_key(p1, p2)
        doc = get_db().collection('distanze_cache').document(key).get()
        if doc.exists:
            return doc.to_dict().get('dist')
        
        # Fallback bidirezionale: controlla la rotta inversa
        rev_key = _cache_key(p2, p1)
        doc_rev = get_db().collection('distanze_cache').document(rev_key).get()
        if doc_rev.exists:
            return doc_rev.to_dict().get('dist')
    except:
        pass
    return None

def _scrivi_cache_firestore(coppie):
    """Scrive un batch di distanze su Firestore (max 500 per batch)."""
    if not coppie:
        return
    try:
        db = get_db()
        batch = db.batch()
        for key, dist, dur in coppie:
            ref = db.collection('distanze_cache').document(key)
            batch.set(ref, {'dist': dist, 'dur': dur}, merge=True)
        batch.commit()
        print(f"[CACHE] Scritte {len(coppie)} nuove distanze su Firestore.")
    except Exception as e:
        print(f"[CACHE] Errore scrittura Firestore: {e}")

def _crea_matrice_distanze_cloud(punti, errori_lista):
    """
    Crea la matrice delle distanze (in metri) con 3 livelli:
      1. Cache Firestore (gratis, istantaneo)
      2. Google Distance Matrix API (preciso, a pagamento)
      3. Haversine (fallback di emergenza)
    """
    n = len(punti)
    matrix = [[0] * n for _ in range(n)]
    da_calcolare = []  # coppie (i, j) mancanti dalla cache

    # FASE 1: lettura dalla cache Firestore
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dist = _leggi_cache_firestore(punti[i], punti[j])
            if dist is not None:
                matrix[i][j] = dist
            else:
                da_calcolare.append((i, j))

    if not da_calcolare:
        print(f"[CACHE] Matrice completa da cache Firestore ({n} punti).")
        return matrix

    print(f"[MATRIX] {len(da_calcolare)} coppie mancanti → richiesta a Google Distance Matrix API.")

    # FASE 2: Google Distance Matrix API con chunking 10x10
    nuove_coppie = []

    if not GOOGLE_MAPS_API_KEY or not requests:
        print("[MATRIX] Chiave API mancante o requests non disponibile → uso Haversine.")
        for i, j in da_calcolare:
            matrix[i][j] = _haversine(punti[i], punti[j])
        return matrix

    CHUNK_SIZE = 10
    try:
        # Raggruppa per righe (origins)
        righe_da_calc = sorted(set(i for i, j in da_calcolare))
        for r_start in range(0, n, CHUNK_SIZE):
            r_end = min(r_start + CHUNK_SIZE, n)
            righe_blocco = [i for i in range(r_start, r_end) if i in righe_da_calc]
            if not righe_blocco:
                continue

            origins = "|".join([f"{punti[i]['lat']},{punti[i]['lon']}" for i in righe_blocco])

            for c_start in range(0, n, CHUNK_SIZE):
                c_end = min(c_start + CHUNK_SIZE, n)
                # Salta blocco se tutte le coppie sono già note
                coppie_blocco = [(i, j) for i in righe_blocco for j in range(c_start, c_end) if i != j and matrix[i][j] == 0]
                if not coppie_blocco:
                    continue

                destinations = "|".join([f"{punti[j]['lat']},{punti[j]['lon']}" for j in range(c_start, c_end)])
                url = (
                    f"https://maps.googleapis.com/maps/api/distancematrix/json"
                    f"?origins={origins}&destinations={destinations}&key={GOOGLE_MAPS_API_KEY}"
                )
                resp = requests.get(url, timeout=10).json()

                if resp.get('status') == 'OK':
                    for i_local, row_data in enumerate(resp['rows']):
                        i_global = righe_blocco[i_local]
                        for j_local, elem in enumerate(row_data['elements']):
                            j_global = c_start + j_local
                            if i_global == j_global:
                                continue
                            if elem.get('status') == 'OK':
                                dist = elem['distance']['value']
                                dur = elem['duration']['value']
                                matrix[i_global][j_global] = dist
                                nuove_coppie.append((_cache_key(punti[i_global], punti[j_global]), dist, dur))
                            else:
                                # Fallback puntuale
                                matrix[i_global][j_global] = _haversine(punti[i_global], punti[j_global])
                elif resp.get('status') == 'REQUEST_DENIED':
                    print("[MATRIX] ERRORE: API Google negata. Controlla la chiave GOOGLE_MAPS_API_KEY.")
                    # Fallback totale
                    for i, j in da_calcolare:
                        if matrix[i][j] == 0:
                            matrix[i][j] = _haversine(punti[i], punti[j])
                    return matrix

    except Exception as e:
        print(f"[MATRIX] Eccezione durante API Google: {e} → Haversine di emergenza.")
        for i, j in da_calcolare:
            if matrix[i][j] == 0:
                matrix[i][j] = _haversine(punti[i], punti[j])

    # FASE 3: Salva le nuove distanze in cache Firestore
    _scrivi_cache_firestore(nuove_coppie)

    return matrix


def core_ottimizza_viaggio(viaggio_id):
    start_time = time.time()
    print("[INFO] Start ottimizza_viaggio")

    if not viaggio_id:
        return {"status": "errore", "message": "viaggio_id mancante", "errori": ["viaggio_id mancante"], "data": {}}
        
    doc_ref = get_db().collection('clienti').document('DNR').collection('viaggi ddt').document(viaggio_id)
    doc_viaggio = doc_ref.get()
    if not doc_viaggio.exists:
        return {"status": "errore", "message": "Viaggio non trovato", "errori": ["Viaggio non trovato"], "data": {}}
    viaggio = doc_viaggio.to_dict()
    
    punti = viaggio.get('punti', [])
    if not punti:
        return {"status": "errore", "message": "Viaggio vuoto (nessun punto)", "errori": ["Punti vuoti"], "data": {}}
    
    # BLOCCO ERRORI LOGICI: Impossibile ottimizzare se i DDT sono < 2
    if len(punti) < 2:
        return {
            "status": "errore", 
            "message": "Impossibile ottimizzare: servono almeno 2 DDT nel viaggio.", 
            "errori": ["Meno di 2 DDT"], 
            "data": {}
        }
        
    errori_lista = []

    # Costruisci punti come lista di dict con lat/lon
    punti_norm = []
    for i, p in enumerate(punti):
        try:
            punti_norm.append({'lat': float(p['lat']), 'lon': float(p.get('lon', p.get('lng', 0)))})
        except:
            punti_norm.append({'lat': 0.0, 'lon': 0.0})
            errori_lista.append(f"Coordinate invalide punto {i}")

    distance_matrix = _crea_matrice_distanze_cloud(punti_norm, errori_lista)

    try:
        from ortools.constraint_solver import routing_enums_pb2
        from ortools.constraint_solver import pywrapcp

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.time_limit.seconds = 10 
        
        solution = routing.SolveWithParameters(search_parameters)
        
        if solution:
            ordine_visita = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                ordine_visita.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
                
            punti_ottimizzati = [punti[i] for i in ordine_visita]
            
            # Update stato viaggio a "ottimizzato"
            doc_ref.update({
                "punti_ottimizzati": punti_ottimizzati,
                "ordine_visita": ordine_visita,
                "status": "ottimizzato"
            })
            
            end_time = time.time()
            elapsed = end_time - start_time
            _registra_statistica('ottimizza_viaggio', elapsed, len(errori_lista))

            return {
                "status": "ok" if not errori_lista else "parziale",
                "message": f"Ottimizzazione in {elapsed:.2f}s",
                "errori": errori_lista,
                "data": {
                    "viaggio_id": viaggio_id,
                    "ordine_visita": ordine_visita,
                    "tempo_sec": elapsed
                }
            }
        else:
            return {"status": "errore", "message": "Nessuna soluzione trovata da OR-Tools", "errori": errori_lista + ["Nessuna route"], "data": {}}
            
    except Exception as e_opt:
        err_msg = f"Errore runtime OR-Tools: {e_opt}"
        return {"status": "errore", "message": "Eccezione OR-Tools", "errori": errori_lista + [err_msg], "data": {}}

def core_genera_distinta_viaggio(viaggio_id):
    start_time = time.time()
    print("[INFO] Start genera_distinta_viaggio")
    
    if not viaggio_id:
        return {"status": "errore", "message": "viaggio_id mancante", "errori": ["viaggio_id mancante"], "data": {}}

    doc_ref = get_db().collection('customers').document('DNR').collection('Viaggi_DNR').document(viaggio_id)
    doc_viaggio = doc_ref.get()
    if not doc_viaggio.exists:
        return {"status": "errore", "message": "Viaggio non trovato", "errori": ["Viaggio non trovato"], "data": {}}
    viaggio = doc_viaggio.to_dict()
    
    # BLOCCO ERRORI LOGICI: Impedire distinta se non ottimizzato
    if viaggio.get('status', 'bozza') != 'ottimizzato':
        return {
            "status": "errore", 
            "message": "Operazione respinta. Il viaggio deve essere ottimizzato prima di generare la distinta.",
            "errori": ["Stato viaggio non ottimizzato"], 
            "data": {}
        }
    
    ddt_ids = viaggio.get('ddt_ids', [])
    if not ddt_ids:
        return {"status": "errore", "message": "Viaggio vuoto (nessun ddt_ids)", "errori": ["Viaggio senza ddt_ids"], "data": {}}

    articoli_noti, config_cons = get_config_app()
    bucket = storage.bucket(name=BUCKET_NAME)
    accumulatore = defaultdict(lambda: {"qty": [], "desc": ""})
    errori_lista = []
    
    for ddt_id in ddt_ids:
        try:
            ddt_doc = get_db().collection('clienti').document('DNR').collection('ddt').document(ddt_id).get()
            if not ddt_doc.exists: continue
            ddt = ddt_doc.to_dict()
            blob = bucket.blob(ddt['storage_path'])
            if not blob.exists(): continue
            
            pdf_bytes = blob.download_as_bytes()
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if not tables: continue
                    tab = next((t for t in tables if t and "Cod. Articolo" in str(t[0])), None)
                    if not tab: continue
                    for row in tab[1:]:
                        if not row or not row[0]: continue
                        base, var = normalize_code(row[0], articoli_noti)
                        desc = str(row[1] or "").replace('\n', ' ').strip()
                        qty_raw = str(row[3] or "")
                        qty_parsed = [(int(m.group(1)), m.group(2).title()) 
                                      for m in re.finditer(r"(\d+)\s+([A-Za-z]+)", qty_raw)]
                        if qty_parsed:
                            key = (base, var)
                            accumulatore[key]["qty"].extend(qty_parsed)
                            if not accumulatore[key]["desc"]:
                                accumulatore[key]["desc"] = desc
        except Exception as e_ddt:
            err_msg = f"Errore su DDT {ddt_id}: {e_ddt}"
            errori_lista.append(err_msg)

    if not accumulatore:
        return {"status": "errore", "message": "Nessun articolo estratto dai DDT", "errori": errori_lista, "data": {}}

    report_items = []
    for (codice, variante), dati in sorted(accumulatore.items()):
        report_items.append({
            "codice": codice,
            "variante": variante,
            "descrizione": dati["desc"],
            "display_qty": consolidate_qty(codice, dati["qty"], config_cons)
        })

    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm

    try:
        out_pdf = io.BytesIO()
        c = canvas.Canvas(out_pdf, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 16)
        
        data_viaggio = viaggio.get('data', 'Sconosciuta')
        nome_giro = viaggio.get('nome_giro', 'Sconosciuto')
        c.drawString(2*cm, height - 2*cm, f"DISTINTA DI CARICO - {nome_giro} del {data_viaggio}")
        
        c.setFont("Helvetica-Bold", 10)
        y = height - 3.5*cm
        
        c.drawString(2*cm, y, "Codice")
        c.drawString(6*cm, y, "Descrizione / Variante")
        c.drawString(14*cm, y, "Quantità")
        c.line(2*cm, y-0.2*cm, 19*cm, y-0.2*cm)
        y -= 0.8*cm

        c.setFont("Helvetica", 10)
        for item in report_items:
            if y < 2*cm:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 2*cm
            c.drawString(2*cm, y, item['codice'])
            
            desc_var = item['descrizione']
            if item['variante']:
                desc_var += f" ({item['variante']})"
            if len(desc_var) > 45: desc_var = desc_var[:42] + "..."
            c.drawString(6*cm, y, desc_var)
            
            c.drawString(14*cm, y, item['display_qty'])
            y -= 0.6*cm

        c.save()
        out_pdf.seek(0)
        
        data_formattata = data_viaggio.replace('/', '-')
        pdf_path = f"CONSEGNE/CONSEGNE_{data_formattata}/DISTINTE_VIAGGIO/{viaggio_id}.pdf"
        distinta_blob = bucket.blob(pdf_path)
        distinta_blob.upload_from_file(out_pdf, content_type="application/pdf")
        pdf_url = f"gs://{BUCKET_NAME}/{pdf_path}"
        
        # AGGIORNA STATO A COMPLETATO E AGGIORNA STATO DDT AD ASSEGNATO
        doc_ref.update({"status": "completato"})
        for ddt_id in ddt_ids:
            get_db().collection('clienti').document('DNR').collection('ddt').document(ddt_id).update({"stato": "assegnato"})
            
    except Exception as e_pdf:
        err_msg = f"Errore generazione PDF: {e_pdf}"
        return {"status": "errore", "message": "Fallita generazione PDF", "errori": errori_lista + [err_msg], "data": {}}
    
    end_time = time.time()
    elapsed = end_time - start_time
    _registra_statistica('genera_distinta', elapsed, len(errori_lista))

    return {
        "status": "ok" if not errori_lista else "parziale",
        "message": f"Distinta generata in {elapsed:.2f}s",
        "errori": errori_lista,
        "data": {
            "viaggio_id": viaggio_id,
            "articoli_totali": len(report_items),
            "pdf_url": pdf_url,
            "tempo_sec": elapsed
        }
    }


# ─── PUNTO #3: MAPPE AUTISTI CON STRADE CURVE (GOOGLE DIRECTIONS) ─────────────

DEPOT_CLOUD = {"lat": 45.442805, "lon": 11.714498, "nome": "DEPOSITO VEGGIANO"}
AVG_SPEED_KMH = 45
TIME_PER_STOP_MIN = 8

def _get_directions_data(percorso_punti):
    """Chiama Directions API. Restituisce (km, sec_guida, lista_polylines)."""
    punti_pieni = [DEPOT_CLOUD] + percorso_punti + [DEPOT_CLOUD]
    km_tot, sec_tot, polylines, nuove_coppie = 0.0, 0, [], []

    km_stima = sum(_haversine(punti_pieni[k], punti_pieni[k+1]) / 1000 * 1.3
                   for k in range(len(punti_pieni) - 1))
    sec_stima = int((km_stima / AVG_SPEED_KMH) * 3600)

    if not GOOGLE_MAPS_API_KEY or not requests:
        return round(km_stima, 1), sec_stima, []

    CHUNK = 20
    try:
        for i in range(0, len(punti_pieni) - 1, CHUNK):
            sub = punti_pieni[i:i + CHUNK + 1]
            origin = f"{sub[0]['lat']},{sub[0]['lon']}"
            dest   = f"{sub[-1]['lat']},{sub[-1]['lon']}"
            waypts = "|".join([f"{p['lat']},{p['lon']}" for p in sub[1:-1]])
            url = (f"https://maps.googleapis.com/maps/api/directions/json"
                   f"?origin={origin}&destination={dest}"
                   f"&waypoints={waypts}&key={GOOGLE_MAPS_API_KEY}")
            r = requests.get(url, timeout=8).json()
            if r.get("status") == "OK":
                route = r["routes"][0]
                legs  = route["legs"]
                km_tot  += sum(l["distance"]["value"] for l in legs) / 1000.0
                sec_tot += sum(l["duration"]["value"]  for l in legs)
                polylines.append(route["overview_polyline"]["points"])
                if len(legs) == len(sub) - 1:
                    for idx_l, leg in enumerate(legs):
                        key = _cache_key(sub[idx_l], sub[idx_l + 1])
                        nuove_coppie.append((key, leg["distance"]["value"], leg["duration"]["value"]))
    except Exception as e:
        print(f"[DIRECTIONS] Eccezione: {e}")

    if nuove_coppie:
        _scrivi_cache_firestore(nuove_coppie)

    final_km  = round(km_tot  if km_tot  > 0 else km_stima, 1)
    final_sec = sec_tot if sec_tot > 0 else sec_stima
    return final_km, final_sec, polylines


def _genera_html_mappa(viaggio_id, punti, km, sec_guida, polylines):
    """Genera HTML mappa mobile-first con polyline strade vere."""
    t_guida_min = sec_guida // 60
    t_sosta_min = len(punti) * TIME_PER_STOP_MIN
    t_tot_min   = t_guida_min + t_sosta_min

    def fmt_min(m):
        hh, mm = divmod(m, 60)
        return f"{hh}h {mm}m" if hh > 0 else f"{mm}m"

    fermate_html = ""
    for idx, p in enumerate(punti):
        nome = p.get("nome", p.get("codice_cliente", f"Tappa {idx+1}"))
        ind  = p.get("indirizzo", "")
        lat  = p.get("lat", "")
        lon  = p.get("lon", p.get("lng", ""))
        nav  = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
        
        is_parz = any(r.get("is_parziale") for r in p.get("rientri_alert", []) if isinstance(r, dict))
        warn_class = " warning" if is_parz else ""
        
        fermate_html += (
            f'<div class="card" id="card-{idx}" onclick="selectCard({idx})">'
            f'<div class="stop-num{warn_class}">{idx+1}</div>'
            f'<div class="stop-info"><span class="name">{nome}</span><span class="addr">{ind}</span></div>'
            f'<a href="{nav}" target="_blank" class="btn-nav">&#x2BAC;</a></div>'
        )

    punti_js_list = []
    for p in punti:
        is_parz = any(r.get("is_parziale") for r in p.get("rientri_alert", []) if isinstance(r, dict))
        punti_js_list.append({
            "lat": float(p.get("lat", 0)),
            "lng": float(p.get("lon", p.get("lng", 0))),
            "nome": p.get("nome", ""),
            "is_parziale": is_parz
        })
    punti_js     = json.dumps(punti_js_list)
    polylines_js = json.dumps(polylines)

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>Mappa {viaggio_id}</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
<script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&libraries=geometry&callback=initMap" async defer></script>
<style>
:root{{--p:#4f46e5;--accent:#10b981}}
body,html{{margin:0;padding:0;height:100%;font-family:'Outfit',sans-serif;overflow:hidden}}
.main-container{{display:flex;flex-direction:column;height:100vh}}
#map{{height:42vh;width:100%;background:#dfe5eb}}
#sidebar{{flex:1;display:flex;flex-direction:column;background:white;border-top:2px solid #cbd5e1;overflow:hidden}}
.header{{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}}
.trip-title{{margin:0;font-size:.65rem;font-weight:800;text-transform:uppercase;color:var(--accent)}}
.stats-row{{display:flex;gap:16px;margin-top:4px}}
.stat-val{{font-size:.85rem;font-weight:800;color:white}}
.stat-lbl{{font-size:.52rem;color:#94a3b8;text-transform:uppercase}}
#delivery-list{{flex:1;overflow-y:auto;padding:8px;background:#f1f5f9;padding-bottom:60px}}
.card{{background:white;border-radius:12px;padding:10px;margin-bottom:8px;display:grid;grid-template-columns:42px 1fr 40px;gap:8px;align-items:center;border:1px solid #cbd5e1;cursor:pointer;transition:all .2s}}
.card.active{{border-color:var(--p);border-left:5px solid var(--p);background:#eef2ff}}
.stop-num{{width:32px;height:32px;background:var(--p);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px}}
.stop-num.warning {{
background: repeating-linear-gradient(45deg, #000, #000 4px, #f59e0b 4px, #f59e0b 8px) !important;
color: white !important;
text-shadow: 1px 1px 2px black, -1px -1px 2px black, 0px 0px 3px black;
border: 2px solid black;
}}
.stop-info{{display:flex;flex-direction:column;gap:3px;min-width:0}}
.name{{font-size:.85rem;font-weight:800;color:#1e293b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.addr{{font-size:.75rem;color:#64748b;font-weight:600}}
.btn-nav{{background:var(--accent);color:white;width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:20px}}
</style>
</head>
<body>
<div class="main-container">
<div id="map"></div>
<div id="sidebar">
<div class="header">
<p class="trip-title">&#x1F69B; {viaggio_id}</p>
<div class="stats-row">
<div><div class="stat-val">&#x1F6E3;&#xFE0F; {km} km</div><div class="stat-lbl">Km Reali</div></div>
<div><div class="stat-val">&#x1F552; {fmt_min(t_guida_min)}</div><div class="stat-lbl">Guida</div></div>
<div><div class="stat-val">&#x23F1;&#xFE0F; {fmt_min(t_tot_min)}</div><div class="stat-lbl">Totale</div></div>
<div><div class="stat-val">&#x1F4E6; {len(punti)}</div><div class="stat-lbl">Tappe</div></div>
</div>
</div>
<div id="delivery-list">{fermate_html}</div>
</div>
</div>
<script>
const PUNTI={punti_js};
const POLYLINES={polylines_js};
const DEPOT={{lat:{DEPOT_CLOUD["lat"]},lng:{DEPOT_CLOUD["lon"]}}};
let map,markers=[];
function initMap(){{
map=new google.maps.Map(document.getElementById("map"),{{
center:PUNTI.length?{{lat:PUNTI[0].lat,lng:PUNTI[0].lng}}:DEPOT,
zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true}});
POLYLINES.forEach(enc=>{{
const path=google.maps.geometry.encoding.decodePath(enc);
new google.maps.Polyline({{path,geodesic:true,strokeColor:"#4f46e5",strokeOpacity:.85,strokeWeight:4,map}});
}});
new google.maps.Marker({{position:DEPOT,map,
icon:{{path:google.maps.SymbolPath.CIRCLE,scale:14,fillColor:"#1e293b",fillOpacity:1,strokeWeight:0}},
label:{{text:"D",color:"white",fontWeight:"bold"}}}});
PUNTI.forEach((p,i)=>{{
let fillColor = "#4f46e5";
let strokeColor = "white";
let strokeWeight = 2;
let labelColor = "white";
if (p.is_parziale) {{
fillColor = "#f59e0b";
strokeColor = "#000000";
strokeWeight = 3;
labelColor = "#000000";
}}
const m=new google.maps.Marker({{position:{{lat:p.lat,lng:p.lng}},map,
icon:{{path:google.maps.SymbolPath.CIRCLE,scale:13,fillColor:fillColor,fillOpacity:1,strokeWeight:strokeWeight,strokeColor:strokeColor}},
label:{{text:String(i+1),color:labelColor,fontWeight:"bold",fontSize:"12px"}}}});
m.addListener("click",()=>selectCard(i));
markers.push(m);
}});
}}
function selectCard(i){{
document.querySelectorAll(".card").forEach(c=>c.classList.remove("active"));
const card=document.getElementById("card-"+i);
if(card){{card.classList.add("active");card.scrollIntoView({{behavior:"smooth",block:"center"}});}}
if(markers[i]){{map.panTo(markers[i].getPosition());map.setZoom(16);}}
}}
</script>
</body></html>"""


def core_genera_mappa_autista(viaggio_id):
    start_time = time.time()
    if not viaggio_id:
        return {"status": "errore", "message": "viaggio_id mancante", "errori": ["viaggio_id mancante"], "data": {}}

    doc_ref = get_db().collection('customers').document('DNR').collection('Viaggi_DNR').document(viaggio_id)
    doc_viaggio = doc_ref.get()
    if not doc_viaggio.exists:
        return {"status": "errore", "message": "Viaggio non trovato", "errori": ["Viaggio non trovato"], "data": {}}

    viaggio = doc_viaggio.to_dict()
    punti = viaggio.get("punti_ottimizzati") or viaggio.get("punti", [])
    if not punti:
        return {"status": "errore", "message": "Viaggio senza punti", "errori": ["Punti vuoti"], "data": {}}

    punti_norm = []
    for p in punti:
        try:
            punti_norm.append({**p, "lat": float(p["lat"]), "lon": float(p.get("lon", p.get("lng", 0)))})
        except:
            pass

    km, sec_guida, polylines = _get_directions_data(punti_norm)
    html = _genera_html_mappa(viaggio_id, punti_norm, km, sec_guida, polylines)

    bucket = storage.bucket(name=BUCKET_NAME)
    data_viaggio = viaggio.get("data", "sconosciuta").replace("/", "-")
    html_path = f"CONSEGNE/CONSEGNE_{data_viaggio}/MAPPE_AUTISTI/{viaggio_id}.html"
    blob = bucket.blob(html_path)
    blob.upload_from_string(html.encode("utf-8"), content_type="text/html; charset=utf-8")
    url_pubblica = f"https://storage.googleapis.com/{BUCKET_NAME}/{html_path}"

    doc_ref.update({
        "mappa_url": url_pubblica,
        "km_reali": km,
        "t_guida_min": sec_guida // 60,
        "t_tot_min": (sec_guida // 60) + len(punti_norm) * TIME_PER_STOP_MIN
    })

    elapsed = time.time() - start_time
    _registra_statistica("genera_mappa_autista", elapsed)

    return {
        "status": "ok",
        "message": f"Mappa generata in {elapsed:.2f}s ({len(polylines)} tratti stradali)",
        "errori": [],
        "data": {
            "viaggio_id": viaggio_id,
            "mappa_url": url_pubblica,
            "km_reali": km,
            "t_guida_min": sec_guida // 60,
            "n_polylines": len(polylines),
            "tempo_sec": elapsed
        }
    }


# ─── PUNTO #5: RICALCOLO ISTANTANEO PERCORSO RIORDINATO ──────────────────────

def core_ricalcola_percorso(viaggio_id, nuovi_punti, num_locked=0):
    """
    Riceve un viaggio con le tappe riordinate manualmente dal frontend.
    - Le prime `num_locked` tappe sono H10 bloccate (non si toccano).
    - Le restanti vengono riottimizzate con OR-Tools + Distance Matrix API.
    - Salva il nuovo ordine su Firestore e rigenera la mappa autista.
    """
    start_time = time.time()

    if not viaggio_id or not nuovi_punti:
        return {"status": "errore", "message": "viaggio_id o punti mancanti", "errori": [], "data": {}}

    doc_ref = get_db().collection('customers').document('DNR').collection('Viaggi_DNR').document(viaggio_id)
    doc_viaggio = doc_ref.get()
    if not doc_viaggio.exists:
        return {"status": "errore", "message": "Viaggio non trovato", "errori": [], "data": {}}

    # Normalizza coordinate
    punti_norm = []
    for p in nuovi_punti:
        try:
            punti_norm.append({**p, "lat": float(p["lat"]), "lon": float(p.get("lon", p.get("lng", 0)))})
        except:
            pass

    # Parti bloccate (H10) + parti da riottimizzare
    locked   = punti_norm[:num_locked]
    to_optim = punti_norm[num_locked:]

    punti_finali = locked[:]

    if to_optim:
        try:
            from ortools.constraint_solver import routing_enums_pb2, pywrapcp

            start_node = locked[-1] if locked else DEPOT_CLOUD
            all_locs   = [start_node] + to_optim + [DEPOT_CLOUD]
            n          = len(all_locs)

            dist_matrix = _crea_matrice_distanze_cloud(all_locs, [])

            manager = pywrapcp.RoutingIndexManager(n, 1, [0], [n - 1])
            routing = pywrapcp.RoutingModel(manager)

            def dist_cb(fi, ti):
                return dist_matrix[manager.IndexToNode(fi)][manager.IndexToNode(ti)]

            cb_idx = routing.RegisterTransitCallback(dist_cb)
            routing.SetArcCostEvaluatorOfAllVehicles(cb_idx)
            params = pywrapcp.DefaultRoutingSearchParameters()
            params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            params.time_limit.seconds = 8

            sol = routing.SolveWithParameters(params)
            if sol:
                idx = routing.Start(0)
                while not routing.IsEnd(idx):
                    node = manager.IndexToNode(idx)
                    if 0 < node < n - 1:
                        punti_finali.append(all_locs[node])
                    idx = sol.Value(routing.NextVar(idx))
            else:
                punti_finali.extend(to_optim)

        except Exception as e:
            print(f"[RICALCOLA] OR-Tools fallback ordine manuale: {e}")
            punti_finali.extend(to_optim)

    # Ricalcola KM e tempi con Directions API
    km, sec_guida, polylines = _get_directions_data(punti_finali)

    # Aggiorna Firestore
    doc_ref.update({
        "punti_ottimizzati": punti_finali,
        "ordine_manuale":    True,
        "num_locked":        num_locked,
        "km_reali":          km,
        "t_guida_min":       sec_guida // 60,
        "t_tot_min":         (sec_guida // 60) + len(punti_finali) * TIME_PER_STOP_MIN,
        "status":            "ottimizzato"
    })

    # Rigenera mappa autista aggiornata
    viaggio = doc_viaggio.to_dict()
    html = _genera_html_mappa(viaggio_id, punti_finali, km, sec_guida, polylines)
    bucket = storage.bucket(name=BUCKET_NAME)
    data_v = viaggio.get("data", "sconosciuta").replace("/", "-")
    html_path = f"CONSEGNE/CONSEGNE_{data_v}/MAPPE_AUTISTI/{viaggio_id}.html"
    blob = bucket.blob(html_path)
    blob.upload_from_string(html.encode("utf-8"), content_type="text/html; charset=utf-8")
    url_pubblica = f"https://storage.googleapis.com/{BUCKET_NAME}/{html_path}"

    elapsed = time.time() - start_time
    _registra_statistica("ricalcola_percorso", elapsed)

    return {
        "status": "ok",
        "message": f"Percorso ricalcolato in {elapsed:.2f}s ({num_locked} tappe bloccate)",
        "errori": [],
        "data": {
            "viaggio_id":    viaggio_id,
            "km_reali":      km,
            "t_guida_min":   sec_guida // 60,
            "t_tot_min":     (sec_guida // 60) + len(punti_finali) * TIME_PER_STOP_MIN,
            "n_tappe":       len(punti_finali),
            "n_locked":      num_locked,
            "mappa_url":     blob.public_url,
            "tempo_sec":     elapsed
        }
    }


# ─── PUNTO #6: RIEPILOGO FATTURAZIONE MENSILE ────────────────────────────────

# Costanti fatturazione
VALORE_DDT_STANDARD = 16.50   # € per DDT standard (Frutta e Latte)
VALORE_DDT_SPECIALE = 16.50   # € per DDT aree speciali (stessa tariffa, separati per contabilità)

AREA_RE_CLOUD = re.compile(r'(?:conto di|ordine e conto di)\s+[A-Z](\d{4,5})', re.I)
AREE_SPECIALI_FRUTTA = {"3198", "3199"}
AREE_SPECIALI_LATTE  = {"4199"}


def _estrai_area_da_storage(blob):
    """Apre un PDF DDT da Firebase Storage ed estrae il codice area numerico."""
    try:
        pdf_bytes = blob.download_as_bytes()
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = pdf.pages[0].extract_text() or ""
            m = AREA_RE_CLOUD.search(text)
            if m:
                return m.group(1)
    except:
        pass
    return None


def core_riepilogo_fatturazione(mese: str, anno: str = "2026"):
    """
    Scansiona tutti i DDT su Firebase Storage per il mese indicato.
    Restituisce i 4 contatori per la fatturazione:
      1. Frutta Standard   (tutti i DDT frutta tranne 3198/3199)
      2. Frutta Speciale   (DDT frutta con area 3198 o 3199)
      3. Latte Standard    (tutti i DDT latte tranne 4199)
      4. Latte Speciale    (DDT latte con area 4199)
    """
    start_time = time.time()

    if not mese or len(mese) != 2:
        return {"status": "errore", "message": "Mese non valido (usa MM, es: 04)", "errori": [], "data": {}}

    bucket = storage.bucket(name=BUCKET_NAME)
    prefix_base = "CONSEGNE/"

    # Cerca tutte le cartelle CONSEGNE del mese richiesto
    pattern_mese = f"-{mese}-{anno}"
    blobs_all = list(bucket.list_blobs(prefix=prefix_base))

    stats = {
        "FRUTTA": {"standard": 0, "speciali": 0, "dettaglio": {"3198": 0, "3199": 0}},
        "LATTE":  {"standard": 0, "speciali": 0, "dettaglio": {"4199": 0}}
    }
    cartelle_trovate = set()
    orfani = 0

    for blob in blobs_all:
        # Filtra solo i PDF dentro DDT-ORIGINALI-DIVISI del mese corretto
        path = blob.name
        if "DDT-ORIGINALI-DIVISI" not in path or not path.endswith(".pdf"):
            continue
        # Verifica che la cartella CONSEGNE_XX-MM-YYYY corrisponda al mese
        parts = path.split("/")
        if len(parts) < 2:
            continue
        cartella = parts[1]  # es. CONSEGNE_22-04-2026
        if pattern_mese not in cartella:
            continue

        cartelle_trovate.add(cartella)

        # Determina il tipo (FRUTTA o LATTE) dal percorso
        tipo = None
        if "/FRUTTA/" in path:
            tipo = "FRUTTA"
        elif "/LATTE/" in path:
            tipo = "LATTE"
        else:
            continue

        # Estrae il codice area dal PDF
        area = _estrai_area_da_storage(blob)

        if tipo == "FRUTTA":
            if area in AREE_SPECIALI_FRUTTA:
                stats["FRUTTA"]["speciali"] += 1
                if area in stats["FRUTTA"]["dettaglio"]:
                    stats["FRUTTA"]["dettaglio"][area] += 1
            else:
                stats["FRUTTA"]["standard"] += 1
                if not area:
                    orfani += 1
        else:  # LATTE
            if area in AREE_SPECIALI_LATTE:
                stats["LATTE"]["speciali"] += 1
                stats["LATTE"]["dettaglio"]["4199"] += 1
            else:
                stats["LATTE"]["standard"] += 1
                if not area:
                    orfani += 1

    tot_frutta  = stats["FRUTTA"]["standard"] + stats["FRUTTA"]["speciali"]
    tot_latte   = stats["LATTE"]["standard"]  + stats["LATTE"]["speciali"]
    tot_generale = tot_frutta + tot_latte

    fatturato_frutta_std  = round(stats["FRUTTA"]["standard"] * VALORE_DDT_STANDARD, 2)
    fatturato_frutta_spec = round(stats["FRUTTA"]["speciali"] * VALORE_DDT_SPECIALE, 2)
    fatturato_latte_std   = round(stats["LATTE"]["standard"]  * VALORE_DDT_STANDARD, 2)
    fatturato_latte_spec  = round(stats["LATTE"]["speciali"]  * VALORE_DDT_SPECIALE, 2)
    fatturato_totale      = round(fatturato_frutta_std + fatturato_frutta_spec +
                                   fatturato_latte_std  + fatturato_latte_spec, 2)

    elapsed = time.time() - start_time
    _registra_statistica("riepilogo_fatturazione", elapsed)

    return {
        "status": "ok",
        "message": f"Riepilogo {mese}/{anno}: {tot_generale} DDT in {elapsed:.1f}s",
        "errori": [f"{orfani} DDT senza codice area (conteggiati come Standard)"] if orfani else [],
        "data": {
            "mese": mese, "anno": anno,
            "cartelle_elaborate": len(cartelle_trovate),
            "frutta": {
                "standard":   stats["FRUTTA"]["standard"],
                "speciali":   stats["FRUTTA"]["speciali"],
                "dettaglio":  stats["FRUTTA"]["dettaglio"],
                "fatturato_standard":  fatturato_frutta_std,
                "fatturato_speciali":  fatturato_frutta_spec,
                "totale":     tot_frutta
            },
            "latte": {
                "standard":   stats["LATTE"]["standard"],
                "speciali":   stats["LATTE"]["speciali"],
                "dettaglio":  stats["LATTE"]["dettaglio"],
                "fatturato_standard":  fatturato_latte_std,
                "fatturato_speciali":  fatturato_latte_spec,
                "totale":     tot_latte
            },
            "totale_generale":    tot_generale,
            "fatturato_totale":   fatturato_totale,
            "valore_ddt_euro":    VALORE_DDT_STANDARD,
            "tempo_sec":          elapsed
        }
    }


def core_processa_job_pdf(job_id):
    start_time = time.time()
    db = get_db()
    job_ref = db.collection('clienti').document('DNR').collection('processing_jobs').document(job_id)
    job_doc = job_ref.get()
    
    if not job_doc.exists: return {"status": "errore", "message": "Job non trovato"}
    data = job_doc.to_dict()
    data_lavoro_forzata = data.get('data_lavoro')
    if data.get("status") != "uploaded": return {"status": "errore", "message": "Stato job non valido per elaborazione"}
    
    job_ref.update({"status": "processing", "updated_at": firestore.SERVER_TIMESTAMP})
    
    try:
        bucket = storage.bucket()
        path = data.get("storage_path")
        etichetta = data.get("type", "FRUTTA").upper()
        
        # 1. Carica Mappatura e Articoli
        clienti_ref = db.collection('clienti').document('DNR').collection('raccolta clienti')
        db_mappati = {}
        for doc in clienti_ref.stream():
            d = doc.to_dict()
            cf = str(d.get('codice_frutta') or '').strip().lower()
            cl = str(d.get('codice_latte') or '').strip().lower()
            if cf and cf != 'p00000' and cf != 'nan': db_mappati[cf] = d
            if cl and cl != 'p00000' and cl != 'nan': db_mappati[cl] = d
        
        articoli_ref = db.collection('clienti').document('DNR').collection('codici articoli')
        db_articoli = {doc.id: doc.to_dict() for doc in articoli_ref.stream()}
        
        # 2. Download
        blob = bucket.blob(path)
        pdf_bytes = blob.download_as_bytes()
        
        # 3. Processing
        risultato = _processa_pdf_core_logic(pdf_bytes, etichetta, db_mappati, db_articoli)
        
        split_files = risultato["split_files"]
        deliveries = risultato["deliveries"]
        nuovi_dati = risultato["nuovi_dati"]
        nuovi_orari = risultato.get("nuovi_orari", {})
        nuovi_articoli = risultato.get("nuovi_articoli", {})
        
        if not deliveries:
            job_ref.update({"status": "completed", "message": "Nessun DDT trovato nel PDF"})
            return {"status": "ok", "pdf_generati": 0}

        # Se l'utente ha scelto una data nel calendario, ha la precedenza
        if data_lavoro_forzata:
            data_elab = data_lavoro_forzata
            print(f"[INFO] Uso data forzata dal calendario: {data_elab}")
        else:
            data_elab = deliveries[0]["data"]
            print(f"[INFO] Uso data estratta dal PDF: {data_elab}")
        
        # --- PULIZIA PREVENTIVA (Sovrascrittura pulita) ---
        print(f"[INFO] Pulizia preventiva per {data_elab} - {etichetta}")
        
        # 1. Rimuovi vecchi file da Storage
        cart_out_base = f"split_ddt/{data_elab}/{etichetta}/"
        blobs_del = bucket.list_blobs(prefix=cart_out_base)
        for b in blobs_del: b.delete()
        
        # 2. Rimuovi vecchi dati (Solo Storage)
        cart_out_base = f"split_ddt/{data_elab}/{etichetta}/"
        blobs_del = bucket.list_blobs(prefix=cart_out_base)
        for b in blobs_del: b.delete()
        print(f"[INFO] Pulizia Storage completata per {data_elab}.")

        # 4. Upload split e salvataggio DDT
        for fname, out_stream in split_files.items():
            out_path = f"split_ddt/{data_elab}/{etichetta}/{fname}"
            split_blob = bucket.blob(out_path)
            split_blob.upload_from_file(out_stream, content_type='application/pdf')
            
        # 5. Salvataggio nuovi dati dinamici
        for l, info in nuovi_dati.items():
            db.collection('clienti').document('DNR').collection('nuovi codici consegna').document(l).set(info, merge=True)
            
        for l, info in nuovi_orari.items():
            db.collection('clienti').document('DNR').collection('nuovi orari mancanti').document(l).set(info, merge=True)
            
        for c, info in nuovi_articoli.items():
            doc_id = str(c).replace('/', '-').replace(' ', '_')
            db.collection('clienti').document('DNR').collection('nuovi articoli rilevati').document(doc_id).set(info, merge=True)
            
        # 6. Salvataggio Metadati Temporanei (per Step 2)
        metadata_ddt = {
            "data_elab": data_elab,
            "tipo": etichetta,
            "deliveries": deliveries
        }
        meta_path = f"split_ddt/{data_elab}/{etichetta}/ddt_estratti.json"
        bucket.blob(meta_path).upload_from_string(
            json.dumps(metadata_ddt, indent=2), 
            content_type='application/json'
        )
        
        elapsed = time.time() - start_time
        job_ref.update({
            "status": "completed",
            "data_rilevata": data_elab,
            "meta_path_json": meta_path,
            "pdf_generati": len(split_files),
            "nuovi_clienti": len(nuovi_dati),
            "nuovi_articoli": len(nuovi_articoli),
            "nuovi_orari": len(nuovi_orari),
            "nuovi_clienti_list": list(nuovi_dati.keys()),
            "nuovi_articoli_list": list(nuovi_articoli.keys()),
            "nuovi_orari_list": list(nuovi_orari.keys()),
            "tempo_sec": round(elapsed, 2),
            "updated_at": firestore.SERVER_TIMESTAMP
        })
        
        return {"status": "ok", "pdf_generati": len(split_files), "tempo_sec": round(elapsed, 2)}
        
    except Exception as e:
        job_ref.update({"status": "error", "error_message": str(e), "updated_at": firestore.SERVER_TIMESTAMP})
        return {"status": "errore", "message": str(e)}

def core_genera_report_giornaliero(uid, data_consegna):
    """
    Implementa gli step 2, 3 e 4 del workflow locale:
    - Aggrega i DDT per la data indicata (Step 2)
    - Crea la struttura della Lista Unificata (Step 3)
    - Genera la Mappa Generale delle Zone HTML (Step 4)
    """
    start_time = time.time()
    db = get_db()
    bucket = storage.bucket(name=BUCKET_NAME)
    if not data_consegna:
        return {"status": "errore", "message": "Data mancante"}

    print(f"[INFO] Generazione report per il {data_consegna}")
    
    # 1. Recupera i DDT scansionando la cartella dello Storage
    ddt_list = []
    prefix_search = f"split_ddt/{data_consegna}/"
    print(f"[INFO] Scansione Storage per data {data_consegna}...")
    
    try:
        # Caricamento bulk clienti per evitare timeout (Deadline Exceeded)
        clienti_ref = db.collection('clienti').document('DNR').collection('raccolta clienti')
        db_mappati = {}
        for doc in clienti_ref.stream():
            d = doc.to_dict()
            cf = str(d.get('codice_frutta') or '').strip().lower()
            cl = str(d.get('codice_latte') or '').strip().lower()
            if cf and cf != 'p00000' and cf != 'nan': db_mappati[cf] = d
            if cl and cl != 'p00000' and cl != 'nan': db_mappati[cl] = d

        blobs = bucket.list_blobs(prefix=prefix_search)
        for blob in blobs:
            if blob.name.endswith("ddt_estratti.json"):
                print(f"[INFO] Leggo file: {blob.name}")
                try:
                    meta_data = json.loads(blob.download_as_string())
                    for ddt in meta_data.get("deliveries", []):
                        cod = ddt.get("codice_consegna")
                        cod_l = str(cod).strip().lower()
                        cliente_info = db_mappati.get(cod_l)
                        
                        if cliente_info:
                            ddt["nome"] = cliente_info.get('cliente') or cliente_info.get('nome_consegna') or cod
                        else:
                            ddt["nome"] = cod
                        ddt_list.append(ddt)
                except Exception as e_read:
                    print(f"[ERROR] Impossibile leggere {blob.name}: {e_read}")
    except Exception as e_list:
        print(f"[ERROR] Errore scansione storage: {e_list}")

    if not ddt_list:
        # Debug Radar: vediamo cosa c'e' effettivamente nello Storage
        cercati = [f"split_ddt/{data_consegna}/FRUTTA/ddt_estratti.json", f"split_ddt/{data_consegna}/LATTE/ddt_estratti.json"]
        try:
            prefix_check = f"split_ddt/{data_consegna}/"
            blobs_esistenti = list(bucket.list_blobs(prefix=prefix_check))
            files_trovati = [b.name for b in blobs_esistenti]
            msg = f"Nessun dato trovato per il {data_consegna}. Percorsi attesi: {', '.join(cercati)}. Nello Storage vedo: {', '.join(files_trovati) if files_trovati else 'NULLA'}"
        except Exception as e_debug:
            msg = f"Nessun dato trovato per il {data_consegna} e errore durante il radar: {e_debug}"
            
        print(f"[ERROR] {msg}")
        return {"status": "errore", "message": msg}

    # 2. Aggrega per cliente (Step 2 locale)
    punti_map = {} # chiave: tripla_chiave o codice_cliente
    for ddt in ddt_list:
        cod = ddt.get('codice_consegna')
        cod_l = str(cod).strip().lower()
        tipo = ddt.get('tipo', 'FRUTTA')
        
        # Cerchiamo il cliente nel dizionario pre-caricato
        cliente_info = db_mappati.get(cod_l)
        nome = ddt.get('nome', cod)
        
        # Identificativo unico del punto di consegna (per evitare duplicati nello stesso giro)
        chiave = ddt.get('tripla_chiave') or cod
        
        if chiave not in punti_map:
            punti_map[chiave] = {
                "nome": nome,
                "indirizzo": cliente_info.get('indirizzo', '') if cliente_info else '',
                "codice_frutta": ddt.get('codice_frutta', 'p00000'),
                "codice_latte": ddt.get('codice_latte', 'p00000'),
                "codici_ddt_frutta": [],
                "codici_ddt_latte": [],
                "zona": (cliente_info.get('codice_zona') or cliente_info.get('zona') or '0000') if cliente_info else '0000',
                "lat": float(cliente_info.get('lat', 0)) if cliente_info and cliente_info.get('lat') else 0,
                "lon": float(cliente_info.get('lon', 0)) if cliente_info and cliente_info.get('lon') else 0,
                "rientri_alert": [] # Qui andrebbero i rientri se implementati
            }
        
        if tipo == 'FRUTTA':
            punti_map[chiave]["codici_ddt_frutta"].append(ddt.get('num_ddt', 'UNK'))
        else:
            punti_map[chiave]["codici_ddt_latte"].append(ddt.get('num_ddt', 'UNK'))

    # --- INTEGRAZIONE RIENTRI DDT ---
    try:
        rientri_ref = db.collection('clienti').document('DNR').collection('gestione_rientri')
        # Wait, the collection used in gestione.html is 'rientri ddt'!
        # Let's check gestione.html line 465: if(currentTab === 'rientri') collPath = 'clienti/DNR/rientri ddt';
        # OH WOW. In main.py I used 'gestione_rientri'. I need to use 'rientri ddt'!
        rientri_ref = db.collection('clienti').document('DNR').collection('rientri ddt')
        
        for r_doc in rientri_ref.stream():
            r_data = r_doc.to_dict() or {}
            stato = str(r_data.get('stato') or r_data.get('Stato') or '').strip().lower()
            
            # Ignora se già allegato a una data diversa da quella in elaborazione
            if 'allegato' in stato and data_consegna not in stato:
                continue
                
            r_cod = str(r_data.get('codice_consegna') or r_data.get('Codice consegna') or '').strip()
            if not r_cod: continue
            r_data_ddt = r_data.get('data_ddt') or r_data.get('Data e Num DDT') or ''
            r_cod_l = r_cod.lower()
            
            # Cerca match tra le consegne odierne
            chiave_esistente = None
            for k in punti_map.keys():
                if str(k).strip().lower() == r_cod_l:
                    chiave_esistente = k
                    break
                    
            stato_attuale = str(r_data.get('stato') or r_data.get('Stato') or '')
            nuovo_stato = ""
            
            tipo_val = str(r_data.get('Tipo') or r_data.get('tipo') or '').lower().strip()
            is_parz = bool(r_data.get('is_parziale') or False) or (tipo_val == 'parziale')
            note_val = str(r_data.get('note') or r_data.get('Note') or r_data.get('nota_integrativa') or '').strip()
            
            rientro_obj = {
                "codice": r_cod,
                "status": "red",
                "data_ddt": r_data_ddt,
                "is_parziale": is_parz,
                "nota_integrativa": note_val
            }
            
            if chiave_esistente:
                punti_map[chiave_esistente]['rientri_alert'].append(rientro_obj)
                nuovo_stato = f"allegato DDT {data_consegna}"
            else:
                # Crea punto isolato in zona speciale
                cliente_info = db_mappati.get(r_cod_l)
                if r_cod not in punti_map:
                    punti_map[r_cod] = {
                        "nome": (cliente_info.get('cliente') or cliente_info.get('nome_consegna') or r_cod) if cliente_info else r_cod,
                        "indirizzo": cliente_info.get('indirizzo', '') if cliente_info else '',
                        "codice_frutta": cliente_info.get('codice_frutta', 'p00000') if cliente_info else 'p00000',
                        "codice_latte": cliente_info.get('codice_latte', 'p00000') if cliente_info else 'p00000',
                        "codici_ddt_frutta": [],
                        "codici_ddt_latte": [],
                        "zona": "DDT_DA_INSERIRE",
                        "lat": float(cliente_info.get('lat', 0)) if cliente_info and cliente_info.get('lat') else 0,
                        "lon": float(cliente_info.get('lon', 0)) if cliente_info and cliente_info.get('lon') else 0,
                        "rientri_alert": [],
                        "_is_rientro_speciale": True
                    }
                punti_map[r_cod]['rientri_alert'].append(rientro_obj)
                nuovo_stato = "In lavorazione"
                
            # Aggiorna DB se lo stato è cambiato
            if stato_attuale != nuovo_stato:
                try:
                    db.collection('clienti').document('DNR').collection('rientri ddt').document(r_doc.id).update({
                        'Stato': nuovo_stato,
                        'stato': firestore.DELETE_FIELD
                    })
                except Exception as e_up:
                    print(f"[WARN] Impossibile aggiornare stato rientro {r_doc.id}: {e_up}")
    except Exception as e_r:
        print(f"[ERROR] Errore integrazione rientri: {e_r}")

    # 3. Organizza per Zone (Step 4 locale)
    zone_dict = defaultdict(list)
    for p in punti_map.values():
        zone_dict[p['zona']].append(p)
        
    # Colori per le zone (stessa palette dello script 4)
    palette = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4", "#f97316", "#14b8a6", "#6366f1", "#a855f7", "#3b82f6", "#22c55e", "#d946ef", "#84cc16"]
    
    zone_finali = []
    chiavi_zone = sorted(zone_dict.keys())
    for i, zid in enumerate(chiavi_zone):
        zone_finali.append({
            "id_zona": zid,
            "nome_giro": f"V{i+1:02d}" if zid != "0000" else "SENZA ZONA",
            "color": palette[i % len(palette)],
            "lista_punti": zone_dict[zid]
        })

    # 4. Salvataggio file JSON storici nello Storage (Standard Johnson)
    path_base = f"REPORTS/{data_consegna}"
    
    # punti_consegna.json
    bucket.blob(f"{path_base}/punti_consegna.json").upload_from_string(
        json.dumps(list(punti_map.values()), indent=2), content_type='application/json'
    )
    
    # punti_consegna_unificati_Johnson.json
    bucket.blob(f"{path_base}/punti_consegna_unificati_Johnson.json").upload_from_string(
        json.dumps(list(punti_map.values()), indent=2), content_type='application/json'
    )
    
    # viaggi_giornalieri_Johnson.json
    bucket.blob(f"{path_base}/viaggi_giornalieri_Johnson.json").upload_from_string(
        json.dumps(zone_finali, indent=2), content_type='application/json'
    )

    # 5. Genera KML (zona_google_{data}.kml)
    kml_content = _genera_kml_zone(data_consegna, zone_finali)
    bucket.blob(f"{path_base}/zona_google_{data_consegna}.kml").upload_from_string(
        kml_content.encode('utf-8'), content_type='application/vnd.google-earth.kml+xml'
    )

    # 6. Genera HTML Mappa Generale (4_mappa_zone_google.html)
    html_mappa = _genera_html_mappa_generale(data_consegna, zone_finali)
    path_mappa = f"{path_base}/4_mappa_zone_google.html"
    blob_mappa = bucket.blob(path_mappa)
    blob_mappa.upload_from_string(html_mappa.encode('utf-8'), content_type='text/html')
    
    # 7. Registra il report su Firestore
    report_meta = {
        "data_consegna": data_consegna,
        "punti_totali": len(punti_map),
        "zone_totali": len(zone_finali),
        "mappa_url": blob_mappa.public_url,
        "created_at": firestore.SERVER_TIMESTAMP,
        "tipo": "REPORT_GENERALE"
    }
    db.collection('clienti').document('DNR').collection('reports_logistici').document(data_consegna).set(report_meta)
    
    elapsed = time.time() - start_time
    _registra_statistica('genera_report_generale', elapsed)
    
    # Safe return object (SERVER_TIMESTAMP is not JSON serializable)
    return_meta = report_meta.copy()
    return_meta["created_at"] = "timestamp"
    
    return {
        "status": "ok",
        "message": "Report Johnson generati con successo",
        "data": return_meta
    }

def _genera_kml_zone(data, zone_list):
    """Genera un file KML base per Google Earth"""
    kml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>',
        f'<name>Zone {data}</name>'
    ]
    for z in zone_list:
        kml.append(f'<Folder><name>Zona {z["id_zona"]}</name>')
        for p in z["lista_punti"]:
            if p["lat"] and p["lon"]:
                kml.append(f'<Placemark><name>{p["nome"]}</name><Point><coordinates>{p["lon"]},{p["lat"]},0</coordinates></Point></Placemark>')
        kml.append('</Folder>')
    kml.append('</Document></kml>')
    return "\n".join(kml)

def _genera_html_mappa_generale(data, zone_list):
    """Template semplificato della mappa generale (Step 4 locale)"""
    zone_json = json.dumps(zone_list)
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>Mappa Zone - {data}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&libraries=marker"></script>
    <style>
        :root {{ --p: #4f46e5; --bg: #f8fafc; }}
        body {{ margin: 0; font-family: 'Outfit', sans-serif; display: flex; height: 100vh; }}
        #sidebar {{ width: 350px; background: white; border-right: 1px solid #e2e8f0; overflow-y: auto; padding: 20px; }}
        #map {{ flex: 1; }}
        .zone-card {{ border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; margin-bottom: 10px; cursor: pointer; }}
        .zone-header {{ display: flex; align-items: center; gap: 10px; font-weight: 800; }}
        .color-pill {{ width: 15px; height: 15px; border-radius: 4px; }}
        .point-item {{ font-size: 0.8rem; margin-top: 5px; color: #64748b; }}
        .badge-parziale {{ background: #f59e0b; color: black; font-weight: 800; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 5px; }}
    </style>
</head>
<body>
    <div id="sidebar">
        <h2>Zone del {data}</h2>
        <div id="zone-list"></div>
    </div>
    <div id="map"></div>
    <script>
        const ZONE = {zone_json};
        let map;
        function initMap() {{
            map = new google.maps.Map(document.getElementById("map"), {{
                center: {{ lat: 45.44, lng: 11.71 }}, zoom: 10
            }});
            
            const list = document.getElementById("zone-list");
            ZONE.forEach(z => {{
                // Sidebar
                const div = document.createElement("div");
                div.className = "zone-card";
                div.innerHTML = `<div class="zone-header">
                    <div class="color-pill" style="background:${{z.color}}"></div>
                    ${{z.nome_giro}} (${{z.lista_punti.length}} tappe)
                </div>`;
                list.appendChild(div);
                
                // Markers
                z.lista_punti.forEach(p => {{
                    if(p.lat && p.lon) {{
                        let isParziale = false;
                        if (p.rientri_alert && Array.isArray(p.rientri_alert)) {{
                            isParziale = p.rientri_alert.some(r => r.is_parziale);
                        }}
                        
                        let fillColor = z.color;
                        let strokeColor = "white";
                        let strokeWeight = 2;
                        let scale = 8;
                        
                        if (isParziale) {{
                            fillColor = "#f59e0b";
                            strokeColor = "#000000";
                            strokeWeight = 3;
                            scale = 10;
                            const badge = document.createElement("div");
                            badge.className = "point-item";
                            badge.innerHTML = `• ${{p.nome}} <span class="badge-parziale">PARZIALE</span>`;
                            div.appendChild(badge);
                        }}
                        
                        new google.maps.Marker({{
                            position: {{lat: p.lat, lng: p.lon}},
                            map: map,
                            title: p.nome,
                            icon: {{
                                path: google.maps.SymbolPath.CIRCLE,
                                scale: scale,
                                fillColor: fillColor,
                                fillOpacity: 1,
                                strokeWeight: strokeWeight,
                                strokeColor: strokeColor
                            }}
                        }});
                    }}
                }});
            }});
        }}
        window.onload = initMap;
    </script>
</body>
</html>"""

# --- ENDPOINTS HTTP ---
@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=540,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def processa_job_pdf(req: https_fn.CallableRequest):
    return core_processa_job_pdf(req.data.get("job_id"))

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def elabora_pdf_estrazione(req: https_fn.CallableRequest):
    return core_elabora_pdf_estrazione(req.auth.uid if req.auth else None)

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def genera_distinta_viaggio(req: https_fn.CallableRequest):
    return core_genera_distinta_viaggio(req.data.get("viaggio_id"))

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def ottimizza_viaggio(req: https_fn.CallableRequest):
    return core_ottimizza_viaggio(req.data.get("viaggio_id"))

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def genera_mappa_autista(req: https_fn.CallableRequest):
    return core_genera_mappa_autista(req.data.get("viaggio_id"))

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def ricalcola_percorso(req: https_fn.CallableRequest):
    return core_ricalcola_percorso(
        req.data.get("viaggio_id"),
        req.data.get("punti", []),
        int(req.data.get("num_locked", 0))
    )

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=540,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def riepilogo_fatturazione(req: https_fn.CallableRequest):
    return core_riepilogo_fatturazione(
        req.data.get("mese", ""),
        req.data.get("anno", "2026")
    )

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=60,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def check_giornaliero(req: https_fn.CallableRequest):
    return core_check_giornaliero(req.auth.uid if req.auth else None)

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=60,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def stats_giornaliere(req: https_fn.CallableRequest):
    return core_stats_giornaliere(req.auth.uid if req.auth else None)

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=60,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def chiudi_giornata(req: https_fn.CallableRequest):
    return core_chiudi_giornata(req.auth.uid if req.auth else None)

@https_fn.on_call(region="europe-west1", memory=options.MemoryOption.GB_1, timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"]))
def genera_report_giornaliero(req: https_fn.CallableRequest):
    try:
        data_consegna = req.data.get("data_consegna") if isinstance(req.data, dict) else None
        return core_genera_report_giornaliero(
            req.auth.uid if req.auth else None,
            data_consegna
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "errore", "message": f"Global exception: {str(e)}"}

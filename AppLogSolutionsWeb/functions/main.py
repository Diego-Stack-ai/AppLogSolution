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
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

# --- CONFIGURAZIONI ---
BUCKET_NAME = "log-solution-60007.firebasestorage.app"
DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'(?:[Ll]uogo [Dd]i [Dd]estinazione|[Cc]odice [Dd]estinazione):\s*([pP]\d{4,5})')

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
        
        docs = get_db().collection('customers').document('DNR').collection('anagrafica_articoli').stream()
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
    return data, luogo

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
    ddts = list(db.collection('customers').document('DNR').collection('ddt').stream())
    ddt_non_assegnati = sum(1 for d in ddts if d.to_dict().get('stato') != 'assegnato')

    # 2. Clienti senza coordinate
    clienti = list(db.collection('customers').document('DNR').collection('clienti').stream())
    clienti_senza_coordinate = 0
    for c in clienti:
        data = c.to_dict()
        lat, lon = data.get('lat'), data.get('lon')
        if not lat or not lon or lat == '0' or lat == '0.0':
            clienti_senza_coordinate += 1

    # 3. Viaggi incompleti (senza ddt o non completati)
    viaggi = list(db.collection('customers').document('DNR').collection('Viaggi_DNR').stream())
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
    
    ddts = list(db.collection('customers').document('DNR').collection('ddt').stream())
    ddt_non_assegnati = sum(1 for d in ddts if d.to_dict().get('stato') != 'assegnato')
    
    if ddt_non_assegnati > 0:
        return {
            "status": "errore",
            "message": "Impossibile chiudere la giornata: ci sono DDT non assegnati.",
            "errori": [f"{ddt_non_assegnati} DDT in sospeso"],
            "data": {}
        }
        
    viaggi = list(db.collection('customers').document('DNR').collection('Viaggi_DNR').stream())
    viaggi_non_completati = [v.id for v in viaggi if v.to_dict().get('status') != 'completato']
    
    if viaggi_non_completati:
        return {
            "status": "errore",
            "message": "Impossibile chiudere la giornata: ci sono viaggi non completati.",
            "errori": [f"Viaggi aperti: {len(viaggi_non_completati)}"],
            "data": {}
        }

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
    date_valide = set()

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
                        d, l = _estrai_data_luogo(text)
                        if not d or not l: continue
                            
                        date_valide.add(d)
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

                        get_db().collection('customers').document('DNR').collection('ddt').add({
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
    col = db.collection('customers').document('DNR').collection('clienti')

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
    get_db().collection('customers').document('DNR').collection('clienti').document(doc_id).set(doc_data, merge=True)
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
        
    doc_ref = get_db().collection('customers').document('DNR').collection('Viaggi_DNR').document(viaggio_id)
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
            ddt_doc = get_db().collection('customers').document('DNR').collection('ddt').document(ddt_id).get()
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
            get_db().collection('customers').document('DNR').collection('ddt').document(ddt_id).update({"stato": "assegnato"})
            
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
        fermate_html += (
            f'<div class="card" id="card-{idx}" onclick="selectCard({idx})">'
            f'<div class="stop-num">{idx+1}</div>'
            f'<div class="stop-info"><span class="name">{nome}</span><span class="addr">{ind}</span></div>'
            f'<a href="{nav}" target="_blank" class="btn-nav">&#x2BAC;</a></div>'
        )

    punti_js     = json.dumps([{"lat": float(p.get("lat",0)), "lng": float(p.get("lon", p.get("lng",0))), "nome": p.get("nome","")} for p in punti])
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
const m=new google.maps.Marker({{position:{{lat:p.lat,lng:p.lng}},map,
icon:{{path:google.maps.SymbolPath.CIRCLE,scale:13,fillColor:"#4f46e5",fillOpacity:1,strokeWeight:2,strokeColor:"white"}},
label:{{text:String(i+1),color:"white",fontWeight:"bold",fontSize:"12px"}}}});
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
    blob.make_public()
    url_pubblica = blob.public_url

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
    blob = bucket.blob(f"CONSEGNE/CONSEGNE_{data_v}/MAPPE_AUTISTI/{viaggio_id}.html")
    blob.upload_from_string(html.encode("utf-8"), content_type="text/html; charset=utf-8")
    blob.make_public()

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


# --- ENDPOINTS HTTP ---
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

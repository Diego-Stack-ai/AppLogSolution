import io
import re
import json
import time
from datetime import datetime, date
from collections import defaultdict
import firebase_admin
from firebase_admin import initialize_app, firestore, storage
from firebase_functions import https_fn, options
from pypdf import PdfReader, PdfWriter
import pdfplumber

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

                        # CREAZIONE RECORD DDT (Stato visivo chiaro)
                        cliente_nome = l
                        cliente_trovato = False
                        
                        # Cerca prima per codice_frutta (sia case sensitive che lowercase)
                        mappatura_docs = list(get_db().collection('customers').document('DNR').collection('clienti').where('codice_frutta', '==', l).limit(1).stream())
                        if not mappatura_docs:
                            mappatura_docs = list(get_db().collection('customers').document('DNR').collection('clienti').where('codice_frutta', '==', l.lower()).limit(1).stream())
                        
                        if mappatura_docs:
                            cliente_nome = mappatura_docs[0].to_dict().get('cliente', mappatura_docs[0].to_dict().get('nome_consegna', l))
                            cliente_trovato = True
                        else:
                            # Cerchiamo su codice_latte
                            mappatura_docs = list(get_db().collection('customers').document('DNR').collection('clienti').where('codice_latte', '==', l.upper()).limit(1).stream())
                            if not mappatura_docs:
                                mappatura_docs = list(get_db().collection('customers').document('DNR').collection('clienti').where('codice_latte', '==', l.lower()).limit(1).stream())
                            if mappatura_docs:
                                cliente_nome = mappatura_docs[0].to_dict().get('cliente', mappatura_docs[0].to_dict().get('nome_consegna', l))
                                cliente_trovato = True

                        # Se cliente non trovato -> stato = 'da_mappare', altrimenti 'pronto'
                        stato_iniziale = "pronto" if cliente_trovato else "da_mappare"

                        get_db().collection('customers').document('DNR').collection('ddt').add({
                            "codice_cliente": l,
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
    import math
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0 # km
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
        a = math.sin(dLat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dLon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    distance_matrix = []
    for i, p1 in enumerate(punti):
        row = []
        try:
            val_lat = p1.get('lat')
            val_lon = p1.get('lon')
            if val_lat is None or val_lon is None:
                raise ValueError("Missing coords")
            lat1 = float(val_lat)
            lon1 = float(val_lon)
        except:
            lat1, lon1 = 0.0, 0.0
            errori_lista.append(f"Coordinate invalide punto {i}")
            
        for j, p2 in enumerate(punti):
            try:
                v2_lat = p2.get('lat')
                v2_lon = p2.get('lon')
                if v2_lat is None or v2_lon is None:
                    raise ValueError("Missing coords")
                lat2 = float(v2_lat)
                lon2 = float(v2_lon)
            except:
                lat2, lon2 = 0.0, 0.0
            dist = haversine(lat1, lon1, lat2, lon2)
            row.append(int(dist * 1000))
        distance_matrix.append(row)

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


# --- ENDPOINTS HTTP ---
@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def elabora_pdf_estrazione(req: https_fn.CallableRequest):
    return core_elabora_pdf_estrazione(req.auth.uid if req.auth else None)

@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def genera_distinta_viaggio(req: https_fn.CallableRequest):
    return core_genera_distinta_viaggio(req.data.get("viaggio_id"))

@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def ottimizza_viaggio(req: https_fn.CallableRequest):
    return core_ottimizza_viaggio(req.data.get("viaggio_id"))

@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=60,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def check_giornaliero(req: https_fn.CallableRequest):
    return core_check_giornaliero(req.auth.uid if req.auth else None)

@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=60,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def stats_giornaliere(req: https_fn.CallableRequest):
    return core_stats_giornaliere(req.auth.uid if req.auth else None)

@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=60,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def chiudi_giornata(req: https_fn.CallableRequest):
    return core_chiudi_giornata(req.auth.uid if req.auth else None)

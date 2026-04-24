import io
import re
import json
import time
from datetime import datetime
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
db = firestore.client()

# --- GESTIONE CONFIGURAZIONI CACHE ---
_CACHED_ARTICOLI_NOTI = None
_CACHED_CONSOLIDAMENTO = None
_CACHE_TIMESTAMP = 0
CACHE_TTL = 300 # 5 minuti

def get_config_app():
    global _CACHED_ARTICOLI_NOTI, _CACHED_CONSOLIDAMENTO, _CACHE_TIMESTAMP
    now = time.time()
    
    if _CACHED_ARTICOLI_NOTI is None or _CACHED_CONSOLIDAMENTO is None or (now - _CACHE_TIMESTAMP) > CACHE_TTL:
        print("[INFO] Fetching config da Firestore (config/app e articoli)")
        doc = db.collection('config').document('app').get()
        if doc.exists:
            _CACHED_ARTICOLI_NOTI = frozenset(doc.to_dict().get('ARTICOLI_NOTI', []))
        else:
            _CACHED_ARTICOLI_NOTI = frozenset()
            
        docs = db.collection('articoli').stream()
        _CACHED_CONSOLIDAMENTO = {d.id: d.to_dict() for d in docs}
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
    if codice not in config:
        by_unit = defaultdict(int)
        for q, u in lista_qty: by_unit[u] += q
        return " e ".join([f"{v} {k}" for k, v in sorted(by_unit.items())])
    
    c = config[codice]
    u_princ, u_sec, ratio = c.get('unita_princ', ''), c.get('unita_sec', ''), int(c.get('ratio', 1))
    tot_sec = sum(q for q, u in lista_qty if u_sec.lower() in u.lower())
    tot_princ = sum(q for q, u in lista_qty if u_princ.lower() in u.lower())
    if ratio > 0:
        tot_princ += tot_sec // ratio
        resto_sec = tot_sec % ratio
    else:
        resto_sec = tot_sec
        
    res = []
    if tot_princ > 0: res.append(f"{tot_princ} {u_princ}")
    if resto_sec > 0: res.append(f"{resto_sec} {u_sec}")
    return " e ".join(res)

# --- CORE LOGIC FUNCTIONS ---
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

                        # CREAZIONE RECORD DDT
                        mappatura_docs = db.collection('mappatura').where('codice_legacy', '==', l).limit(1).stream()
                        cliente_nome = l
                        for mdoc in mappatura_docs:
                            cliente_nome = mdoc.to_dict().get('cliente', l)

                        db.collection('ddt').add({
                            "codice_cliente": l,
                            "nome": cliente_nome,
                            "data": d,
                            "storage_path": percorso_out,
                            "tipo": tipo_label,
                            "stato": "pronto"
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

def core_genera_distinta_viaggio(viaggio_id):
    start_time = time.time()
    print("[INFO] Start genera_distinta_viaggio")
    
    if not viaggio_id:
        return {"status": "errore", "message": "viaggio_id mancante", "errori": ["viaggio_id mancante"], "data": {}}

    doc_viaggio = db.collection('viaggi').document(viaggio_id).get()
    if not doc_viaggio.exists:
        return {"status": "errore", "message": "Viaggio non trovato", "errori": ["Viaggio non trovato"], "data": {}}
    viaggio = doc_viaggio.to_dict()
    
    ddt_ids = viaggio.get('ddt_ids', [])
    if not ddt_ids:
        return {"status": "errore", "message": "Viaggio vuoto (nessun ddt_ids)", "errori": ["Viaggio senza ddt_ids"], "data": {}}

    articoli_noti, config_cons = get_config_app()
    bucket = storage.bucket(name=BUCKET_NAME)
    accumulatore = defaultdict(lambda: {"qty": [], "desc": ""})
    errori_lista = []
    
    # Aggregazione
    print(f"[INFO] Processando {len(ddt_ids)} DDT per il viaggio {viaggio_id}")
    for ddt_id in ddt_ids:
        try:
            ddt_doc = db.collection('ddt').document(ddt_id).get()
            if not ddt_doc.exists:
                errori_lista.append(f"DDT {ddt_id} non esiste nel db")
                continue
            ddt = ddt_doc.to_dict()
            blob = bucket.blob(ddt['storage_path'])
            if not blob.exists():
                errori_lista.append(f"Storage blob mancante per DDT {ddt_id}")
                continue
            
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
            print(f"[ERROR] {err_msg}")
            errori_lista.append(err_msg)

    if not accumulatore:
        return {"status": "errore", "message": "Nessun articolo estratto dai DDT", "errori": errori_lista, "data": {}}

    # Formattazione Dati
    report_items = []
    for (codice, variante), dati in sorted(accumulatore.items()):
        report_items.append({
            "codice": codice,
            "variante": variante,
            "descrizione": dati["desc"],
            "display_qty": consolidate_qty(codice, dati["qty"], config_cons)
        })

    # Generazione PDF (ReportLab)
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
        
        # Salva in Storage
        data_formattata = data_viaggio.replace('/', '-')
        pdf_path = f"CONSEGNE/CONSEGNE_{data_formattata}/DISTINTE_VIAGGIO/{viaggio_id}.pdf"
        distinta_blob = bucket.blob(pdf_path)
        distinta_blob.upload_from_file(out_pdf, content_type="application/pdf")
        pdf_url = f"gs://{BUCKET_NAME}/{pdf_path}"
    except Exception as e_pdf:
        err_msg = f"Errore generazione PDF: {e_pdf}"
        print(f"[ERROR] {err_msg}")
        return {"status": "errore", "message": "Fallita generazione PDF", "errori": errori_lista + [err_msg], "data": {}}
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[INFO] End genera_distinta_viaggio. Tempo: {elapsed:.2f}s, Articoli aggregati: {len(report_items)}")

    status_code = "ok" if not errori_lista else "parziale"
    
    return {
        "status": status_code,
        "message": f"Distinta generata in {elapsed:.2f}s",
        "errori": errori_lista,
        "data": {
            "viaggio_id": viaggio_id,
            "articoli_totali": len(report_items),
            "pdf_url": pdf_url,
            "tempo_sec": elapsed
        }
    }

def core_ottimizza_viaggio(viaggio_id):
    start_time = time.time()
    print("[INFO] Start ottimizza_viaggio")

    if not viaggio_id:
        return {"status": "errore", "message": "viaggio_id mancante", "errori": ["viaggio_id mancante"], "data": {}}
        
    doc_ref = db.collection('viaggi').document(viaggio_id)
    doc_viaggio = doc_ref.get()
    if not doc_viaggio.exists:
        return {"status": "errore", "message": "Viaggio non trovato", "errori": ["Viaggio non trovato"], "data": {}}
    viaggio = doc_viaggio.to_dict()
    
    punti = viaggio.get('punti', [])
    if not punti:
        return {"status": "errore", "message": "Viaggio vuoto (nessun punto)", "errori": ["Punti vuoti"], "data": {}}
    if len(punti) < 2:
        return {"status": "ok", "message": "Troppi pochi punti per ottimizzare", "errori": [], "data": {"ordine_visita": [0]}}
        
    errori_lista = []
    
    # Costruzione Matrice Distanze (Haversine locale per evitare query API costose)
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

    print(f"[INFO] Calcolo matrice distanze per {len(punti)} punti")
    distance_matrix = []
    for i, p1 in enumerate(punti):
        row = []
        try:
            lat1 = float(p1.get('lat', 0) or 0)
            lon1 = float(p1.get('lon', 0) or 0)
        except:
            lat1, lon1 = 0.0, 0.0
            errori_lista.append(f"Coordinate invalide punto {i}")
            
        for j, p2 in enumerate(punti):
            try:
                lat2 = float(p2.get('lat', 0) or 0)
                lon2 = float(p2.get('lon', 0) or 0)
            except:
                lat2, lon2 = 0.0, 0.0
                
            dist = haversine(lat1, lon1, lat2, lon2)
            row.append(int(dist * 1000)) # in metri per OR-Tools
        distance_matrix.append(row)

    try:
        from ortools.constraint_solver import routing_enums_pb2
        from ortools.constraint_solver import pywrapcp

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0) # 1 veicolo, inizio da 0
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.time_limit.seconds = 10 # Limite di sicurezza
        
        solution = routing.SolveWithParameters(search_parameters)
        
        if solution:
            ordine_visita = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                ordine_visita.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
                
            punti_ottimizzati = [punti[i] for i in ordine_visita]
            
            doc_ref.update({
                "punti_ottimizzati": punti_ottimizzati,
                "ordine_visita": ordine_visita,
                "status": "ottimizzato"
            })
            
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"[INFO] End ottimizza_viaggio. Tempo: {elapsed:.2f}s, Punti: {len(punti)}")

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
        print(f"[ERROR] {err_msg}")
        return {"status": "errore", "message": "Eccezione OR-Tools", "errori": errori_lista + [err_msg], "data": {}}


# --- ENDPOINTS HTTP ---
@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def elabora_pdf_estrazione(req: https_fn.CallableRequest):
    uid = req.auth.uid if req.auth else None
    return core_elabora_pdf_estrazione(uid)

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

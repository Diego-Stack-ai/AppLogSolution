import os
import re
import json
import urllib.parse
import requests
import openpyxl
import glob
from datetime import datetime
import math
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Carica variabili d'ambiente dal file .env nella root del progetto
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


try:
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    HAS_OR_TOOLS = True
except ImportError:
    HAS_OR_TOOLS = False

# --- CONFIGURAZIONE STRUTTURALE ---
PROG_DIR = Path(__file__).resolve().parent
ROOT_DIR = PROG_DIR.parent
WEBAPP_FOLDER = ROOT_DIR / "frontend" / "fatturazione_mappe"

# Importante: Lasciamo i drive originali così come strutturati dal cliente
DRIVE_PATH = Path(r"G:\Il mio Drive\Fatturazione")
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


DEPOT_STR = "Via alessandro volta, 25/a, 35030 Veggiano PD"
DEPOT_COORDS = {"lat": 45.442805, "lon": 11.714498, "nome": "DEPOSITO VEGGIANO", "indirizzo": DEPOT_STR}

CACHE_FILE = DRIVE_PATH / "CACHE_CONSEGNE_TOP.json"
CONFIG_FILE = DRIVE_PATH / "MESE_IN_CORSO.txt"

def get_mese_in_corso():
    if not CONFIG_FILE.exists():
        print("❌ ERRORE: MESE_IN_CORSO.txt non trovato. Esegui prima 1_Riepiloghi_Giornalieri.py!")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_cache():
    import glob
    cred_files = glob.glob(os.path.join(os.path.dirname(__file__), '..', 'backend', 'config', 'log-solution-*-firebase-adminsdk-*.json'))
    if not firebase_admin._apps and cred_files:
        cred = credentials.Certificate(cred_files[0])
        firebase_admin.initialize_app(cred)
    elif not cred_files:
        print("❌ Credenziali Firebase non trovate in backend/config/")
        return {}
        
    db = firestore.client()
    docs = db.collection("customers").document("GRAN CHEF").collection("clienti").stream()
    
    clients_cache = {}
    for doc in docs:
        d = doc.to_dict()
        ind = str(d.get('indirizzo', '')).strip().lower()
        loc = str(d.get('citta', '')).strip().lower()
        pr = str(d.get('provincia', '')).strip().lower()
        
        key1 = f"{ind}, {loc} {pr}".strip(', ')
        lat = d.get('lat')
        lng = d.get('lon') or d.get('lng')
        
        if lat and lng:
            clients_cache[key1] = {"lat": lat, "lng": lng, "lon": lng}
            
    print(f"📡 Sincronizzate {len(clients_cache)} coordinate da Firebase (GRAN CHEF) per la creazione itinerario autisti.")
    return clients_cache

def save_cache(cache):
    pass # Disabilitato perché ora usiamo Firebase centralizzato

def get_geocode(address, cache):
    clean_addr = str(address).replace(".0", "").replace("nan", "").strip().lower()
    if not clean_addr: return None
    
    if clean_addr in cache: 
        return cache[clean_addr]
        
    for k, v in cache.items():
        if k and clean_addr in k:
            return v
            
    print(f"⚠️ Coordinate mancanti in webapp (Firebase) per l'indirizzo: '{clean_addr}'")
    return None

def normalize_viaggio(zone_str):
    z = zone_str.upper().replace('  ', ' ').strip()
    if 'EXTRA' in z: return 'EXTRA'
    if 'VR' in z or 'VERONA' in z:
        if 'MN' in z or 'MANTOVA' in z: return 'VR MN'
        return 'VR'
    if 'LAGO' in z:
        if '1' in z: return 'LAGO 1'
        if '2' in z: return 'LAGO 2'
        return 'LAGO 1'
    if 'BS' in z or 'BRESCIA' in z:
        if '2' in z: return 'BS 2'
        return 'BS 1'
    if 'BELL' in z or 'BL' in z:
        if '1' in z: return 'BL 1'
        if '2' in z: return 'BL 2'
        if '3' in z: return 'BL 3'
        if '4' in z: return 'BL 4'
        if '5' in z: return 'BL 5'
        return 'BL 1'
    return z

def haversine(p1, p2):
    try:
        lat1, lon1 = float(p1.get('lat', 0)), float(p1.get('lon', p1.get('lng', 0)))
        lat2, lon2 = float(p2.get('lat', 0)), float(p2.get('lon', p2.get('lng', 0)))
    except: return 999999.0
    R = 6371 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

def crea_matrice_distanze_haversine(punti):
    n = len(punti)
    return [[int(haversine(punti[i], punti[j]) * 1000) for j in range(n)] for i in range(n)]

def ottimizza_percorso_ortools(locations, depot_coords):
    if not locations: return []
    all_locations = [depot_coords] + locations
    
    if not HAS_OR_TOOLS:
        non_visitati, percorso, corrente = locations[:], [], depot_coords
        while non_visitati:
            idx, pross = min(enumerate(non_visitati), key=lambda x: (haversine(corrente, x[1]), x[0]))
            percorso.append(pross)
            non_visitati.pop(idx)
            corrente = pross
        return percorso

    distance_matrix = crea_matrice_distanze_haversine(all_locations)
    manager = pywrapcp.RoutingIndexManager(len(all_locations), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.time_limit.seconds = 3

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        percorso_ottimizzato = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            if node_index != 0:
                percorso_ottimizzato.append(all_locations[node_index])
            index = solution.Value(routing.NextVar(index))
        return percorso_ottimizzato
    
    return locations

def format_time(minutes):
    hh, mm = divmod(int(minutes), 60)
    return f"{hh}h {mm}m" if hh > 0 else f"{mm}m"

def deploy_online():
    print("\n📦 Avvio deploy automatico Firebase per le mappe Fatturazione...")
    try:
        subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Map deploy fatturazione autisti"], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "push"], cwd=ROOT_DIR, check=True)
        subprocess.run(["firebase", "deploy", "--only", "hosting"], cwd=ROOT_DIR, shell=True, check=True)
        print("✅ Deploy Completato! Mappe live.")
    except Exception as e:
        print(f"\n⚠️ Note Deploy (potresti non essere loggato in Git o Firebase): {e}")

# --- IL NUOVO TEMPLATE HTML (STILE SCUOLE) ---
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ v_id }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}&libraries=geometry,marker&callback=initMap" async defer></script>
    <style>
        :root { --p: #e91e63; --accent: #10b981; --done: #94a3b8; --geo: #3b82f6; } /* Tema Rosato/Rosso per distinguerlo da Scuole */
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Outfit', sans-serif; background: #f8fafc; overflow: hidden; }
        .main-container { display: flex; flex-direction: column; height: 100vh; }
        #map { height: 42vh; width: 100%; background: #dfe5eb; position: relative; }
        #sidebar { flex: 1; display: flex; flex-direction: column; background: white; border-top: 2px solid #cbd5e1; overflow: hidden; }
        .header { padding: 6px 12px; background: #1e293b; color: white; border-bottom: 2px solid var(--accent); position: relative; }
        .trip-title { margin: 0; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; color: var(--accent); letter-spacing: 0.5px; }
        .reset-btn { position: absolute; right: 12px; top: 8px; font-size: 0.6rem; color: #94a3b8; text-decoration: underline; border: none; background: none; font-weight: 600; }
        .stats-row { display: flex; justify-content: space-between; gap: 8px; margin-top: 2px; }
        .stat-item { flex: 1; display: flex; flex-direction: column; align-items: start; }
        .stat-val { font-size: 0.82rem; font-weight: 800; color: white; line-height: 1; }
        .stat-lbl { font-size: 0.52rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-top: 1px; }
        #delivery-list { flex: 1; overflow-y: auto; padding: 8px; background: #f1f5f9; padding-bottom: 60px; }
        
        .card { 
            background: white; border-radius: 12px; padding: 10px; margin-bottom: 8px; 
            display: grid; grid-template-columns: 42px 1fr 52px; gap: 8px; align-items: center;
            border: 1px solid #cbd5e1; position: relative; transition: all 0.2s; 
        }
        .card.done { opacity: 0.6; background: #e2e8f0; border-color: #cbd5e1; }
        .card.done .stop-num { background: var(--done); }
        .card.done .btn-done { color: var(--accent); background: white; border: 1px solid var(--accent); }
        .card.next { border-color: var(--p); border-left: 5px solid var(--p); }
        
        .stop-num { width: 32px; height: 32px; background: var(--p); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px; flex-shrink: 0; }
        .stop-info { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
        .name { display: block; font-size: 0.85rem; font-weight: 800; color: #1e293b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .addr { font-size: 0.78rem; color: #64748b; font-weight: 600; line-height: 1.1; display: block; }
        
        .actions { display: flex; gap: 6px; width: 100%; margin-bottom: 2px; }
        .btn-done, .btn-geo { 
            flex: 1; height: 32px; border-radius: 6px; font-size: 0.6rem; font-weight: 800;
            display: flex; align-items: center; justify-content: center; gap: 4px; 
            padding: 0 4px; text-decoration: none; border: none; white-space: nowrap;
        }
        .btn-nav { background: var(--accent); color: white; width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; text-decoration: none; }
        .btn-done { background: white; color: #64748b; border: 1px solid #cbd5e1; }
        .btn-geo { background: var(--geo); color: white; }
        .btn-geo.saved { background: #1e293b; }
        .material-icons-round { font-size: 16px !important; }

        #gps-btn { position: absolute; bottom: 20px; right: 20px; background: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 1000; color: var(--p); border: none; }
        #geo-feedback { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 10px 20px; border-radius: 30px; font-size: 0.8rem; font-weight: 700; z-index: 2000; display: none; }
    </style>
</head>
<body>
    <div id="geo-feedback">Coordinate salvate!</div>
    <div class="main-container">
        <div id="map">
            <button id="gps-btn" onclick="centerOnMe()"><span class="material-icons-round">my_location</span></button>
        </div>
        <div id="sidebar">
            <div class="header">
                <div class="trip-title">🚚 FATTURAZIONE | {{ v_id }}</div>
                <button class="reset-btn" onclick="resetDone()">RESET GIRO</button>
                <div class="stats-row">
                    <div class="stat-item"><span class="stat-val">{{ km }}km</span><span class="stat-lbl">Strada st.</span></div>
                    <div class="stat-item"><span class="stat-val">{{ t_guida }}</span><span class="stat-lbl">Guida st.</span></div>
                    <div class="stat-item"><span class="stat-val">{{ t_sosta }}</span><span class="stat-lbl">Soste</span></div>
                    <div class="stat-item" style="border-left: 1px solid #334155; padding-left: 10px;"><span class="stat-val" style="color:var(--accent);">{{ t_tot }}</span><span class="stat-lbl">Totale</span></div>
                </div>
            </div>
            <div id="delivery-list">{{ cards_html|safe }}</div>
        </div>
    </div>
    
    <!-- FIREBASE SDK -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

        const firebaseConfig = {
            apiKey: "{{ firebase_api_key }}",
            authDomain: "{{ firebase_auth_domain }}",
            projectId: "{{ firebase_project_id }}"
        };

        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);

        window.saveRealCoords = async function(i) {
            if (!window.currentPos) { alert("GPS non pronto. Attendi il pallino blu."); return; }
            const p = window.data[i];
            const btn = document.querySelectorAll('.btn-geo')[i];
            try {
                btn.disabled = true;
                btn.innerHTML = '<span class="material-icons-round">sync</span>';
                
                await addDoc(collection(db, "coordinate_reali_fatturazione"), {
                    nome: p.cliente,
                    indirizzo: p.indirizzo,
                    lat: window.currentPos.lat,
                    lon: window.currentPos.lng,
                    timestamp: serverTimestamp(),
                    v_id: window.v_id
                });

                btn.classList.add('saved');
                btn.innerHTML = '<span class="material-icons-round">location_on</span> GEOLOCALIZZA';
                const f = document.getElementById('geo-feedback');
                f.style.display = 'block'; setTimeout(() => f.style.display = 'none', 3000);
            } catch (e) {
                console.error(e); alert("Errore salvataggio!");
                btn.disabled = false; btn.innerHTML = '<span class="material-icons-round">location_searching</span>';
            }
        };
    </script>

    <script>
        const v_id = "{{ v_id }}";
        const data = {{ deliveries_js|safe }};
        window.data = data; window.v_id = v_id;
        let map, markers = [], userMarker;
        window.currentPos = null;
        
        function loadStatus() {
            const saved = JSON.parse(localStorage.getItem('done_fat_' + v_id) || "[]");
            data.forEach((p, i) => {
                if (saved.includes(i)) {
                    document.querySelectorAll('.card')[i].classList.add('done');
                    const btn = document.querySelectorAll('.btn-done')[i];
                    if(btn) btn.innerHTML = '<span class="material-icons-round">check_circle</span> CONSEGNATO';
                }
            });
        }
        function toggleDone(i, event) {
            if(event) event.stopPropagation();
            const card = document.querySelectorAll('.card')[i];
            const btn = document.querySelectorAll('.btn-done')[i];
            card.classList.toggle('done');
            
            const saved = JSON.parse(localStorage.getItem('done_fat_' + v_id) || "[]");
            if (card.classList.contains('done')) {
                if (!saved.includes(i)) saved.push(i);
                if(btn) btn.innerHTML = '<span class="material-icons-round">check_circle</span> CONSEGNATO';
            } else {
                const idx = saved.indexOf(i); if (idx > -1) saved.splice(idx, 1);
                if(btn) btn.innerHTML = '<span class="material-icons-round">radio_button_unchecked</span> CONSEGNATO';
            }
            localStorage.setItem('done_fat_' + v_id, JSON.stringify(saved));
        }
        function resetDone() {
            if(confirm("Vuoi azzerare tutte le consegne?")) {
                localStorage.removeItem('done_fat_' + v_id); location.reload();
            }
        }

        async function initMap() {
            const centerPoint = data.find(p => p.lat && p.lon) || { lat: 45.4428, lng: 11.7145 };
            map = new google.maps.Map(document.getElementById("map"), { zoom: 12, center: { lat: centerPoint.lat, lng: centerPoint.lon }, disableDefaultUI: true });
            
            if (navigator.geolocation) {
                navigator.geolocation.watchPosition(pos => {
                    const myPos = { lat: pos.coords.latitude, lng: pos.coords.longitude };
                    window.currentPos = myPos;
                    if (!userMarker) {
                        userMarker = new google.maps.Marker({ position: myPos, map: map, icon: { path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: "#4285F4", fillOpacity: 1, strokeColor: "white", strokeWeight: 2 }});
                    } else { userMarker.setPosition(myPos); }
                }, err => console.log("GPS Off"), { enableHighAccuracy: true });
            }

            const ds = new google.maps.DirectionsService();
            const dr = new google.maps.DirectionsRenderer({ map, suppressMarkers: true, polylineOptions: { strokeColor: "#e91e63", strokeOpacity: 0.7, strokeWeight: 5 } });
            const waypts = data.slice(1, -1).filter(d => d.lat && d.lon).map(d => ({ location: { lat: d.lat, lng: d.lon }, stopover: true }));
            
            if (data[0].lat && data[data.length-1].lat) {
                // In Fatturazione l'ordine è già stato ottimizzato rigidamente da Python
                ds.route({ origin: { lat: data[0].lat, lng: data[0].lon }, destination: { lat: data[data.length-1].lat, lng: data[data.length-1].lon }, waypoints: waypts, travelMode: "DRIVING", optimizeWaypoints: false }, (res, st) => { if (st === "OK") dr.setDirections(res); });
            }

            const geocoder = new google.maps.Geocoder();
            const bounds = new google.maps.LatLngBounds();
            data.forEach((p, i) => {
                if (p.lat && p.lon) { addMarker(p, i, bounds); } 
                else {
                    geocoder.geocode({ address: `${p.cliente}, ${p.indirizzo}` }, (res, st) => {
                        if (st === "OK") { p.lat = res[0].geometry.location.lat(); p.lon = res[0].geometry.location.lng(); addMarker(p, i, bounds); }
                    });
                }
            });
            loadStatus();
        }

        function addMarker(p, i, bounds) {
            const m = new google.maps.Marker({ position: { lat: p.lat, lng: p.lon }, map: map, label: { text: (i).toString(), color: "white", fontSize: "10px", fontWeight: "900" } });
            if(i===0) m.setLabel("H");
            markers[i] = m; bounds.extend(m.getPosition()); map.fitBounds(bounds);
        }
        function focusOn(i) { if(markers[i]) { map.panTo(markers[i].getPosition()); map.setZoom(17); } }
        function centerOnMe() { if(userMarker) { map.panTo(userMarker.getPosition()); map.setZoom(16); } }
    </script>
</body>
</html>"""


def elabora_tutte_le_mappe_google():
    mese = get_mese_in_corso()
    INPUT_DIR = DRIVE_PATH / "Riepiloghi_Giornalieri" / mese
    
    # La nuova destinazione "mobile" locale per storico locale
    OUTPUT_DIR_LOCAL = DRIVE_PATH / "Mappe_Complete_Google" / mese / "Mobile"
    OUTPUT_DIR_LOCAL.mkdir(parents=True, exist_ok=True)
    
    # Cartella per Firebase
    WEBAPP_FOLDER.mkdir(parents=True, exist_ok=True)
        
    print(f"Avvio Mappe MOBILE stile Scuole da {INPUT_DIR}...")
    cache = load_cache()
    files = glob.glob(str(INPUT_DIR / "*.xlsx"))
    
    if not files:
        print(f"❌ Nessun file trovato nella cartella del mese: {INPUT_DIR}")
        return
        
    txt_links_content = "🚀 LINK MAPPE PER AUTISTI FATTURAZIONE\n------------------------------------------\n\n"
    
    for file_target in sorted(files):
        match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(file_target))
        if not match: continue
        data_viaggio = match.group(1)
        
        print(f"\nGenerazione Mappe Mobile per: {data_viaggio}")
        wb = openpyxl.load_workbook(file_target, data_only=True)
        ws = wb.active
        
        trips_stops = {}
        current_code = None
        col_map = {}
        
        for row in ws.iter_rows(values_only=True):
            if row[0] and isinstance(row[0], str) and "Viaggio" in row[0]:
                raw_code = re.search(r'-\s*(?:LS\s+)?(.*?)\s*del', row[0], re.IGNORECASE)
                if raw_code:
                    current_code = normalize_viaggio(raw_code.group(1))
                    if current_code not in trips_stops:
                        trips_stops[current_code] = []
                    col_map = {}
                else:
                    current_code = None
                continue
                
            if current_code and not col_map:
                row_str = " ".join([str(c).lower() for c in row if c])
                if "ragione" in row_str or "codice" in row_str:
                    for i, val in enumerate(row):
                        if val and isinstance(val, str):
                            col_map[val.lower().strip()] = i
                    continue
            
            if current_code and col_map:
                if not any(row):
                    current_code = None
                    continue
                    
                idx_rs = col_map.get('ragione sociale', 3)
                idx_ind = col_map.get('indirizzo', 4)
                idx_loc = col_map.get('località') if 'località' in col_map else col_map.get('localita')
                pr_idx = col_map.get('pr.') if 'pr.' in col_map else col_map.get('provincia')
                
                if idx_ind is not None and idx_ind < len(row) and row[idx_ind]:
                    ragione_sociale = str(row[idx_rs]).strip() if idx_rs is not None and idx_rs < len(row) and row[idx_rs] else "Sconosciuto"
                    ind = str(row[idx_ind]).strip()
                    loc = str(row[idx_loc]).strip() if idx_loc is not None and idx_loc < len(row) and row[idx_loc] else ""
                    pr = str(row[pr_idx]).strip() if pr_idx is not None and pr_idx < len(row) and row[pr_idx] else ""
                    
                    if ind and ind.lower() != 'non disponibile':
                        full_a = f"{ind}, {loc} {pr}".strip(', ')
                        if "veggiano" not in full_a.lower() or len(full_a) > 25:
                            trips_stops[current_code].append({
                                "ragione_sociale": ragione_sociale,
                                "indirizzo": full_a
                            })
                            
        for code, original_stops in trips_stops.items():
            if not original_stops: continue
            
            stops_with_coords = []
            for s in original_stops:
                coords = get_geocode(s["indirizzo"], cache)
                if coords:
                    stops_with_coords.append({
                        "nome": s["ragione_sociale"],
                        "indirizzo": s["indirizzo"],
                        "lat": coords['lat'],
                        "lng": coords.get('lng') or coords.get('lon'),
                        "lon": coords.get('lon') or coords.get('lng')
                    })
            
            if stops_with_coords:
                ordered_stops = ottimizza_percorso_ortools(stops_with_coords, DEPOT_COORDS)
                percorso_completo = [DEPOT_COORDS] + ordered_stops
                
                # Statistiche stimate fisse
                km = round(sum(haversine(percorso_completo[j], percorso_completo[j+1]) for j in range(len(percorso_completo)-1)) * 1.25, 1) if len(percorso_completo)>1 else 0
                t_guida = int(km / 45 * 60)
                t_sosta = len(ordered_stops) * 7
                t_tot = t_guida + t_sosta
                
                fname = f"{data_viaggio}_{code.replace(' ', '_')}.html"
                
                # --- STRUTTURAZIONE DELLE CARDS ---
                # Aggiungiamo anche il deposito come prima tappa zero
                deliveries = []
                for sp in percorso_completo:
                    deliveries.append({
                        "cliente": sp["nome"],
                        "indirizzo": sp["indirizzo"],
                        "lat": sp.get("lat"),
                        "lon": sp.get("lon") or sp.get("lng")
                    })
                
                cards_list = []
                for idx, d in enumerate(deliveries):
                    is_depot = (idx == 0)
                    
                    # Url di navigazione basato su Lat/Lon infallibile
                    if d.get("lat") and d.get("lon"):
                        nav_url = f"https://www.google.com/maps/dir/?api=1&destination={d['lat']},{d['lon']}&travelmode=driving"
                    else:
                        query = f"{d['cliente']} {d['indirizzo']}".replace(" ", "+")
                        nav_url = f"https://www.google.com/maps/dir/?api=1&destination={query}&travelmode=driving"
                        
                    p_addr = d["indirizzo"].split(',', 1)
                    via_parte = p_addr[0].strip()
                    resto_parte = p_addr[1].strip() if len(p_addr) > 1 else ""
                    addr_html = f'<span class="addr"><b>{via_parte}</b><br>{resto_parte}</span>'
                    
                    if is_depot:
                        c = f'''<div class="card" onclick="focusOn({idx})" style="background:#f8fafc;">
                            <div class="stop-num" style="background:#475569;">H</div>
                            <div class="stop-info"><b class="name">PARTENZA</b>{addr_html}</div>
                            <a href="{nav_url}" class="btn-nav" style="background:#475569;"><span class="material-icons-round">navigation</span></a>
                        </div>'''
                    else:
                        c = f'''<div class="card {'next' if idx == 1 else ''}" onclick="focusOn({idx})">
                            <div class="stop-num">{idx}</div>
                            <div class="stop-info">
                                <div class="actions">
                                    <button class="btn-geo" onclick="saveRealCoords({idx}, event)"><span class="material-icons-round">location_searching</span> GEOLOCA</button>
                                    <button class="btn-done" onclick="toggleDone({idx}, event)"><span class="material-icons-round">radio_button_unchecked</span> FATTO</button>
                                </div>
                                <b class="name">{d["cliente"]}</b>
                                {addr_html}
                            </div>
                            <a href="{nav_url}" class="btn-nav"><span class="material-icons-round">navigation</span></a>
                        </div>'''
                    cards_list.append(c)
                    
                cards_html = "".join(cards_list)
                
                html_fin = HTML_TEMPLATE.replace("{{ v_id }}", f"{data_viaggio} | {code}") \
                    .replace("{{ api_key }}", API_KEY) \
                    .replace("{{ km }}", str(km)) \
                    .replace("{{ t_guida }}", format_time(t_guida)) \
                    .replace("{{ t_sosta }}", format_time(t_sosta)) \
                    .replace("{{ t_tot }}", format_time(t_tot)) \
                    .replace("{{ cards_html|safe }}", cards_html) \
                    .replace("{{ deliveries_js|safe }}", json.dumps(deliveries)) \
                    .replace("{{ firebase_api_key }}", os.getenv("FIREBASE_API_KEY")) \
                    .replace("{{ firebase_auth_domain }}", os.getenv("FIREBASE_AUTH_DOMAIN")) \
                    .replace("{{ firebase_project_id }}", os.getenv("FIREBASE_PROJECT_ID"))

                
                (OUTPUT_DIR_LOCAL / fname).write_text(html_fin, encoding="utf-8")
                (WEBAPP_FOLDER / fname).write_text(html_fin, encoding="utf-8")
                
                firebase_link = f"https://log-solution-60007.web.app/fatturazione_mappe/{fname}"
                txt_links_content += f"🏎️ {data_viaggio} - {code}: {firebase_link}\n\n"
                print(f"  -> Creato split: {fname}")

    save_cache(cache)
    
    (DRIVE_PATH / "Mappe_Complete_Google" / mese / "LINK_WHATSAPP_AUTISTI.txt").write_text(txt_links_content, encoding="utf-8")
    (WEBAPP_FOLDER / "LINK_WHATSAPP_AUTISTI.txt").write_text(txt_links_content, encoding="utf-8")
    
    print("\n[SUCCESSO] Le mappe Mobile Fatturazione sono state splittate e ultimate.")
    deploy_online()

if __name__ == "__main__":
    elabora_tutte_le_mappe_google()

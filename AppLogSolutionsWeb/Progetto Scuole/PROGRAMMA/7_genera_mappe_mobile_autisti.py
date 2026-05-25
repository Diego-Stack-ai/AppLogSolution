import json
import math
import re
import requests
import subprocess
from pathlib import Path

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
ROOT_DIR = PROG_DIR.parent.parent
CONSEGNE_DIR = PROG_DIR.parent / "CONSEGNE"
WEBAPP_FOLDER = ROOT_DIR / "frontend" / "mappe_autisti"
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

DEPOT = {"lat": 45.442805, "lon": 11.714498, "nome": "DEPOSITO VEGGIANO", "indirizzo": "Via Alessandro Volta 25/a, 35030 Veggiano (PD)"}

# Tentativo di import OR-Tools
try:
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    HAS_OR_TOOLS = True
except ImportError:
    HAS_OR_TOOLS = False

def get_latest_consegne_dir():
    dirs = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
    if not dirs: return None
    return max(dirs, key=lambda d: d.stat().st_ctime)

def haversine(p1, p2):
    try:
        lat1, lon1 = float(p1.get('lat', 0)), float(p1.get('lon', p1.get('lng', 0)))
        lat2, lon2 = float(p2.get('lat', 0)), float(p2.get('lon', p2.get('lng', 0)))
    except: return 999999.0
    R = 6371 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

# --- LOGICA DI OTTIMIZZAZIONE AVANZATA (OR-TOOLS) ---

def ottimizza_percorso(punti_consegna):
    if not punti_consegna: return []
    if not HAS_OR_TOOLS: return ottimizza_percorso_legacy(punti_consegna)

    all_locations = [DEPOT] + punti_consegna
    n = len(all_locations)
    distance_matrix = [[int(haversine(all_locations[i], all_locations[j]) * 1000) for j in range(n)] for i in range(n)]
    
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.time_limit.seconds = 2

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        percorso_ottimizzato = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            if node_index != 0: percorso_ottimizzato.append(all_locations[node_index])
            index = solution.Value(routing.NextVar(index))
        return percorso_ottimizzato
    return ottimizza_percorso_legacy(punti_consegna)

def ottimizza_percorso_legacy(punti):
    non_visitati, percorso, corrente = punti[:], [], DEPOT
    while non_visitati:
        idx, pross = min(enumerate(non_visitati), key=lambda x: (haversine(corrente, x[1]), x[0]))
        percorso.append(pross)
        non_visitati.pop(idx)
        corrente = pross
    return percorso

def deploy_online():
    """Esegue il push su GitHub e il deploy su Firebase."""
    print("\n Avvio deploy automatico su GitHub e Firebase...")
    try:
        # Push su GitHub
        subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "Aggiornamento mappe autisti (auto-publish)"], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "push"], cwd=ROOT_DIR, check=True)
        print("OK Push GitHub completato.")
        
        # Deploy Firebase
        subprocess.run(["firebase", "deploy", "--only", "hosting"], cwd=ROOT_DIR, shell=True, check=True)
        print("OK Deploy Firebase completato.")
    except Exception as e:
        print(f"\nWARN Nota Deploy: {e}")

def format_time(minutes):
    hh, mm = divmod(int(minutes), 60)
    return f"{hh}h {mm}m" if hh > 0 else f"{mm}m"

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
        :root { --p: #4f46e5; --accent: #10b981; --done: #94a3b8; --geo: #3b82f6; }
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Outfit', sans-serif; background: #f8fafc; overflow: hidden; }
        .main-container { display: flex; flex-direction: column; height: 100vh; }
        #map { height: 42vh; width: 100%; background: #dfe5eb; position: relative; }
        #sidebar { flex: 1; display: flex; flex-direction: column; background: white; border-top: 2px solid #cbd5e1; overflow: hidden; }
        .header { padding: 6px 12px; background: #1e293b; color: white; border-bottom: 2px solid var(--accent); position: relative; }
        .trip-title { margin: 0; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; color: var(--accent); letter-spacing: 0.5px; }
        .back-to-links { position: absolute; right: 95px; top: 8px; font-size: 0.6rem; color: var(--accent); text-decoration: none; font-weight: 800; display: flex; align-items: center; gap: 2px; letter-spacing: 0.5px; }
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
        .btn-nav { 
            background: var(--accent); color: white; width: 44px; height: 44px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center; text-decoration: none;
        }
        .btn-done { background: white; color: #64748b; border: 1px solid #cbd5e1; }
        .btn-geo { background: var(--geo); color: white; }
        .btn-geo.saved { background: #1e293b; }
        .material-icons-round { font-size: 16px !important; }
        .btn-nav { background: var(--accent); color: white; }
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
                <div class="trip-title">🏎️ {{ v_id }} | {{ zone_str }}</div>
                <a href="../link_viaggi.html" class="back-to-links"><span class="material-icons-round" style="font-size: 10px !important;">arrow_back</span> TORNA AI LINK</a>
                <button class="reset-btn" onclick="resetDone()">RESET GIRO</button>
                <div class="stats-row">
                    <div class="stat-item"><span class="stat-val">{{ km }}km</span><span class="stat-lbl">Strada</span></div>
                    <div class="stat-item"><span class="stat-val">{{ t_guida }}</span><span class="stat-lbl">Guida</span></div>
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
            apiKey: "AIzaSyDLnhP2Q4bz2ubYwcMLiD3-qq4c220eVKw",
            authDomain: "log-solution-60007.firebaseapp.com",
            projectId: "log-solution-60007",
            storageBucket: "log-solution-60007.appspot.com",
            messagingSenderId: "343696844738",
            appId: "1:343696844738:web:b8d4e10c71fb2c67bc7d20"
        };
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);

        window.saveRealCoords = async function(i) {
            if (!window.currentPos) {
                alert("GPS non pronto. Attendi il pallino blu.");
                return;
            }
            const p = window.data[i];
            const btn = document.querySelectorAll('.btn-geo')[i];
            
            try {
                btn.disabled = true;
                btn.innerHTML = '<span class="material-icons-round">sync</span>';
                
                await addDoc(collection(db, "coordinate_reali"), {
                    codice_frutta: p.codice_frutta || "",
                    codice_latte: p.codice_latte || "",
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
                f.style.display = 'block';
                setTimeout(() => f.style.display = 'none', 3000);
            } catch (e) {
                console.error(e);
                alert("Errore salvataggio!");
                btn.disabled = false;
                btn.innerHTML = '<span class="material-icons-round">location_searching</span>';
            }
        };
    </script>

    <script>
        const v_id = "{{ v_id }}";
        const data = {{ deliveries_js|safe }};
        window.data = data; window.v_id = v_id;
        let map, markers = [], userMarker;
        window.currentPos = null;
        
        // --- GESTIONE STATO CONSEGNE ---
        function loadStatus() {
            const saved = JSON.parse(localStorage.getItem('done_' + v_id) || "[]");
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
            
            const saved = JSON.parse(localStorage.getItem('done_' + v_id) || "[]");
            if (card.classList.contains('done')) {
                if (!saved.includes(i)) saved.push(i);
                if(btn) btn.innerHTML = '<span class="material-icons-round">check_circle</span> CONSEGNATO';
            } else {
                const idx = saved.indexOf(i);
                if (idx > -1) saved.splice(idx, 1);
                if(btn) btn.innerHTML = '<span class="material-icons-round">radio_button_unchecked</span> CONSEGNATO';
            }
            localStorage.setItem('done_' + v_id, JSON.stringify(saved));
        }
        function resetDone() {
            if(confirm("Vuoi azzerare tutte le consegne di questo giro?")) {
                localStorage.removeItem('done_' + v_id);
                location.reload();
            }
        }

        // --- MAPPA E GPS ---
        async function initMap() {
            const centerPoint = data.find(p => p.lat && p.lon) || { lat: 45.4428, lon: 11.7145 };
            map = new google.maps.Map(document.getElementById("map"), { zoom: 12, center: { lat: centerPoint.lat, lng: centerPoint.lon }, disableDefaultUI: true });
            
            // GPS Real-time
            if (navigator.geolocation) {
                navigator.geolocation.watchPosition(pos => {
                    const myPos = { lat: pos.coords.latitude, lng: pos.coords.longitude };
                    window.currentPos = myPos;
                    if (!userMarker) {
                        userMarker = new google.maps.Marker({
                            position: myPos, map: map,
                            icon: { path: google.maps.SymbolPath.CIRCLE, scale: 7, fillColor: "#4285F4", fillOpacity: 1, strokeColor: "white", strokeWeight: 2 }
                        });
                    } else { userMarker.setPosition(myPos); }
                }, err => console.log("GPS Off"), { enableHighAccuracy: true });
            }

            const ds = new google.maps.DirectionsService();
            const dr = new google.maps.DirectionsRenderer({ map, suppressMarkers: true, polylineOptions: { strokeColor: "#4f46e5", strokeOpacity: 0.7, strokeWeight: 5 } });
            const waypts = data.slice(1, -1).filter(d => d.lat && d.lon).map(d => ({ location: { lat: d.lat, lng: d.lon }, stopover: true }));
            
            if (data[0].lat && data[data.length-1].lat) {
                ds.route({ origin: { lat: data[0].lat, lng: data[0].lon }, destination: { lat: data[data.length-1].lat, lng: data[data.length-1].lon }, waypoints: waypts, travelMode: "DRIVING" }, (res, st) => { if (st === "OK") dr.setDirections(res); });
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
            const m = new google.maps.Marker({ position: { lat: p.lat, lng: p.lon }, map: map, label: { text: (i+1).toString(), color: "white", fontSize: "10px", fontWeight: "900" } });
            markers[i] = m; bounds.extend(m.getPosition()); map.fitBounds(bounds);
        }

        function focusOn(i) { if(markers[i]) { map.panTo(markers[i].getPosition()); map.setZoom(17); } }
        function centerOnMe() { if(userMarker) { map.panTo(userMarker.getPosition()); map.setZoom(16); } }
    </script>
</body>
</html>"""

MASTER_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Mappa Generale Percorsi</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}&libraries=geometry,marker&callback=initMap" async defer></script>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --primary-glow: rgba(79, 70, 229, 0.15);
            --bg-dark: #0f172a;
        }
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Outfit', sans-serif; background: var(--bg-dark); overflow: hidden; }
        #map { height: 100%; width: 100%; background: #dfe5eb; position: relative; }
        
        .floating-header {
            position: fixed;
            top: 16px;
            left: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 10px 16px;
            z-index: 1000;
            box-shadow: 0 8px 32px rgba(15, 23, 42, 0.15);
            transition: all 0.3s;
        }

        .header-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .header-title {
            margin: 0;
            font-size: 1rem;
            font-weight: 800;
            color: #0f172a;
        }

        .header-subtitle {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .date-badge {
            font-size: 0.72rem;
            font-weight: 800;
            background: var(--primary-glow);
            color: var(--primary);
            padding: 1px 6px;
            border-radius: 20px;
            border: 1px solid rgba(79, 70, 229, 0.15);
        }

        .stats-badge {
            font-size: 0.72rem;
            font-weight: 600;
            color: #64748b;
        }

        .selector-container select {
            padding: 8px 12px;
            border-radius: 10px;
            border: 2px solid var(--primary);
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 700;
            color: var(--primary);
            background: white;
            outline: none;
            cursor: pointer;
        }

        /* Custom Marker shapes in Map */
        .custom-marker {
            position: absolute;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            font-size: 11px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            border: 2px solid white;
            transition: 0.2s;
            transform: translate(-50%, -100%);
        }
        .m-tonda { border-radius: 50%; }
        .m-goccia { border-radius: 50% 50% 50% 0; transform: rotate(-45deg); }
        .m-goccia span { transform: rotate(45deg); }
        .m-quadrato { border-radius: 4px; }
        .m-triangolo {
            background: transparent !important;
            border-left: 17px solid transparent;
            border-right: 17px solid transparent;
            border-bottom: 34px solid #ccc;
            width: 0 !important;
            height: 0 !important;
            border-radius: 0;
            box-shadow: none;
            border-top: none;
        }
        .m-triangolo span { position: absolute; top: 15px; left: -8px; width: 16px; }

        @media (max-width: 768px) {
            .floating-header {
                top: 0;
                left: 0;
                right: 0;
                border-radius: 0;
                border-bottom: 1px solid rgba(15, 23, 42, 0.08);
                padding: 8px 12px;
                gap: 8px;
                width: 100%;
                box-sizing: border-box;
            }
            .selector-container {
                width: 100%;
            }
            .selector-container select {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="floating-header">
        <div class="header-info">
            <h1 class="header-title">Mappa Generale Percorsi</h1>
            <div class="header-subtitle">
                <span class="date-badge">{{ data_str }}</span>
                <span class="stats-badge" id="stats-summary">0 Fermate</span>
            </div>
        </div>
        <div class="selector-container">
            <select id="giro-select" onchange="filterGiro(this.value)">
                <option value="ALL">🔍 Tutti i Viaggi</option>
            </select>
        </div>
    </div>
    <div id="map"></div>

    <script>
        const viaggi = {{ master_json|safe }};
        let map, infoWindow;
        let allMarkers = [];
        let allPolylines = [];
        let voyageMap = {};

        async function initMap() {
            const centerPoint = { lat: 45.4428, lng: 11.7145 }; // DEPOT VEGGIANO
            map = new google.maps.Map(document.getElementById("map"), {
                zoom: 10,
                center: centerPoint,
                mapId: "LOG_SOLUTION_MASTER_MAP",
                disableDefaultUI: true,
                zoomControl: true,
                streetViewControl: true
            });
            infoWindow = new google.maps.InfoWindow();

            renderAll();
        }

        function renderAll() {
            const selectEl = document.getElementById('giro-select');
            let totalFermate = 0;
            const coordCounts = {};

            viaggi.forEach((v, idx) => {
                const v_id = v.v_id;
                const color = v.color;
                const list = v.lista_punti || [];
                totalFermate += list.length;

                // Add option
                const opt = document.createElement('option');
                opt.value = v_id;
                opt.textContent = `🏎️ Giro ${v_id} (${list.length} fermate)`;
                selectEl.appendChild(opt);

                voyageMap[v_id] = { markers: [], polylines: [] };

                // Disegna polylines reali se presenti
                if (v.polylines && v.polylines.length > 0) {
                    v.polylines.forEach(encodedPath => {
                        const decoded = google.maps.geometry.encoding.decodePath(encodedPath);
                        const poly = new google.maps.Polyline({
                            path: decoded,
                            strokeColor: color,
                            strokeOpacity: 0.75,
                            strokeWeight: 5,
                            map: map
                        });
                        allPolylines.push(poly);
                        voyageMap[v_id].polylines.push(poly);
                    });
                } else {
                    // Fallback: Disegna linee rette tra i punti sequenziali
                    const coords = list.map(p => ({ lat: parseFloat(p.lat), lng: parseFloat(p.lon) })).filter(c => !isNaN(c.lat) && !isNaN(c.lng));
                    if (coords.length > 1) {
                        const poly = new google.maps.Polyline({
                            path: coords,
                            strokeColor: color,
                            strokeOpacity: 0.75,
                            strokeWeight: 4.5,
                            map: map
                        });
                        allPolylines.push(poly);
                        voyageMap[v_id].polylines.push(poly);
                    }
                }

                // Disegna marker
                list.forEach((p, pIdx) => {
                    if (!p.lat || !p.lon) return;
                    const lat = parseFloat(p.lat);
                    const lon = parseFloat(p.lon);
                    const position = { lat, lng: lon };

                    const key = `${lat.toFixed(6)}_${lon.toFixed(6)}`;
                    coordCounts[key] = (coordCounts[key] || 0) + 1;
                    const layer = coordCounts[key];

                    let shape = 'm-goccia';
                    if (layer === 2) shape = 'm-quadrato';
                    else if (layer === 3) shape = 'm-triangolo';
                    else if (layer > 3) shape = 'm-tonda';

                    const el = document.createElement("div");
                    el.className = `custom-marker ${shape}`;
                    if (shape === 'm-triangolo') {
                        el.style.borderBottomColor = color;
                    } else {
                        el.style.backgroundColor = color;
                      }
                      el.innerHTML = `<span style="pointer-events: none;">${pIdx + 1}</span>`;

                      // Use new AdvancedMarkerElement if available
                      let m;
                      if (google.maps.marker && google.maps.marker.AdvancedMarkerElement) {
                          m = new google.maps.marker.AdvancedMarkerElement({
                              position: position,
                              map: map,
                              title: p.nome,
                              content: el
                          });
                      } else {
                          m = new google.maps.Marker({
                              position: position,
                              map: map,
                              title: p.nome,
                              label: { text: (pIdx+1).toString(), color: "white", fontSize: "10px", fontWeight: "900" }
                          });
                      }

                      m.addListener(m.content ? "gmp-click" : "click", () => {
                          const ddtListText = [...(p.codici_ddt_frutta || []), ...(p.codici_ddt_latte || [])].join(', ');
                          const contentHtml = `
                              <div style="padding:10px; font-family:'Outfit', sans-serif; max-width:260px; line-height:1.4;">
                                  <div style="font-size:9px; font-weight:800; color:${color}; text-transform:uppercase; margin-bottom:2px;">🏎️ Giro ${v_id} &bull; Fermata ${pIdx + 1}</div>
                                  <div style="font-weight:800; font-size:13px; color:#0f172a; margin-bottom:4px;">${p.nome}</div>
                                  <div style="font-size:11px; color:#64748b; margin-bottom:8px; display:flex; align-items:start; gap:4px;">
                                      <span class="material-icons-round" style="font-size:14px; color:#94a3b8; margin-top:2px;">place</span>
                                      <span>${p.indirizzo}</span>
                                  </div>
                                  <button onclick="window.open('https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}&travelmode=driving', '_blank')" style="width:100%; background:${color}; color:white; border:none; padding:8px 12px; border-radius:8px; font-size:11px; font-weight:700; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:4px;">
                                      <span class="material-icons-round" style="font-size:13px;">navigation</span> NAVIGA SU GOOGLE MAPS
                                  </button>
                              </div>
                          `;
                          infoWindow.setContent(contentHtml);
                          infoWindow.open(map, m);
                      });

                      allMarkers.push(m);
                      voyageMap[v_id].markers.push(m);
                  });
              });

              document.getElementById('stats-summary').textContent = `${totalFermate} Fermate | ${viaggi.length} Viaggi`;

              if (allMarkers.length > 0) {
                  fitAll();
              }
          }

          function fitAll() {
              let bounds = new google.maps.LatLngBounds();
              allMarkers.forEach(m => bounds.extend(m.position || m.getPosition()));
              map.fitBounds(bounds);
          }

          window.filterGiro = function(selectedVid) {
              infoWindow.close();
              if (selectedVid === "ALL") {
                  allMarkers.forEach(m => m.setMap(map));
                  allPolylines.forEach(p => p.setMap(map));
                  fitAll();
                  return;
              }

              Object.keys(voyageMap).forEach(vid => {
                  const show = (vid === selectedVid);
                  voyageMap[vid].markers.forEach(m => m.setMap(show ? map : null));
                  voyageMap[vid].polylines.forEach(p => p.setMap(show ? map : null));
              });

              const active = voyageMap[selectedVid]?.markers || [];
              if (active.length > 0) {
                  let bounds = new google.maps.LatLngBounds();
                  active.forEach(m => bounds.extend(m.position || m.getPosition()));
                  map.fitBounds(bounds);
              }
          };
      </script>
  </body>
  </html>"""

def cleanup_webapp_folder():
    if WEBAPP_FOLDER.exists():
        print(f" Pulizia cartella webapp '{WEBAPP_FOLDER.name}'...")
        for f in WEBAPP_FOLDER.glob("*.html"):
            try: f.unlink()
            except: pass
        for f in WEBAPP_FOLDER.glob("*.txt"):
            try: f.unlink()
            except: pass

def main():
    target_dir = get_latest_consegne_dir()
    if not target_dir: return
    
    # 1. Pulisce la cartella pubblica per GitHub/Firebase
    cleanup_webapp_folder()
    
    json_path = target_dir / "viaggi_giornalieri_OTTIMIZZATO.json"
    if not json_path.exists():
        json_path = target_dir / "viaggi_giornalieri.json"
        
    if not json_path.exists():
        print("ERR Nessun file viaggi trovato. Esegui la mappa (BAT 2)!")
        return
    with open(json_path, "r", encoding="utf-8") as f: viaggi = json.load(f)
    viaggi = [v for v in viaggi if v.get("id_zona", "") != "DDT_DA_INSERIRE"]

    out_folder = target_dir / "MAPPE_MOBILE_WHATSAPP"
    out_folder.mkdir(exist_ok=True)
    WEBAPP_FOLDER.mkdir(exist_ok=True, parents=True)
    svg_icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>'

    LOCAL_PALETTE = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4", "#f97316", "#14b8a6", "#6366f1", "#a855f7", "#3b82f6", "#22c55e", "#d946ef", "#84cc16"]
    tutti_viaggi_dati = []

    # Estrae la data dalla directory per la visualizzazione nella mappa master
    data_str = target_dir.name.replace("CONSEGNE_", "")

    for i, v in enumerate(viaggi):
        v_id = v.get("nome_giro", f"V{i+1:02d}")
        # IMPORTANTE: Usiamo lista_punti così com'è (è già ottimizzata dal BAT 3)
        perc = v.get("lista_punti", [])
        if not perc: continue
        
        # Statistiche di base (ora coerenti con l'ordine dell'ufficio)
        km = round(sum(haversine(perc[j], perc[j+1]) for j in range(len(perc)-1)) * 1.25, 1) if len(perc)>1 else 0
        t_guida = int(km / 45 * 60)
        t_sosta = len(perc) * 7
        t_tot = t_guida + t_sosta

        color_assegnato = LOCAL_PALETTE[i % len(LOCAL_PALETTE)]

        # Raccogli dati per mappa master complessiva
        tutti_viaggi_dati.append({
            "v_id": v_id,
            "id_zona": v.get("id_zona", v_id),
            "color": color_assegnato,
            "km": km,
            "t_guida": format_time(t_guida),
            "t_sosta": format_time(t_sosta),
            "t_tot": format_time(t_tot),
            "polylines": [], # la versione web parità non ha Directions API, farà fallback su linee rette in JS
            "lista_punti": [{"nome": p.get("nome", "Cliente"), "indirizzo": p.get("indirizzo", "-"), "lat": p.get("lat"), "lon": p.get("lon"), "codice_frutta": p.get("codice_frutta", ""), "codice_latte": p.get("codice_latte", "")} for p in perc]
        })

        zone_list = sorted(list(set([str(p.get('zona', '0000')) for p in perc])))
        z_str = "Zone: " + ", ".join(zone_list[:4])
        fname = f"{v_id}_Zone_{'_'.join(zone_list[:4])}.html"

        # Fallback per navigazione: se mancano lat/lon usa Nome + Indirizzo
        def get_nav_url(d):
            if d.get("lat") and d.get("lon"):
                return f"https://www.google.com/maps/dir/?api=1&destination={d['lat']},{d['lon']}&travelmode=driving"
            # Ricerca testuale: Nome + Indirizzo
            query = f"{d['cliente']} {d['indirizzo']}".replace(" ", "+")
            return f"https://www.google.com/maps/dir/?api=1&destination={query}&travelmode=driving"

        deliveries = [{"cliente": p.get("nome", "Cliente"), "indirizzo": p.get("indirizzo", "-"), "lat": p.get("lat"), "lon": p.get("lon"), "codice_frutta": p.get("codice_frutta", ""), "codice_latte": p.get("codice_latte", "")} for p in perc]
        cards_list = []
        for idx, d in enumerate(deliveries):
            # Formattazione indirizzo su due righe: via/piazza sopra (grassetto), resto sotto
            p_addr = d["indirizzo"].split(',', 1)
            via_parte = p_addr[0].strip()
            resto_parte = p_addr[1].strip() if len(p_addr) > 1 else ""
            addr_html = f'<span class="addr"><b>{via_parte}</b><br>{resto_parte}</span>'
            
            c = f'''<div class="card {'next' if idx == 0 else ''}" onclick="focusOn({idx})">
                <div class="stop-num">{idx+1}</div>
                <div class="stop-info">
                    <div class="actions">
                        <button class="btn-geo" onclick="saveRealCoords({idx}, event)"><span class="material-icons-round">location_searching</span> GEOLOCALIZZA</button>
                        <button class="btn-done" onclick="toggleDone({idx}, event)"><span class="material-icons-round">radio_button_unchecked</span> CONSEGNATO</button>
                    </div>
                    <b class="name">{d["cliente"]}</b>
                    {addr_html}
                </div>
                <a href="{get_nav_url(d)}" class="btn-nav"><span class="material-icons-round">navigation</span></a>
            </div>'''
            cards_list.append(c)
        
        cards_html = "".join(cards_list)

        html = HTML_TEMPLATE.replace("{{ v_id }}", v_id).replace("{{ zone_str }}", z_str).replace("{{ api_key }}", GOOGLE_MAPS_API_KEY).replace("{{ km }}", str(km)).replace("{{ t_guida }}", format_time(t_guida)).replace("{{ t_sosta }}", format_time(t_sosta)).replace("{{ t_tot }}", format_time(t_tot)).replace("{{ cards_html|safe }}", cards_html).replace("{{ deliveries_js|safe }}", json.dumps(deliveries))
        (out_folder / fname).write_text(html, encoding="utf-8")
        (WEBAPP_FOLDER / fname).write_text(html, encoding="utf-8")

    # Genera la mappa complessiva master se ci sono dati
    if tutti_viaggi_dati:
        master_json = json.dumps(tutti_viaggi_dati)
        master_html = MASTER_HTML_TEMPLATE.replace("{{ master_json|safe }}", master_json).replace("{{ api_key }}", GOOGLE_MAPS_API_KEY).replace("{{ data_str }}", data_str)
        
        (out_folder / "00_MAPPA_COMPLESSIVA.html").write_text(master_html, encoding="utf-8")
        (WEBAPP_FOLDER / "00_MAPPA_COMPLESSIVA.html").write_text(master_html, encoding="utf-8")
        
        # Scrive nella cartella locale se presente per parità
        webapp_web = ROOT_DIR.parent / "AppLogSolutionsWeb" / "frontend" / "mappe_autisti"
        if webapp_web.exists():
            webapp_web.mkdir(exist_ok=True, parents=True)
            (webapp_web / "00_MAPPA_COMPLESSIVA.html").write_text(master_html, encoding="utf-8")

    firebase_master_link = "https://log-solution-60007.web.app/mappe_autisti/00_MAPPA_COMPLESSIVA.html"
    txt_content = f" LINK MAPPE PER AUTISTI ({data_str})\n------------------------------------------\n\n"
    txt_content += f"🌍 MAPPA GENERALE COMPLESSIVA:\n{firebase_master_link}\n\n"
    txt_content += "------------------------------------------\n\n"
    
    for i, v in enumerate(viaggi):
        v_id = v.get("nome_giro", f"V{i+1:02d}")
        # IMPORTANTE: Usiamo il nome del file già generato sopra
        zone_list = sorted(list(set([str(p.get('zona', '0000')) for p in v.get("lista_punti", [])])))
        fname = f"{v_id}_Zone_{'_'.join(zone_list[:4])}.html"
        
        # Generiamo link Firebase (più stabili per la web app)
        firebase_link = f"https://log-solution-60007.web.app/mappe_autisti/{fname}"
        
        txt_content += f"🏎️ {v_id} (MAPPA): {firebase_link}\n\n"
        
    (out_folder / "LINK_WHATSAPP_AUTISTI.txt").write_text(txt_content, encoding="utf-8")
    (WEBAPP_FOLDER / "LINK_WHATSAPP_AUTISTI.txt").write_text(txt_content, encoding="utf-8")

    print(f"\nOK Generation completa con OR-Tools.")
    deploy_online()

if __name__ == "__main__": main()

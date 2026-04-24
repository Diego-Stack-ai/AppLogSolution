import json
import math
import sys
import re
import requests
import time
from pathlib import Path

# --- CONFIGURAZIONE LOGISTICA ---
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

# --- CONFIGURAZIONE OTTIMIZZAZIONE ---
# Opzioni: "HAVERSINE" (Locale/Veloce) o "GOOGLE_MATRIX" (API/Preciso)
MODO_DISTANZA = "GOOGLE_MATRIX" 
CACHE_FILE = PROG_DIR / "distanze_reali_cache.json"

DEPOT = {"lat": 45.442805, "lon": 11.714498, "nome": "DEPOSITO VEGGIANO", "indirizzo": "Via Alessandro Volta 25/a, 35030 Veggiano (PD)"}
TIME_OFFSET_PER_STOP = 8
AVG_SPEED_KMH = 35

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

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def haversine(p1, p2):
    try:
        lat1, lon1 = float(p1.get('lat', 0)), float(p1.get('lon', p1.get('lng', 0)))
        lat2, lon2 = float(p2.get('lat', 0)), float(p2.get('lon', p2.get('lng', 0)))
    except: return 999999.0
    R = 6371 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

# --- GESTIONE CACHE DISTANZE REALI ---

class DistanceCache:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return {}
        return {}

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def _get_key(self, p1, p2):
        # Arrotondiamo a 5 decimali per stabilità (~1 metro)
        lat1, lon1 = round(float(p1.get('lat', 0)), 5), round(float(p1.get('lon', p1.get('lng', 0))), 5)
        lat2, lon2 = round(float(p2.get('lat', 0)), 5), round(float(p2.get('lon', p2.get('lng', 0))), 5)
        return f"{lat1},{lon1}_{lat2},{lon2}"

    def get(self, p1, p2):
        return self.data.get(self._get_key(p1, p2))

    def set(self, p1, p2, dist_meters, duration_seconds):
        self.data[self._get_key(p1, p2)] = {"dist": dist_meters, "dur": duration_seconds}

dist_cache = DistanceCache(CACHE_FILE)

# --- LOGICA DI OTTIMIZZAZIONE AVANZATA (OR-TOOLS) ---

def crea_matrice_distanze(punti_con_deposito):
    """Crea la matrice delle distanze (in metri) usando Cache + Google Matrix API con Chunking."""
    n = len(punti_con_deposito)
    matrix = [[0] * n for _ in range(n)]
    
    # 1. Riempimento iniziale dal Cache
    punti_mancanti = False
    for i in range(n):
        for j in range(n):
            if i == j: continue
            cached = dist_cache.get(punti_con_deposito[i], punti_con_deposito[j])
            if cached:
                matrix[i][j] = cached['dist']
            else:
                punti_mancanti = True

    if not punti_mancanti:
        return matrix

    if MODO_DISTANZA == "HAVERSINE":
        return crea_matrice_distanze_haversine_internal(punti_con_deposito)

    # 2. Richiesta a Google Matrix con CHUNKING (per superare il limite di 25 origini e 100 elementi totali)
    # NOTA: Google permette max 100 elementi per richiesta (es: 10 origini x 10 destinazioni)
    CHUNK_SIZE = 10
    print(f"  API Google Matrix: Elaborazione distanze reali per {n} punti...")
    
    try:
        modificato = False
        for r_start in range(0, n, CHUNK_SIZE):
            r_end = min(r_start + CHUNK_SIZE, n)
            origins = "|".join([f"{p['lat']},{p['lon']}" for p in punti_con_deposito[r_start:r_end]])
            
            for c_start in range(0, n, CHUNK_SIZE):
                c_end = min(c_start + CHUNK_SIZE, n)
                # Ottimizzazione: se tutte le distanze in questo blocco sono già nel cache, saltiamo la chiamata
                blocco_mancante = False
                for i in range(r_start, r_end):
                    for j in range(c_start, c_end):
                        if i != j and matrix[i][j] == 0:
                            blocco_mancante = True; break
                    if blocco_mancante: break
                
                if not blocco_mancante: continue

                destinations = "|".join([f"{p['lat']},{p['lon']}" for p in punti_con_deposito[c_start:c_end]])
                url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={GOOGLE_MAPS_API_KEY}"
                
                resp = requests.get(url, timeout=10).json()
                if resp['status'] == 'OK':
                    for i_local, row in enumerate(resp['rows']):
                        i_global = r_start + i_local
                        for j_local, element in enumerate(row['elements']):
                            j_global = c_start + j_local
                            if i_global == j_global: continue
                            
                            if element['status'] == 'OK':
                                dist = element['distance']['value']
                                dur = element['duration']['value']
                                matrix[i_global][j_global] = dist
                                dist_cache.set(punti_con_deposito[i_global], punti_con_deposito[j_global], dist, dur)
                                modificato = True
                elif resp['status'] == 'REQUEST_DENIED':
                    print("  ERR API Google Matrix: Accesso Negato (REQUEST_DENIED).")
                    print("      -> DEVI ABILITARE 'Distance Matrix API' nella Google Cloud Console.")
                    return crea_matrice_distanze_haversine_internal(punti_con_deposito)
                else:
                    print(f"  WARN Google Matrix status: {resp['status']}. Uso Haversine per questo blocco.")
                    # Fallback locale per il blocco specifico
                    for i in range(r_start, r_end):
                        for j in range(c_start, c_end):
                            if i != j and matrix[i][j] == 0:
                                matrix[i][j] = int(haversine(punti_con_deposito[i], punti_con_deposito[j]) * 1000)

        if modificato:
            dist_cache.save()
            
    except Exception as e:
        print(f"  WARN Errore durante il chunking Matrix: {e}. Uso Haversine di emergenza.")
        return crea_matrice_distanze_haversine_internal(punti_con_deposito)

    return matrix

def crea_matrice_distanze_haversine_internal(punti_con_deposito):
    n = len(punti_con_deposito)
    return [[int(haversine(punti_con_deposito[i], punti_con_deposito[j]) * 1000) for j in range(n)] for i in range(n)]

def ottimizza_percorso(punti_consegna):
    """Sceglie automaticamente tra OR-Tools (TSP) o Nearest Neighbor."""
    if not punti_consegna: return []
    
    if not HAS_OR_TOOLS:
        return ottimizza_percorso_legacy(punti_consegna)

    all_locations = [DEPOT] + punti_consegna
    distance_matrix = crea_matrice_distanze(all_locations)
    
    manager = pywrapcp.RoutingIndexManager(len(all_locations), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
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
    
    return ottimizza_percorso_legacy(punti_consegna)

def ottimizza_percorso_legacy(punti):
    """Algoritmo Nearest Neighbor originale."""
    non_visitati, percorso, corrente = punti[:], [], DEPOT
    while non_visitati:
        idx, pross = min(enumerate(non_visitati), key=lambda x: (haversine(corrente, x[1]), x[0]))
        percorso.append(pross)
        non_visitati.pop(idx)
        corrente = pross
    return percorso

# --- FINE LOGICA DI OTTIMIZZAZIONE ---

def get_google_trip_data(percorso):
    """Calcola KM e scarica le strade reali via Google Directions API."""
    punti_pieni = [DEPOT] + percorso + [DEPOT]
    km_tot, sec_tot = 0, 0
    polylines = []
    
    km_stima, sec_stima = 0, 0
    for k in range(len(punti_pieni)-1):
        d = haversine(punti_pieni[k], punti_pieni[k+1]) * 1.3
        km_stima += d
        sec_stima += (d / AVG_SPEED_KMH) * 3600

    try:
        chunk_size = 20 
        for i in range(0, len(punti_pieni)-1, chunk_size):
            sub = punti_pieni[i:i+chunk_size+1]
            origin, dest = f"{sub[0]['lat']},{sub[0]['lon']}", f"{sub[-1]['lat']},{sub[-1]['lon']}"
            waypts = "|".join([f"{p['lat']},{p['lon']}" for p in sub[1:-1]])
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={dest}&waypoints={waypts}&key={GOOGLE_MAPS_API_KEY}"
            r = requests.get(url, timeout=5).json()
            if r.get('status') == 'OK':
                km_tot += sum(l['distance']['value'] for l in r['routes'][0]['legs']) / 1000.0
                sec_tot += sum(l['duration']['value'] for l in r['routes'][0]['legs'])
                polylines.append(r['routes'][0]['overview_polyline']['points'])
    except: pass
            
    final_km = round(km_tot if km_tot > 0 else km_stima, 1)
    final_guida_sec = sec_tot if sec_tot > 0 else sec_stima
    t_guida_min = int(final_guida_sec / 60)
    t_sosta_min = len(percorso) * TIME_OFFSET_PER_STOP
    return final_km, t_guida_min, t_sosta_min, (t_guida_min + t_sosta_min), polylines

def fmt_min(m):
    return f"{m//60}h {m%60}m" if m >= 60 else f"{m}min"

def genera_html_giro(v_id, zone_str, percorso, stats, polylines, output_path):
    km, t_guida, t_sosta, t_tot = stats
    tutti_punti = [DEPOT] + percorso + [DEPOT]
    punti_js = json.dumps(tutti_punti, indent=2, ensure_ascii=False)
    poly_js = json.dumps(polylines)
    titolo_v = f"{v_id} - Zone: {zone_str}"

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titolo_v}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&libraries=geometry&v=weekly" defer></script>
    <style>
        :root {{ --p: #4f46e5; --sidebar-w: 400px; }}
        * {{ box-sizing: border-box; }}
        body, html {{ margin: 0; padding: 0; height: 100%; font-family: 'Inter', sans-serif; overflow: hidden; }}
        .main-container {{ display: flex; height: 100vh; }}
        #sidebar {{ width: var(--sidebar-w); height: 100%; background: white; display: flex; flex-direction: column; z-index: 100; box-shadow: 10px 0 30px rgba(0,0,0,0.1); }}
        .header {{ padding: 24px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; }}
        .stats-grid {{ display: grid; grid-template-columns: 1fr 1fr; padding: 15px; gap: 8px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }}
        .stat-card {{ background: white; padding: 10px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; }}
        .stat-val {{ display: block; font-weight: 800; font-size: 1rem; color: var(--p); }}
        .stat-lbl {{ font-size: 0.65rem; color: #64748b; text-transform: uppercase; font-weight: 700; }}
        .tot-card {{ grid-column: span 2; background: #f5f3ff; border-color: #c7d2fe; }}
        #stop-list {{ flex: 1; overflow-y: auto; padding: 15px; background: #f1f5f9; }}
        .stop-card {{ background: white; border-radius: 14px; padding: 16px; margin-bottom: 12px; display: flex; gap: 14px; align-items: center; border: 1.5px solid #e2e8f0; cursor: pointer; transition: 0.2s; }}
        .stop-card:hover {{ border-color: var(--p); transform: translateX(5px); }}
        .stop-num {{ width: 30px; height: 30px; background: var(--p); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 12px; flex-shrink: 0; }}
        .nav-btn {{ background: #22c55e; color: white; width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; text-decoration: none; }}
        #map {{ flex: 1; height: 100%; }}
        .depot-tag {{ background: #475569; color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 800; }}
        @media (max-width: 800px) {{ .main-container {{ flex-direction: column; }} #sidebar {{ width: 100%; height: 50%; }} #map {{ height: 50%; }} }}
    </style>
</head>
<body>
    <div class="main-container">
        <div id="sidebar">
            <div class="header">
                <div style="font-size:0.75rem; opacity:0.8; font-weight:800; text-transform:uppercase; margin-bottom:4px;">Logistica Operativa</div>
                <h1 style="margin:0; font-size:1.5rem; letter-spacing:-0.01em;">{v_id}</h1>
                <div style="margin-top:6px; font-size:0.85rem; font-weight:600; color: #a5b4fc;">Zone: {zone_str}</div>
            </div>
            <div class="stats-grid">
                <div class="stat-card"><span class="stat-val">{len(percorso)}</span><span class="stat-lbl">Tappe</span></div>
                <div class="stat-card"><span class="stat-val">{km} km</span><span class="stat-lbl">Distanza</span></div>
                <div class="stat-card"><span class="stat-val">{fmt_min(t_guida)}</span><span class="stat-lbl">Guida</span></div>
                <div class="stat-card"><span class="stat-val">{fmt_min(t_sosta)}</span><span class="stat-lbl">Scarico</span></div>
                <div class="stat-card tot-card"><span class="stat-val" style="font-size:1.3rem;">{fmt_min(t_tot)}</span><span class="stat-lbl">TEMPO TOTALE STIMATO</span></div>
            </div>
            <div id="stop-list">
                <div class="stop-card" style="background:#f8fafc;"><div style="color:#475569;"><span class="material-icons-round">home</span></div>
                    <div class="stop-info"><span class="depot-tag">PARTENZA</span><br><b style="font-size:0.9rem;">Deposito Veggiano</b></div>
                </div>
                { "".join([f'''<div class="stop-card" onclick="panTo({i+1})"><div class="stop-num">{i+1}</div><div style="flex:1;"><b style="font-size:0.85rem; color:#1e293b;">{p['nome']}</b><br><small style="color:#64748b; font-size:0.75rem;">{p['indirizzo']}</small></div><a href="https://www.google.com/maps/dir/?api=1&destination={p['lat']},{p['lon']}&travelmode=driving" class="nav-btn" onclick="event.stopPropagation()"><span class="material-icons-round">navigation</span></a></div>''' for i, p in enumerate(percorso)]) }
                <div class="stop-card" style="background:#f8fafc;"><div style="color:#475569;"><span class="material-icons-round">flag</span></div>
                    <div class="stop-info"><span class="depot-tag">ARRIVO</span><br><b style="font-size:0.9rem;">Deposito Veggiano</b></div>
                </div>
            </div>
        </div>
        <div id="map"></div>
    </div>
    <script>
        const data = {punti_js}; const polys = {poly_js}; let map, markers = [];
        async function initMap() {{
            const {{ Map }} = await google.maps.importLibrary("maps");
            const {{ AdvancedMarkerElement }} = await google.maps.importLibrary("marker");
            
            // Trova primo punto per centrare
            const centerP = data.find(p => p.lat && p.lon) || {{lat: 45.4428, lon: 11.7145}};
            map = new Map(document.getElementById("map"), {{ zoom: 12, center: {{ lat: centerP.lat, lng: centerP.lon }}, mapId: 'DEMO_MAP_ID' }});
            
            const geocoder = new google.maps.Geocoder();
            const bounds = new google.maps.LatLngBounds();

            data.forEach((p, i) => {{
                const isD = (i === 0 || i === data.length - 1);
                if (p.lat && p.lon) {{
                    addAdvMarker(p, i, isD, bounds, AdvancedMarkerElement);
                }} else {{
                    // Geocoding di backup
                    const query = `${{p.nome}}, ${{p.indirizzo}}`;
                    geocoder.geocode({{ address: query }}, (results, status) => {{
                        if (status === "OK") {{
                            const loc = results[0].geometry.location;
                            p.lat = loc.lat(); p.lon = loc.lng();
                            addAdvMarker(p, i, isD, bounds, AdvancedMarkerElement);
                        }} else {{
                            geocoder.geocode({{ address: p.indirizzo }}, (res2, st2) => {{
                                if (st2 === "OK") {{
                                    const loc2 = res2[0].geometry.location;
                                    p.lat = loc2.lat(); p.lon = loc2.lng();
                                    addAdvMarker(p, i, isD, bounds, AdvancedMarkerElement);
                                }}
                            }});
                        }}
                    }});
                }}
            }});

            if (polys.length > 0) {{
                polys.forEach(pString => {{
                    const p = google.maps.geometry.encoding.decodePath(pString);
                    new google.maps.Polyline({{ path: p, strokeColor: "#4f46e5", strokeOpacity: 0.8, strokeWeight: 6, map }});
                }});
            }} else {{
                new google.maps.Polyline({{ 
                    path: data.filter(p => p.lat).map(p => ({{ lat: p.lat, lng: p.lon }})), 
                    strokeColor: "#4f46e5", strokeOpacity: 0.6, strokeWeight: 4, map 
                }});
            }}
        }}

        function addAdvMarker(p, i, isD, bounds, AdvancedMarkerElement) {{
            const m = new AdvancedMarkerElement({{
                map,
                position: {{ lat: p.lat, lng: p.lon }},
                content: createPin(i, isD),
                title: p.nome
            }});
            markers[i] = m;
            bounds.extend(m.position);
            map.fitBounds(bounds);
        }}

        function createPin(idx, isD) {{
            const d = document.createElement("div"); d.style.background = isD ? "#475569" : "#4f46e5";
            d.style.color = "white"; d.style.width = "26px"; d.style.height = "26px"; d.style.borderRadius = "50%"; 
            d.style.display = "flex"; d.style.alignItems = "center"; d.style.justifyContent = "center";
            d.style.fontSize = "11px"; d.style.fontWeight = "900"; d.style.border = "3px solid white";
            d.innerText = isD ? "" : idx; if(isD) d.innerHTML = '<span class="material-icons-round" style="font-size:14px">home</span>';
            return d;
        }}

        function panTo(i) {{ if(markers[i]) {{ map.panTo(markers[i].position); map.setZoom(17); }} }}
        window.addEventListener('load', initMap);
    </script>
</body></html>"""
    output_path.write_text(html, encoding="utf-8")

def gera_riepilogo(summary_data, output_path):
    km_tot = round(sum(z['km'] for z in summary_data), 1)
    min_tot = sum(z['t_tot'] for z in summary_data)
    cards_html = "".join([f'''
        <div style="background:white; border-radius:24px; padding:30px; border:1.5px solid #e2e8f0; position:relative; overflow:hidden; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
            <div style="position:absolute; top:0; left:0; width:12px; height:100%; background:#4f46e5;"></div>
            <div style="font-size:0.8rem; font-weight:800; color:#64748b; text-transform:uppercase; margin-bottom:8px;">{z['v_id']}</div>
            <b style="font-size:1.15rem; color:#0f172a; display:block;">Zone: {z['zone_str']}</b>
            <div style="font-size:0.85rem; font-weight:700; color:#10b981; margin-top:5px;">💰 Fatturato: € {z['fatturato']} ({z['tot_ddt']} DDT)</div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin:20px 0; font-size:0.85rem; color:#475569; border-top:1px solid #f1f5f9; padding-top:15px;">
                <span>🛣️ <b>{z['km']} km</b></span><span>🕒 Guida: {fmt_min(z['t_guida'])}</span>
                <span> {z['punti']} tappe</span><span style="font-weight:900; color:#4f46e5;">🏁 TOT: {fmt_min(z['t_tot'])}</span>
            </div>
            <a href="{z['fname']}" style="display:block; background:#4f46e5; color:white; text-align:center; padding:15px; border-radius:14px; text-decoration:none; font-weight:800; font-size:0.85rem;">APRI MAPPA</a>
        </div>
    ''' for z in summary_data])

    VALORE_DDT = 18.50
    tot_ddt_generale = sum(z['tot_ddt'] for z in summary_data)
    fatturato_generale = f"{sum(float(z['fatturato']) for z in summary_data):.2f}"

    html = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8"><title>Dashboard Logistica</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&display=swap" rel="stylesheet">
<style>
    body {{ font-family: 'Inter', sans-serif; background: #f8fafc; padding: 60px 20px; color: #1e293b; }}
    .main-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 24px; margin: 40px 0; }}
    .sum-card {{ background: white; padding: 35px; border-radius: 24px; text-align: center; border: 1px solid #e2e8f0; }}
    .g-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 30px; }}
</style></head>
<body>
    <div style="max-width:1400px; margin:0 auto;">
        <h1 style="font-weight:900; font-size:2.8rem; margin:0;">Dashboard Logistica</h1>
        <p style="color:#64748b; font-size:1.1rem; margin-top:10px;">Pianificazione flotta basata su Veggiano (PD)</p>
        <div class="main-grid">
            <div class="sum-card"><b style="font-size:2.2rem; color:#4f46e5;">{len(summary_data)}</b><br><small>GIRI</small></div>
            <div class="sum-card"><b style="font-size:2.2rem; color:#4f46e5;">{km_tot} km</b><br><small>KM TOTALI</small></div>
            <div class="sum-card"><b style="font-size:2.2rem; color:#10b981;">€ {fatturato_generale}</b><br><small>FATTURATO ({tot_ddt_generale} DDT)</small></div>
            <div class="sum-card"><b style="font-size:2.2rem; color:#10b981;">{fmt_min(sum(z['t_sosta'] for z in summary_data))}</b><br><small>SCARICO</small></div>
            <div class="sum-card" style="background:#eef2ff;"><b style="font-size:2.2rem; color:#4f46e5;">{fmt_min(min_tot)}</b><br><small>TEMPO TOTALE</small></div>
        </div>
        <div class="g-grid">{cards_html}</div>
    </div>
</body></html>"""
    output_path.write_text(html, encoding="utf-8")

def main():
    target_dir = get_latest_consegne_dir()
    if not target_dir: return print("ERR Nessuna cartella.")
    json_f = target_dir / "viaggi_giornalieri.json"
    if not json_f.exists(): return print(f"ERR Salva la mappa!")
    with open(json_f, "r", encoding="utf-8") as f: data_zone = json.load(f)
    data_zone = [z for z in data_zone if z.get("id_zona", "") != "DDT_DA_INSERIRE"]
    out_dir = target_dir / "PERCORSI_VEGGIANO"
    out_dir.mkdir(exist_ok=True)
    summary = []
    
    data_zone_sorted = sorted(data_zone, key=lambda x: x.get('id_zona', ''))
    
    print(f"\n--- GENERAZIONE PERCORSI CON OR-TOOLS ({MODO_DISTANZA}) ---")

    for i, z in enumerate(data_zone_sorted, 1):
        punti = z.get("lista_punti", [])
        if not punti: continue
        v_id = f"V{i:02d}"
        zone_coinvolte = sorted(list(set([str(p.get('zona','0000')) for p in punti])))
        z_str = ", ".join(zone_coinvolte).replace('None', '0000')
        
        perc = ottimizza_percorso(punti)
        km, t_guida, t_sosta, t_tot, polylines = get_google_trip_data(perc)
        
        
        # Calcolo Fatturato DDT (16.50 Euro ciascuno)
        tot_ddt = 0
        for p in punti:
            tot_ddt += len([c for c in p.get("codici_ddt_frutta", []) if c and c != "p00000"])
            tot_ddt += len([c for c in p.get("codici_ddt_latte", []) if c and c != "p00000"])
            # Fallback per punti caricati senza liste esplicite
            if not p.get("codici_ddt_frutta") and not p.get("codici_ddt_latte"):
                if p.get("codice_frutta") and p.get("codice_frutta") != "p00000": tot_ddt += 1
                if p.get("codice_latte") and p.get("codice_latte") != "p00000": tot_ddt += 1
        
        fatturato = f"{tot_ddt * 16.50:.2f}"
        
        fname = sanitize_filename(f"{v_id}_Zone_{'_'.join(zone_coinvolte[:3])}.html")
        info = {'v_id': v_id, 'zone_str': z_str, 'fname': fname, 'km': km, 't_guida': t_guida, 't_sosta': t_sosta, 't_tot': t_tot, 'punti': len(punti), 'tot_ddt': tot_ddt, 'fatturato': fatturato}
        summary.append(info)
        
        genera_html_giro(v_id, z_str, perc, (km, t_guida, t_sosta, t_tot), polylines, out_dir / fname)
        print(f"  OK {v_id} (Zone: {z_str:<12}) -> {km:>5} km | {fmt_min(t_tot)}")

    riepilogo_fname = sanitize_filename("RIEPILOGO_GIRI.html")
    gera_riepilogo(summary, out_dir / riepilogo_fname)
    print(f"\n COMPLETATO! Linee visibili con OR-Tools.")

if __name__ == "__main__": 
    if not HAS_OR_TOOLS:
        print("\nℹ️  Per risultati migliori, installa OR-Tools: pip install ortools\n")
    main()

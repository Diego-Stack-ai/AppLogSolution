import json
import sys
import threading
import webbrowser
import time
from pathlib import Path

try:
    from flask import Flask, render_template_string, request, jsonify
    from flask_cors import CORS
except ImportError:
    print("ERRORE: Flask o flask-cors non installati. Esegui: pip install flask flask-cors")
    sys.exit(1)

# Importiamo la logica del file 6 per poter usare OR-Tools e ricalcolare gli HTML
PROG_DIR = Path(__file__).resolve().parent
sys.path.append(str(PROG_DIR))

try:
    import importlib
    gen_percorsi = importlib.import_module("6_genera_percorsi_veggiano")
    HAS_GEN_PERCORSI = True
except Exception as e:
    print(f"WARN: Impossibile importare 6_genera_percorsi_veggiano.py ({e}). L'ottimizzazione e rigenerazione HTML non funzioneranno al 100%.")
    HAS_GEN_PERCORSI = False

BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

app = Flask(__name__)
CORS(app)

DATA_GIORNO = ""
FILE_JSON_OTTIMIZZATO = None

def _trova_ultima_cartella():
    folders = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
    if not folders: return None
    return max(folders, key=lambda d: d.stat().st_mtime)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

@app.route('/')
def index():
    if not FILE_JSON_OTTIMIZZATO or not FILE_JSON_OTTIMIZZATO.exists():
        return "File viaggi_giornalieri_OTTIMIZZATO.json non trovato."
    
    dati = json.loads(FILE_JSON_OTTIMIZZATO.read_text(encoding="utf-8"))
    if HAS_GEN_PERCORSI:
        for v in dati:
            v["depot"] = gen_percorsi.get_depot_for_points(v.get("lista_punti", []))
            
    return render_template_string(HTML_TEMPLATE, 
                                  DATA_GIORNO=DATA_GIORNO, 
                                  JSON_VIAGGI=json.dumps(dati, ensure_ascii=False),
                                  API_KEY=GOOGLE_MAPS_API_KEY)

@app.route('/save', methods=['POST'])
def save():
    try:
        req = request.json
        viaggio_id = req.get('viaggio_id')
        lista_punti = req.get('lista_punti', [])
        usa_ortools = req.get('usa_ortools', False)
        num_locked = int(req.get('num_locked', 0))

        if not FILE_JSON_OTTIMIZZATO.exists():
            return jsonify({"status": "error", "msg": "File non trovato"})

        dati = json.loads(FILE_JSON_OTTIMIZZATO.read_text(encoding="utf-8"))
        
        target_viaggio = None
        for v in dati:
            if v.get("nome_giro") == viaggio_id:
                target_viaggio = v
                break
                
        if not target_viaggio:
            return jsonify({"status": "error", "msg": "Viaggio non trovato"})

        # OTTIMIZZAZIONE IBRIDA
        if usa_ortools and HAS_GEN_PERCORSI:
            locked_points = lista_punti[:num_locked]
            remaining_points = lista_punti[num_locked:]
            
            if remaining_points:
                from ortools.constraint_solver import pywrapcp, routing_enums_pb2
                depot = gen_percorsi.get_depot_for_points(lista_punti)
                start_point = locked_points[-1] if locked_points else depot
                all_locations = [start_point] + remaining_points + [depot]
                num_nodes = len(all_locations)
                
                manager = pywrapcp.RoutingIndexManager(num_nodes, 1, [0], [num_nodes - 1])
                routing = pywrapcp.RoutingModel(manager)
                dist_matrix = gen_percorsi.crea_matrice_distanze(all_locations)
                
                def distance_callback(from_index, to_index):
                    return dist_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]
                    
                transit_callback_index = routing.RegisterTransitCallback(distance_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                # Aggiungi vincoli di orario (Time Windows) solo per Grand Chef
                is_grand_chef = viaggio_id.upper().startswith("GRANCHEF") or any("GRAND" in str(p.get("tipologia_grado") or "").upper() or "CHEF" in str(p.get("tipologia_grado") or "").upper() or "GRANCHEF" in str(p.get("zona") or "").upper() for p in remaining_points)
                
                if is_grand_chef:
                    def time_callback(from_index, to_index):
                        from_node = manager.IndexToNode(from_index)
                        to_node = manager.IndexToNode(to_index)
                        dist = dist_matrix[from_node][to_node]
                        travel_time = (dist / 1000.0 / gen_percorsi.AVG_SPEED_KMH) * 60
                        # Sosta solo se il nodo di partenza non è lo start_point (nodo 0) e non è l'arrivo (depot)
                        offset = 12 if is_grand_chef else gen_percorsi.TIME_OFFSET_PER_STOP
                        service_time = offset if from_node not in (0, num_nodes - 1) else 0
                        return int(travel_time + service_time)

                    time_callback_index = routing.RegisterTransitCallback(time_callback)
                    routing.AddDimension(
                        time_callback_index,
                        30,  # slack consentito
                        1440,
                        False,
                        "Time"
                    )
                    time_dimension = routing.GetDimensionOrDie("Time")

                    def parse_time_to_minutes(time_str, default_val):
                        if not time_str: return default_val
                        import re
                        m = re.match(r"(\d{2}):(\d{2})", str(time_str).strip())
                        if m:
                            return int(m.group(1)) * 60 + int(m.group(2))
                        return default_val

                    # Applica vincoli sui remaining_points (nodi da 1 a num_nodes - 2)
                    for i, p in enumerate(remaining_points, start=1):
                        min_min = parse_time_to_minutes(p.get("orario_min"), 420)
                        max_min = parse_time_to_minutes(p.get("orario_max"), 840)
                        node_index = manager.NodeToIndex(i)
                        time_dimension.CumulVar(node_index).SetRange(min_min, max_min)
                
                search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
                search_parameters.time_limit.seconds = 3
                
                solution = routing.SolveWithParameters(search_parameters)

                # Fallback se non trova soluzioni con orari rigidi
                if not solution and is_grand_chef:
                    manager = pywrapcp.RoutingIndexManager(num_nodes, 1, [0], [num_nodes - 1])
                    routing = pywrapcp.RoutingModel(manager)
                    def distance_callback_fallback(from_index, to_index):
                        return dist_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]
                    transit_callback_index_fallback = routing.RegisterTransitCallback(distance_callback_fallback)
                    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index_fallback)
                    solution = routing.SolveWithParameters(search_parameters)
                
                opt_rem = []
                if solution:
                    index = routing.Start(0)
                    index = solution.Value(routing.NextVar(index)) # Salta il nodo iniziale
                    while not routing.IsEnd(index):
                        node_index = manager.IndexToNode(index)
                        opt_rem.append(all_locations[node_index])
                        index = solution.Value(routing.NextVar(index))
                    lista_punti = locked_points + opt_rem
                else:
                    lista_punti = locked_points + remaining_points
        
        # Salvataggio nel JSON Unico
        target_viaggio["lista_punti"] = lista_punti
        FILE_JSON_OTTIMIZZATO.write_text(json.dumps(dati, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # Ricalcolo Mappa HTML (per avere il PDF corretto)
        if HAS_GEN_PERCORSI:
            percorsi_dir = FILE_JSON_OTTIMIZZATO.parent / "PERCORSI_VEGGIANO"
            percorsi_dir.mkdir(exist_ok=True)
            
            # Sovrascriviamo lo STESSO file originale per non creare duplicati
            file_html_name = target_viaggio.get("file_sorgente")
            if not file_html_name:
                zone_str_file = "_".join(target_viaggio.get("zone", ["0000"])[:3])
                file_html_name = f"{viaggio_id}_Zone_{zone_str_file}.html"
            
            output_html_path = percorsi_dir / file_html_name
            zone_str_titolo = ", ".join(target_viaggio.get("zone", ["0000"]))
            
            # Calcola KM veri via API Google Directions (stessa logica del file 6)
            depot = gen_percorsi.get_depot_for_points(lista_punti)
            full_stats = gen_percorsi.get_google_trip_data(lista_punti, depot)
            final_km, t_guida_min, t_sosta_min, t_tot, polylines = full_stats
            stats_4 = (final_km, t_guida_min, t_sosta_min, t_tot)
            
            gen_percorsi.genera_html_giro(viaggio_id, zone_str_titolo, lista_punti, stats_4, polylines, output_html_path, depot)

        return jsonify({"status": "ok", "msg": "Salvataggio e Ottimizzazione completati!"})

    except Exception as e:
        import traceback
        err_str = traceback.format_exc()
        with open("error_log.txt", "w") as f:
            f.write(err_str)
        return jsonify({"status": "error", "msg": f"{str(e)}\n{err_str}"}), 500


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>Editor Percorsi</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
    <script>
        (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. See https://goo.gle/js-api-loading-troubleshooting"):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
            key: "{{API_KEY}}",
            v: "beta"
        });
    </script>
    <style>
        :root { --primary: #4f46e5; --bg: #f8fafc; }
        body { margin: 0; font-family: 'Inter', sans-serif; display: flex; height: 100vh; background: var(--bg); }
        #sidebar { width: 450px; background: white; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; z-index: 10; box-shadow: 2px 0 10px rgba(0,0,0,0.05); }
        .header { padding: 20px; background: #1e293b; color: white; }
        select { width: 100%; padding: 10px; margin-top: 10px; border-radius: 6px; border: 1px solid #ccc; font-weight: bold; }
        .controls { padding: 15px; border-bottom: 1px solid #e2e8f0; background: #f1f5f9; }
        .btn { padding: 10px; font-weight: bold; cursor: pointer; border: none; border-radius: 6px; color: white; width: 100%; margin-top: 8px; }
        .btn-save { background: #10b981; }
        .btn-opt { background: #f59e0b; }
        #list-container { flex: 1; overflow-y: auto; padding: 10px; }
        .point-card { background: white; border: 1px solid #e2e8f0; margin-bottom: 8px; padding: 10px; border-radius: 8px; display: flex; align-items: center; gap: 10px; cursor: grab; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: all 0.2s ease; }
        .point-card:active { cursor: grabbing; }
        .point-card.late { border-left: 5px solid #ef4444; background: #fef2f2; }
        .num-badge { width: 24px; height: 24px; background: var(--primary); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: bold; flex-shrink: 0; }
        #map { flex: 1; }
        .custom-marker { background: var(--primary); color: white; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
        .custom-marker.late { background: #ef4444; }
        #status { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); background: #10b981; color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; display: none; z-index: 9999; }
    </style>
</head>
<body>
    <div id="sidebar">
        <div class="header">
            <h2 style="margin:0; font-size:1.2rem;">Editor Percorsi [v1.1]</h2>
            <select id="viaggio-select" onchange="loadViaggio()"></select>
        </div>
        <div class="controls">
            <div style="font-size:0.8rem; font-weight:600; margin-bottom:5px;">Configurazione Salvataggio</div>
            <label style="font-size:0.85rem; display:flex; align-items:center; gap:8px;">
                Punti bloccati in testa (non ottimizzati):
                <input type="number" id="num-locked" value="0" min="0" style="width:60px; padding:4px; border:1px solid #ccc; border-radius:4px; font-weight:bold;">
            </label>
            <button class="btn btn-save" onclick="salva(false)">💾 SALVA ORDINE ESATTO</button>
            <button class="btn btn-opt" onclick="salva(true)">⚡ SALVA E OTTIMIZZA IL RESTO (OR-TOOLS)</button>
            <div id="gc-info-box" style="margin-top:12px; padding:10px; border-radius:6px; font-size:0.82rem; border: 1px solid #cbd5e1; background: #f8fafc; display:none; line-height:1.4;"></div>
        </div>
        <div id="list-container"></div>
    </div>
    <div id="map"></div>
    <div id="status">Aggiornamento completato!</div>

    <script>
        const DATA = {{JSON_VIAGGI | safe}};
        let map, markers = [], polyline;
        let activeViaggio = null;

        function calcolaETA(viaggio) {
            try {
                const isGC = viaggio.nome_giro.toUpperCase().includes('GRANCHEF') || viaggio.lista_punti.some(p => (p.tipologia_grado || '').toUpperCase().includes('GRAND') || (p.tipologia_grado || '').toUpperCase().includes('CHEF') || (p.zona || '').toUpperCase().includes('GRANCHEF'));
                const sosta = isGC ? 12 : 8;
                const speed = 35; // km/h
                
                const depotLat = viaggio.depot ? viaggio.depot.lat : 45.442805;
                const depotLon = viaggio.depot ? viaggio.depot.lon : 11.714498;
                const depot = { lat: depotLat, lon: depotLon };
                
                let currentTime = 420; // 07:00
                
                function getDistKm(lat1, lon1, lat2, lon2) {
                    const R = 6371; // km
                    const dLat = (lat2 - lat1) * Math.PI / 180;
                    const dLon = (lon2 - lon1) * Math.PI / 180;
                    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                              Math.sin(dLon/2) * Math.sin(dLon/2);
                    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                    return R * c;
                }
                
                function parseTimeToMinutes(timeStr, defaultVal) {
                    if (!timeStr) return defaultVal;
                    const parts = String(timeStr).trim().split(':');
                    if (parts.length >= 2) {
                        return parseInt(parts[0]) * 60 + parseInt(parts[1]);
                    }
                    return defaultVal;
                }
                
                function formatMinutesToTime(minutes) {
                    const m = Math.floor(minutes) % 1440;
                    const hh = String(Math.floor(m / 60)).padStart(2, '0');
                    const mm = String(m % 60).padStart(2, '0');
                    return `${hh}:${mm}`;
                }
                
                let oraPartenzaMagazzino = "07:00";
                
                for (let i = 0; i < viaggio.lista_punti.length; i++) {
                    const p = viaggio.lista_punti[i];
                    const prev = i === 0 ? depot : { lat: viaggio.lista_punti[i-1].lat, lon: viaggio.lista_punti[i-1].lon };
                    
                    const distKm = getDistKm(prev.lat, prev.lon, p.lat, p.lon) * 1.3;
                    const durataGuidaMin = (distKm / speed) * 60;
                    
                    let arrivalTime;
                    if (isGC && i === 0) {
                        arrivalTime = 420; // 07:00
                        const partenzaMin = 420 - durataGuidaMin;
                        oraPartenzaMagazzino = formatMinutesToTime(partenzaMin);
                    } else {
                        arrivalTime = currentTime + durataGuidaMin;
                    }
                    
                    const departureTime = arrivalTime + sosta;
                    p.eta_arrivo = arrivalTime;
                    p.ora_arrivo = formatMinutesToTime(arrivalTime);
                    p.ora_ripartenza = formatMinutesToTime(departureTime);
                    
                    const maxTimeMin = parseTimeToMinutes(p.orario_max, 840);
                    p.isLate = arrivalTime > (maxTimeMin + 1);
                    
                    currentTime = departureTime;
                }
                
                viaggio.isGC = isGC;
                viaggio.sosta = sosta;
                viaggio.oraPartenzaMagazzino = oraPartenzaMagazzino;
            } catch (err) {
                console.error("Errore calcolo ETA: ", err);
            }
        }

        async function initMap() {
            try {
                const { Map } = await google.maps.importLibrary("maps");
                map = new Map(document.getElementById("map"), { center: {lat: 45.44, lng: 11.71}, zoom: 10, mapId: "EDITOR_MAP" });
                
                const sel = document.getElementById("viaggio-select");
                DATA.forEach(v => {
                    let opt = document.createElement("option");
                    opt.value = v.nome_giro;
                    opt.textContent = `${v.nome_giro} (${v.lista_punti.length} fermate)`;
                    sel.appendChild(opt);
                });
                loadViaggio();

                Sortable.create(document.getElementById('list-container'), {
                    animation: 150,
                    handle: '.drag-handle',
                    forceFallback: true,
                    onEnd: () => {
                        aggiornaNumeri();
                        drawMappa();
                    }
                });
            } catch (err) {
                alert("Errore caricamento Google Maps: " + err.message);
                console.error(err);
            }
        }

        function loadViaggio() {
            try {
                const vid = document.getElementById("viaggio-select").value;
                activeViaggio = DATA.find(v => v.nome_giro === vid);
                
                calcolaETA(activeViaggio);
                
                const infoBox = document.getElementById("gc-info-box");
                if (activeViaggio.isGC) {
                    infoBox.style.display = "block";
                    infoBox.innerHTML = `
                        <div style="font-weight:bold; color:#1e293b; margin-bottom:4px;">🚚 Regole Tratta: GRAND CHEF</div>
                        <div style="color:#475569;">📍 Magazzino: <span style="font-weight:600; color:#4f46e5;">Veggiano (PD)</span></div>
                        <div style="color:#475569;">⏰ Ora Partenza: <span style="font-weight:600; color:#10b981;">${activeViaggio.oraPartenzaMagazzino}</span></div>
                        <div style="color:#475569;">⏳ Sosta per fermata: <b>12 min</b></div>
                        <div style="color:#475569;">🎯 Vincolo: Primo Stop fisso alle <b>07:00</b></div>
                    `;
                    document.getElementById("num-locked").value = 0;
                } else {
                    infoBox.style.display = "block";
                    infoBox.innerHTML = `
                        <div style="font-weight:bold; color:#1e293b; margin-bottom:4px;">🏫 Regole Tratta: SCUOLE</div>
                        <div style="color:#475569;">📍 Magazzino: <span style="font-weight:600; color:#4f46e5;">Veggiano (PD)</span></div>
                        <div style="color:#475569;">⏰ Ora Partenza: <span style="font-weight:600; color:#10b981;">07:00 (Fissa)</span></div>
                        <div style="color:#475569;">⏳ Sosta per fermata: <b>8 min</b></div>
                        <div style="color:#475569;">⚠️ Tolleranza max: consegna entro le <b>10:00</b></div>
                    `;
                    const numH10 = activeViaggio.lista_punti.filter(p => (p.orario_max||'').includes('10:')).length;
                    document.getElementById("num-locked").value = numH10;
                }
                
                renderList();
                drawMappa();
            } catch (err) {
                alert("Errore nel caricamento del viaggio: " + err.message);
                console.error(err);
            }
        }

        function renderList() {
            try {
                const cont = document.getElementById("list-container");
                cont.innerHTML = activeViaggio.lista_punti.map((p, i) => {
                    const isH10 = !activeViaggio.isGC && (p.orario_max || '').includes('10:');
                    const badgeH10 = isH10 ? `<span style="background:#fef3c7; color:#d97706; padding:2px 6px; border-radius:4px; font-size:0.65rem; font-weight:bold;">🏫 SCUOLA H10</span>` : '';
                    const badgeLate = p.isLate ? `<span style="background:#fecaca; color:#dc2626; padding:2px 6px; border-radius:4px; font-size:0.65rem; font-weight:bold; margin-left:4px;">⚠️ RITARDO ETA</span>` : '';
                    
                    return `<div class="point-card ${p.isLate ? 'late' : ''}" data-idx="${i}">
                        <div class="num-badge">${i+1}</div>
                        <div style="flex:1; user-select: none;">
                            <div style="font-weight:700; font-size:0.85rem;">${p.nome}</div>
                            <div style="font-size:0.7rem; color:#64748b;">${p.indirizzo}</div>
                            <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:4px; align-items:center;">
                                <span style="font-size:0.72rem; color:#4f46e5; font-weight:700;">
                                    Fascia: ${p.orario_min || '07:00'} - ${p.orario_max || '14:00'}
                                </span>
                                ${badgeH10}
                                ${badgeLate}
                            </div>
                            <div style="font-size:0.72rem; color:#10b981; font-weight:700; margin-top:3px; background:#f0fdf4; padding:2px 6px; border-radius:4px; display:inline-block;">
                                ⏱️ Arrivo stimato: <span style="color:#047857; font-weight:800;">${p.ora_arrivo}</span> | Ripartenza: ${p.ora_ripartenza}
                            </div>
                        </div>
                        <div class="drag-handle" style="color:#94a3b8; cursor:grab; padding: 10px; font-size: 1.2rem; user-select: none;">☰</div>
                    </div>`;
                }).join('');
            } catch (err) {
                console.error("Errore renderList: ", err);
            }
        }

        function aggiornaNumeri() {
            try {
                const cards = document.querySelectorAll('.point-card');
                let newList = [];
                cards.forEach((c, i) => {
                    c.querySelector('.num-badge').textContent = i+1;
                    const oldIdx = parseInt(c.dataset.idx);
                    newList.push(activeViaggio.lista_punti[oldIdx]);
                    c.dataset.idx = i;
                });
                activeViaggio.lista_punti = newList;
                
                calcolaETA(activeViaggio);
                renderList();
            } catch (err) {
                console.error("Errore aggiornaNumeri: ", err);
            }
        }

        async function drawMappa() {
            try {
                markers.forEach(m => m.setMap(null)); markers = [];
                if(polyline) polyline.setMap(null);

                const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
                let path = [];
                let bounds = new google.maps.LatLngBounds();
                
                const depotLat = activeViaggio.depot ? activeViaggio.depot.lat : 45.442805;
                const depotLon = activeViaggio.depot ? activeViaggio.depot.lon : 11.714498;
                
                path.push({lat: depotLat, lng: depotLon});
                bounds.extend({lat: depotLat, lng: depotLon});

                activeViaggio.lista_punti.forEach((p, i) => {
                    if(!p.lat) return;
                    path.push({lat: p.lat, lng: p.lon});
                    bounds.extend({lat: p.lat, lng: p.lon});
                    
                    const el = document.createElement("div");
                    el.className = `custom-marker ${p.isLate ? 'late' : ''}`;
                    el.innerHTML = i+1;
                    
                    const m = new AdvancedMarkerElement({ position: {lat: p.lat, lng: p.lon}, map: map, content: el });
                    markers.push(m);
                });
                
                path.push({lat: depotLat, lng: depotLon});

                polyline = new google.maps.Polyline({
                    path: path, strokeColor: "#4f46e5", strokeOpacity: 0.6, strokeWeight: 4, map: map
                });
                
                map.fitBounds(bounds);
            } catch (err) {
                alert("Errore disegno mappa: " + err.message);
                console.error(err);
            }
        }

        function salva(usa_ortools) {
            const numLocked = document.getElementById("num-locked").value;
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = "ATTENDI...";
            
            fetch('/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    viaggio_id: activeViaggio.nome_giro,
                    lista_punti: activeViaggio.lista_punti,
                    usa_ortools: usa_ortools,
                    num_locked: numLocked
                })
            }).then(r=>r.json()).then(d => {
                if(d.status === 'ok') {
                    const st = document.getElementById('status');
                    st.style.display = 'block';
                    setTimeout(()=>st.style.display='none', 3000);
                    if(usa_ortools) setTimeout(() => location.reload(), 1000);
                } else {
                    alert("Errore: " + d.msg);
                }
            }).finally(() => {
                btn.disabled = false;
                btn.textContent = usa_ortools ? "⚡ SALVA E OTTIMIZZA IL RESTO (OR-TOOLS)" : "💾 SALVA ORDINE ESATTO";
            });
        }

        window.onload = initMap;
    </script>
</body>
</html>
"""

def main():
    global DATA_GIORNO, FILE_JSON_OTTIMIZZATO
    cartella = _trova_ultima_cartella()
    if not cartella:
        print("Nessuna cartella CONSEGNE trovata.")
        sys.exit(1)
        
    DATA_GIORNO = cartella.name.replace("CONSEGNE_", "")
    FILE_JSON_OTTIMIZZATO = cartella / "viaggi_giornalieri_OTTIMIZZATO.json"
    
    # Crea il file comodo nella cartella PERCORSI_VEGGIANO
    percorsi_dir = cartella / "PERCORSI_VEGGIANO"
    percorsi_dir.mkdir(exist_ok=True)
    link_file = percorsi_dir / "00_MAPPA_INTERATTIVA.html"
    
    html_redirect = f"""<!DOCTYPE html>
<html><head>
<meta http-equiv="refresh" content="0; url=http://127.0.0.1:5001" />
<title>Avvio Mappa Interattiva...</title>
</head><body>
<p>Avvio dell'Editor Interattivo in corso... <br><a href="http://127.0.0.1:5001">Clicca qui se non vieni reindirizzato automaticamente</a></p>
<p style="color:red; font-size:12px;">(Nota: Il terminale nero del BAT 3 deve rimanere aperto in background per poter salvare le modifiche!)</p>
</body></html>"""
    link_file.write_text(html_redirect, encoding="utf-8")
    
    print(f"\n[+] EDITOR PERCORSI AVVIATO!")
    print(f"    Il motore in background e' in ascolto sulla porta 5001.")
    print(f"    E' stato creato il file '00_MAPPA_INTERATTIVA.html' nella cartella PERCORSI_VEGGIANO.")
    print(f"    Puoi aprire quel file per modificare i giri a tuo piacimento.")
    print(f"    LASCIA QUESTA FINESTRA APERTA finche' non hai finito di salvare le modifiche!\n")
    
    # Auto-apriamo comunque il file per farglielo vedere subito appena finisce il BAT 3
    def open_b():
        time.sleep(1.5)
        webbrowser.open(f"file:///{link_file.resolve().as_posix()}")
    threading.Thread(target=open_b, daemon=True).start()
    
    # Uso porta 5001 per evitare conflitti con la mappa delle zone (5000)
    app.run(port=5001, debug=False)

if __name__ == "__main__":
    main()

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
try:
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    HAS_OR_TOOLS = True
except ImportError:
    HAS_OR_TOOLS = False

# CONFIGURAZIONE STRUTTURALE
DRIVE_PATH = r"G:\Il mio Drive\Fatturazione"
API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"
DEPOT_STR = "Via alessandro volta, 25/a, 35030 Veggiano PD"
DEPOT_COORDS = {"lat": 45.442805, "lng": 11.714498}

CACHE_FILE = os.path.join(DRIVE_PATH, "CACHE_CONSEGNE_TOP.json")
CONFIG_FILE = os.path.join(DRIVE_PATH, "MESE_IN_CORSO.txt")

def get_mese_in_corso():
    if not os.path.exists(CONFIG_FILE):
        print("❌ ERRORE: MESE_IN_CORSO.txt non trovato. Esegui prima 1_Riepiloghi_Giornalieri.py!")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def get_geocode(address, cache):
    clean_addr = str(address).replace(".0", "").replace("nan", "").strip()
    if not clean_addr: return None
    if clean_addr in cache: return cache[clean_addr]
        
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(clean_addr + ', Italia')}&key={API_KEY}"
    try:
        r = requests.get(url).json()
        if r['status'] == 'OK':
            loc = r['results'][0]['geometry']['location']
            coords = {"lat": loc['lat'], "lng": loc['lng']}
            cache[clean_addr] = coords
            return coords
    except Exception as e:
        pass
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

def calcola_km_stradali(ordered_stops, depot_coords, api_key):
    if not ordered_stops:
        return 0.0
    
    punti_pieni = [depot_coords] + ordered_stops + [depot_coords]
    km_tot = 0.0
    chunk_size = 20
    
    for i in range(0, len(punti_pieni)-1, chunk_size):
        sub = punti_pieni[i:i+chunk_size+1]
        if len(sub) < 2: continue
        
        origin = f"{sub[0]['lat']},{sub[0]['lng']}"
        dest = f"{sub[-1]['lat']},{sub[-1]['lng']}"
        
        if len(sub) > 2:
            waypts = "|".join([f"{p['lat']},{p['lng']}" for p in sub[1:-1]])
            way_str = f"&waypoints={waypts}"
        else:
            way_str = ""
            
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={dest}{way_str}&key={api_key}"
        try:
            r = requests.get(url).json()
            if r.get('status') == 'OK':
                for leg in r['routes'][0]['legs']:
                    km_tot += leg['distance']['value']
        except Exception:
            pass
            
    return km_tot / 1000.0


def solve_tsp_google(locations):
    ordered_stops = ottimizza_percorso_ortools(locations, DEPOT_COORDS)
    km_totali = calcola_km_stradali(ordered_stops, DEPOT_COORDS, API_KEY)
    return ordered_stops, km_totali

def elabora_tutte_le_mappe_google():
    mese = get_mese_in_corso()
    INPUT_DIR = os.path.join(DRIVE_PATH, "Riepiloghi_Giornalieri", mese)
    OUTPUT_DIR = os.path.join(DRIVE_PATH, "Mappe_Complete_Google", mese)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Avvio Mappe con Algoritmo OR-TOOLS/GOOGLE da {INPUT_DIR}...")
    cache = load_cache()
    files = glob.glob(os.path.join(INPUT_DIR, "*.xlsx"))
    
    if not files:
        print(f"❌ Nessun file trovato nella cartella del mese: {INPUT_DIR}")
        return
    
    for file_target in sorted(files):
        match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(file_target))
        if not match: continue
        data_viaggio = match.group(1)
        
        print(f"\nGenerazione Mappa Google: {data_viaggio}")
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
                            
        trips_output = []
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
                        "lng": coords['lng']
                    })
            
            if stops_with_coords:
                ordered_stops, km_totali = solve_tsp_google(stops_with_coords)
                
                base_url = "https://www.google.com/maps/dir/?api=1"
                origin = "&origin=" + urllib.parse.quote(DEPOT_STR)
                destination = "&destination=" + urllib.parse.quote(DEPOT_STR)
                
                wa_stops = []
                for sp in ordered_stops:
                    addr_wa = sp["indirizzo"]
                    if "SAPPADA" in addr_wa.upper():
                        addr_wa = addr_wa.replace("32047", "33012").replace("(BL)", "(UD)")
                    wa_stops.append(urllib.parse.quote(addr_wa))
                
                waypoints = "&waypoints=" + "|".join(wa_stops)
                wa_link = f"{base_url}{origin}{destination}{waypoints}&travelmode=driving"
                
                trips_output.append({
                    "id": code,
                    "stops": ordered_stops,
                    "km_str": f"{km_totali:.1f} km calcolati",
                    "wa": wa_link
                })
                
        if trips_output:
            html_filename = os.path.join(OUTPUT_DIR, f"3_Mappa_GMaps_{data_viaggio}.html")
            
            try:
                date_obj = datetime.strptime(data_viaggio, "%Y-%m-%d")
                data_bella = date_obj.strftime("%d/%m/%Y")
            except:
                data_bella = data_viaggio
                
            HTML_CODE = f"""<!DOCTYPE html><html><head><title>Mappa Google Directions {data_bella}</title><meta charset='utf-8'><script src='https://maps.googleapis.com/maps/api/js?key={API_KEY}'></script>
            <style>body,html{{height:100%;margin:0;font-family:sans-serif;background:#eff6ff;}}#map{{height:100%;width:100%;position:fixed;}}#side{{position:absolute;top:10px;left:10px;width:320px;background:white;padding:15px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,0.3);z-index:100;max-height:90vh;overflow-y:auto;}}.card{{border:2px solid #eee;border-radius:12px;padding:12px;margin-bottom:12px;cursor:pointer;}}.active-card{{border-color:#4f46e5;background:#f0f3ff;}}.wa-btn{{display:block;background:#3b82f6;color:white;text-align:center;padding:10px;border-radius:10px;font-weight:800;text-decoration:none;margin-top:10px;}}</style>
            </head><body><div id='side'><h2 style='color:#4f46e5;margin:0;'>Log Solution</h2><p style='font-size:0.8rem;color:grey;'>Ottimizzazione Nativa Google - {data_bella}</p><div id='cards'></div></div><div id='map'></div><script>
            const trips={json.dumps(trips_output)};
            let map, ds, dr, markers=[];
            function initMap(){{
                map=new google.maps.Map(document.getElementById('map'),{{center:{{lat:45.8,lng:12.1}},zoom:9}});
                ds=new google.maps.DirectionsService(); dr=new google.maps.DirectionsRenderer({{map:map, suppressMarkers:true}});
                trips.forEach((t,i)=>{{
                    const card=document.createElement('div'); card.className='card'; card.id='card-'+i;
                    card.innerHTML=`<b>Furgone: ${{t.id}}</b><div id='km-${{i}}' style='font-weight:bold;color:#16a34a;margin:5px 0;'>${{t.km_str}}</div><div style='font-size:0.75rem;color:grey;'>${{t.stops.map((s,idx)=>(idx+1)+'. '+s.nome).join('<br>')}}</div><a href="${{t.wa}}" target="_blank" class='wa-btn'>Avvia Navigatore WhatsApp</a>`;
                    card.onclick=()=>selectTrip(i); document.getElementById('cards').appendChild(card);
                }});
                if(trips.length > 0) selectTrip(0);
            }}
            function selectTrip(idx){{
                document.querySelectorAll('.card').forEach(el=>el.classList.remove('active-card')); document.getElementById('card-'+idx).classList.add('active-card');
                const t=trips[idx]; markers.forEach(m=>m.setMap(null)); markers=[];
                markers.push(new google.maps.Marker({{position:{{lat:{DEPOT_COORDS['lat']},lng:{DEPOT_COORDS['lng']}}}, map:map, label:'H'}}));
                t.stops.forEach((s, i) => {{ markers.push(new google.maps.Marker({{position: {{lat:s.lat, lng:s.lng}}, map:map, label: (i+1).toString()}})); }});
                // CHIAVE: optimizeWaypoints ORA È FALSE PERCHE' I PUNTI SONO GIA' ORDINATI E DEVONO ESSERE RISPETTATI
                ds.route({{origin:'{DEPOT_STR}',destination:'{DEPOT_STR}',waypoints:t.stops.map(s=>({{location:new google.maps.LatLng(s.lat,s.lng),stopover:true}})),travelMode:'DRIVING',optimizeWaypoints:false}},(res,stat)=>{{ if(stat==='OK') dr.setDirections(res); }});
            }}google.maps.event.addDomListener(window,'load',initMap);</script></body></html>"""
            
            with open(html_filename, "w", encoding="utf-8") as f:
                f.write(HTML_CODE)
            print(f"  -> File HTML Google nativo salvato: {os.path.basename(html_filename)}")

    save_cache(cache)
    print("\n[SUCCESSO] Le mappe perfette Google Directions sono pronte.")

if __name__ == "__main__":
    elabora_tutte_le_mappe_google()

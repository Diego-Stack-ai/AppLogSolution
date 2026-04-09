import os
import glob
import pandas as pd
import openpyxl
import json
import requests
import re
import urllib.parse
from datetime import datetime
import math
import sys
import firebase_admin
from firebase_admin import credentials, firestore
try:
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    HAS_OR_TOOLS = True
except ImportError:
    HAS_OR_TOOLS = False

# CONFIGURAZIONE
DRIVE_PATH = r"G:\Il mio Drive\Fatturazione"
API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"
DEPOT_COORDS = {"lat": 45.442805, "lng": 11.714498}
CACHE_FILE = os.path.join(DRIVE_PATH, "CACHE_CONSEGNE_TOP.json")
WARNING_FILE = os.path.join(DRIVE_PATH, "Avvisi_Geografici.txt")
CONFIG_FILE = os.path.join(DRIVE_PATH, "MESE_IN_CORSO.txt")

def get_mese_in_corso():
    if not os.path.exists(CONFIG_FILE):
        print("❌ ERRORE: MESE_IN_CORSO.txt non trovato. Esegui prima 1_Riepiloghi_Giornalieri.py!")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()
DRIVE_PATH = r"G:\Il mio Drive\Fatturazione"
API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"
DEPOT_COORDS = {"lat": 45.442805, "lng": 11.714498}
CACHE_FILE = os.path.join(DRIVE_PATH, "CACHE_CONSEGNE_TOP.json")
WARNING_FILE = os.path.join(DRIVE_PATH, "Avvisi_Geografici.txt")

# Pulisci il file di log precedente se esiste
if os.path.exists(WARNING_FILE):
    os.remove(WARNING_FILE)

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
            clients_cache[key1] = {"lat": lat, "lng": lng}
            
    print(f"📡 Sincronizzate {len(clients_cache)} coordinate da Firebase (GRAN CHEF) per i calcoli KM.")
    return clients_cache

def save_cache(cache):
    pass # Nessun salvataggio necessario, Firebase è SSoT

def get_geocode(address, expected_pr, cache, date_str, trip_code, customer_name):
    # Cerca indirizzo su Firebase Cache 
    clean_addr = str(address).replace(".0", "").replace("nan", "").strip().lower()
    if not clean_addr: return None
    
    if clean_addr in cache: 
        return cache[clean_addr]
        
    # Ricerca di fallback (se l'indirizzo contiene parti)
    for k, v in cache.items():
        if k and clean_addr in k:
            return v
    
    print(f"[{date_str} - {trip_code}] ⚠️ Coord mancante su Firebase per: {customer_name} ({clean_addr})")
    
    with open(WARNING_FILE, "a", encoding="utf-8") as fw:
        fw.write(f"[{date_str} - {trip_code}] MANCA COORDINATA in Firebase per {customer_name}:\n")
        fw.write(f"   Indirizzo Viaggio: {clean_addr}. Aggiungi latitudine/longitudine su WebApp PWA!\n\n")
        
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


def solve_tsp_google_km(locations):
    ordered_stops = ottimizza_percorso_ortools(locations, DEPOT_COORDS)
    km_totali = calcola_km_stradali(ordered_stops, DEPOT_COORDS, API_KEY)
    return km_totali

def estrai_e_calcola():
    mese = get_mese_in_corso()
    print(f"Avvio Calcolo Chilometrico Mensile OR-TOOLS NATIVO per il mese [{mese.upper()}]...")
    cache = load_cache()
    
    input_dir = os.path.join(DRIVE_PATH, "Riepiloghi_Giornalieri", mese)
    if not os.path.exists(input_dir):
        print(f"❌ Cartella {input_dir} non trovata.")
        sys.exit(1)
        
    files = glob.glob(os.path.join(input_dir, "*.xlsx"))
    
    risultati_mensili = {}
    
    for file_path in sorted(files):
        match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(file_path))
        if not match: continue
        data_viaggio = match.group(1)
        
        print(f"Analizzando data KM: {data_viaggio}")
        wb = openpyxl.load_workbook(file_path, data_only=True)
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
                                "full_address": full_a,
                                "pr_excel": pr
                            })

        risultati_mensili[data_viaggio] = {}
        
        for code, stops in trips_stops.items():
            coords_list = []
            for s in stops:
                c = get_geocode(s["full_address"], s["pr_excel"], cache, data_viaggio, code, s["ragione_sociale"])
                if c: coords_list.append(c)
                
            num_tappe = len(coords_list)  # escluso magazzino (non è nelle stops)
            
            if not coords_list:
                risultati_mensili[data_viaggio][code] = 0.0
                risultati_mensili[data_viaggio][f"{code}_tappe"] = 0
                continue
                
            # USA GOOGLE NATIVO INVECE DI OR-TOOLS
            km_totali = solve_tsp_google_km(coords_list)
            risultati_mensili[data_viaggio][code] = int(km_totali)
            risultati_mensili[data_viaggio][f"{code}_tappe"] = num_tappe

    save_cache(cache)
    
    if risultati_mensili:
        df_out = pd.DataFrame.from_dict(risultati_mensili, orient='index')
        df_out.index.name = 'Data'
        df_out.reset_index(inplace=True)
        df_out = df_out.sort_values('Data')
        
        out_file = os.path.join(DRIVE_PATH, "Riepiloghi_Giornalieri", mese, f"Riepilogo_KM_Mensile_{mese.upper()}.xlsx")
        df_out.to_excel(out_file, index=False)
        print("\n✅ Calcolo KM Mensile completato e allineato stradalmente!")

if __name__ == "__main__":
    estrai_e_calcola()

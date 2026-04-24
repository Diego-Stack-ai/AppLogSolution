from flask import Flask, render_template, jsonify, request
import json
import socket
import math
from pathlib import Path

app = Flask(__name__, template_folder='templates')

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

DEPOT = {"lat": 45.442805, "lon": 11.714498, "nome": "DEPOSITO VEGGIANO", "indirizzo": "Via Alessandro Volta 25/a, 35030 Veggiano (PD)"}

def haversine(p1, p2):
    try:
        lat1, lon1 = float(p1.get('lat', 0)), float(p1.get('lon', p1.get('lng', 0)))
        lat2, lon2 = float(p2.get('lat', 0)), float(p2.get('lon', p2.get('lng', 0)))
    except: return 999999.0
    R = 6371 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

def ottimizza_percorso(punti):
    """Logica identica a BAT 3"""
    if not punti: return []
    non_visitati, percorso, corrente = punti[:], [], DEPOT
    while non_visitati:
        idx, pross = min(enumerate(non_visitati), key=lambda x: (haversine(corrente, x[1]), x[0]))
        percorso.append(pross)
        non_visitati.pop(idx)
        corrente = pross
    return percorso

def get_latest_data():
    dirs = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
    if not dirs: return None
    latest = max(dirs, key=lambda d: d.stat().st_ctime)
    json_path = latest / "viaggi_giornalieri.json"
    if not json_path.exists(): return None
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [z for z in data if z.get("id_zona", "") != "DDT_DA_INSERIRE"]

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "127.0.0.1"

@app.route("/")
@app.route("/viaggio/<v_id>")
def index(v_id=None):
    viaggi_raw = get_latest_data()
    if not viaggi_raw: return "Errore: Nessun dato viaggi trovato."
    
    # Lista rapida dei viaggi per il menu in basso
    all_trips_info = [{"id": f"V{i+1:02d}", "name": f"Viaggio {i+1}"} for i, _ in enumerate(viaggi_raw)]
    
    if v_id is None:
        v_id = "V01"
        
    try:
        v_idx = int(v_id.replace("V", "")) - 1
    except:
        v_idx = 0
        
    if v_idx >= len(viaggi_raw): v_idx = 0
    
    current_trip_raw = viaggi_raw[v_idx]
    punti_raw = current_trip_raw.get("lista_punti", [])
    
    # Ottimizziamo la sequenza come BAT 3
    perc_ottimizzato = ottimizza_percorso(punti_raw)
    
    deliveries = []
    for i, p in enumerate(perc_ottimizzato):
        deliveries.append({
            "id": i + 1,
            "numero_consegna": i + 1,
            "cliente": p.get("nome"),
            "indirizzo": p.get("indirizzo"),
            "lat": p.get("lat"),
            "lng": p.get("lon")
        })
        
    return render_template(
        "autisti.html", 
        v_id=v_id,
        deliveries=deliveries, 
        deliveries_js=json.dumps(deliveries),
        api_key=GOOGLE_MAPS_API_KEY,
        all_trips_info=all_trips_info
    )

if __name__ == "__main__":
    ip = get_local_ip()
    print("-" * 60)
    print(f"📡 SERVER MOBILE AUTISTI OPERATIVO")
    print(f"💻 Sul computer: http://localhost:5000")
    print(f"🤳 Sulla rete (Link WhatsApp): http://{ip}:5000")
    print("-" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)

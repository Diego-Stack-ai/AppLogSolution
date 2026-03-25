import json
import math
import re
import requests
from pathlib import Path

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

DEPOT = {"lat": 45.442805, "lon": 11.714498, "nome": "DEPOSITO VEGGIANO", "indirizzo": "Via Alessandro Volta 25/a, 35030 Veggiano (PD)"}

def get_latest_consegne_dir():
    dirs = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
    if not dirs: return None
    return max(dirs, key=lambda d: d.name)

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
    if not punti: return []
    non_visitati, percorso, corrente = punti[:], [], DEPOT
    while non_visitati:
        idx, pross = min(enumerate(non_visitati), key=lambda x: (haversine(corrente, x[1]), x[0]))
        percorso.append(pross)
        non_visitati.pop(idx)
        corrente = pross
    return percorso

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ v_id }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}"></script>
    <style>
        :root { --p: #4f46e5; --accent: #10b981; }
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Outfit', sans-serif; background: #f8fafc; overflow: hidden; }
        .main-container { display: flex; flex-direction: column; height: 100vh; }
        #map { height: 48vh; width: 100%; background: #dfe5eb; position: relative; }
        #sidebar { flex: 1; display: flex; flex-direction: column; background: white; border-top: 3px solid #cbd5e1; overflow: hidden; }
        .header { padding: 12px 18px; background: #1e293b; color: white; border-bottom: 2px solid var(--accent); }
        .trip-title { margin: 0; font-size: 1rem; font-weight: 800; display: flex; align-items: center; gap: 8px; }
        #delivery-list { flex: 1; overflow-y: auto; padding: 12px; background: #f1f5f9; padding-bottom: 50px; }
        .btn-global { display: flex; align-items: center; justify-content: center; gap: 8px; background: var(--p); color: white; border: none; padding: 14px; border-radius: 12px; width: 100%; font-size: 0.85rem; font-weight: 800; text-decoration: none; margin-bottom: 12px; }
        .card { background: white; border-radius: 16px; padding: 14px; margin-bottom: 10px; display: flex; align-items: center; gap: 12px; border: 1.5px solid #cbd5e1; cursor: pointer; position: relative; }
        .card.next { border-color: var(--accent); background: #f0fdf4; border-left: 5px solid var(--accent); }
        .stop-num { width: 30px; height: 30px; background: var(--p); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px; flex-shrink: 0; }
        .next .stop-num { background: var(--accent); }
        .stop-info { flex: 1; min-width: 0; }
        .name { display: block; font-size: 0.88rem; font-weight: 800; color: #1e293b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .addr { font-size: 0.72rem; color: #64748b; font-weight: 600; }
        .btn-nav { background: var(--accent); color: white; width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; text-decoration: none; flex-shrink: 0; }
        .icon-nav { width: 22px; height: 22px; fill: white; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="map"></div>
        <div id="sidebar">
            <div class="header">
                <h2 class="trip-title">🏎️ {{ v_id }} | Giro Autista</h2>
            </div>
            <div id="delivery-list">
                <a href="https://www.google.com/maps/dir/?api=1&destination={{ first_lat }},{{ first_lon }}" class="btn-global">🚀 APRI TUTTE LE TAPPE</a>
                {{ cards_html|safe }}
            </div>
        </div>
    </div>
    <script>
        const data = {{ deliveries_js|safe }}; let map, markers = [];
        const navIcon = `<svg class="icon-nav" viewBox="0 0 24 24"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>`;

        function initMap() {
            try {
                map = new google.maps.Map(document.getElementById("map"), { 
                    zoom: 12, center: { lat: data[0].lat, lng: data[0].lon },
                    disableDefaultUI: false, streetViewControl: false
                });

                const directionsService = new google.maps.DirectionsService();
                const directionsRenderer = new google.maps.DirectionsRenderer({ 
                    map, suppressMarkers: true, polylineOptions: { strokeColor: "#4f46e5", strokeOpacity: 0.8, strokeWeight: 6 } 
                });
                
                const waypts = data.slice(1, -1).map(d => ({ location: { lat: d.lat, lng: d.lon }, stopover: true }));
                directionsService.route({ 
                    origin: { lat: data[0].lat, lng: data[0].lon }, 
                    destination: { lat: data[data.length-1].lat, lng: data[data.length-1].lon }, 
                    waypoints: waypts, travelMode: "DRIVING" 
                }, (res, status) => { if (status === "OK") directionsRenderer.setDirections(res); });

                data.forEach((p, i) => {
                    const marker = new google.maps.Marker({
                        position: { lat: p.lat, lng: p.lon }, map: map, 
                        label: { text: (i+1).toString(), color: "white", fontWeight: "bold" },
                        title: p.cliente
                    });
                    marker.addListener("click", () => {
                       new google.maps.InfoWindow({ content: `<div style="padding:5px;"><b>${i+1}. ${p.cliente}</b></div>` }).open(map, marker);
                    });
                    markers.push(marker);
                });
                const b = new google.maps.LatLngBounds(); data.forEach(p => b.extend({ lat: p.lat, lng: p.lon })); map.fitBounds(b);
            } catch (e) { console.error(e); }
        }
        function focusOn(i) { map.panTo(markers[i].getPosition()); map.setZoom(17); }
        window.onload = initMap;
    </script>
</body>
</html>"""

def main():
    target_dir = get_latest_consegne_dir()
    if not target_dir: return
    json_path = target_dir / "viaggi_giornalieri.json"
    if not json_path.exists(): return
    with open(json_path, "r", encoding="utf-8") as f: viaggi = json.load(f)

    out_folder = target_dir / "MAPPE_MOBILE_WHATSAPP"
    out_folder.mkdir(exist_ok=True)
    
    # Icona SVG pre-renderizzata per le card
    svg_icon = '<svg width="22" height="22" viewBox="0 0 24 24" fill="white"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>'

    for i, v in enumerate(viaggi):
        v_id = f"V{i+1:02d}"
        punti_raw = v.get("lista_punti", [])
        if not punti_raw: continue
        
        zone_list = sorted(list(set([str(p.get('zona', '0000')) for p in punti_raw])))
        fname = f"{v_id}_Zone_{'_'.join(zone_list[:4])}.html"
        
        perc = ottimizza_percorso(punti_raw)
        deliveries = [{"cliente": p.get("nome", "Cliente"), "indirizzo": p.get("indirizzo", "-"), "lat": p.get("lat"), "lon": p.get("lon")} for p in perc]

        cards_html = ""
        for idx, d in enumerate(deliveries):
            is_next = "next" if idx == 0 else ""
            cards_html += f'''
            <div class="card {is_next}" onclick="focusOn({idx})">
                <div class="stop-num">{idx+1}</div>
                <div class="stop-info"><b class="name">{d['cliente']}</b><span class="addr">{d['indirizzo']}</span></div>
                <a href="https://www.google.com/maps/dir/?api=1&destination={d['lat']},{d['lon']}&travelmode=driving" class="btn-nav">{svg_icon}</a>
            </div>'''

        html = HTML_TEMPLATE.replace("{{ v_id }}", v_id).replace("{{ api_key }}", GOOGLE_MAPS_API_KEY)
        html = html.replace("{{ first_lat }}", str(deliveries[0]['lat'])).replace("{{ first_lon }}", str(deliveries[0]['lon']))
        html = html.replace("{{ cards_html|safe }}", cards_html)
        html = html.replace("{{ deliveries_js|safe }}", json.dumps(deliveries))
        
        (out_folder / fname).write_text(html, encoding="utf-8")
        print(f" ✅ Generata Mappa (Fix Icone SVG): {fname}")

if __name__ == "__main__": main()

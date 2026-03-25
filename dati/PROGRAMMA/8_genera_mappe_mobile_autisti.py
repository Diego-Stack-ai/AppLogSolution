import json
import math
import re
import requests
from pathlib import Path

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
ROOT_DIR = PROG_DIR.parent.parent
CONSEGNE_DIR = PROG_DIR.parent / "CONSEGNE"
WEBAPP_FOLDER = ROOT_DIR / "frontend" / "mappe_autisti"
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
    <script src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}&libraries=geometry,marker"></script>
    <style>
        :root { --p: #4f46e5; --accent: #10b981; }
        body, html { margin: 0; padding: 0; height: 100%; font-family: 'Outfit', sans-serif; background: #f8fafc; overflow: hidden; }
        .main-container { display: flex; flex-direction: column; height: 100vh; }
        #map { height: 50vh; width: 100%; background: #dfe5eb; position: relative; }
        #sidebar { flex: 1; display: flex; flex-direction: column; background: white; border-top: 1px solid #cbd5e1; overflow: hidden; }
        .header { padding: 6px 15px; background: #1e293b; color: white; border-bottom: 2px solid var(--accent); }
        .trip-title { margin: 0; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 6px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9; }
        #delivery-list { flex: 1; overflow-y: auto; padding: 10px; background: #f1f5f9; padding-bottom: 40px; }
        .card { background: white; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; border: 1px solid #cbd5e1; cursor: pointer; transition: 0.2s; }
        .card.next { border-color: var(--accent); background: #f0fdf4; border-left: 4px solid var(--accent); }
        .stop-num { width: 26px; height: 26px; background: var(--p); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 11px; flex-shrink: 0; }
        .next .stop-num { background: var(--accent); }
        .stop-info { flex: 1; min-width: 0; }
        .name { display: block; font-size: 0.82rem; font-weight: 800; color: #1e293b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .addr { font-size: 0.68rem; color: #64748b; font-weight: 600; }
        .btn-nav { background: var(--accent); color: white; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; text-decoration: none; flex-shrink: 0; }
        .icon-nav { width: 20px; height: 20px; fill: white; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="map"></div>
        <div id="sidebar">
            <div class="header">
                <h2 class="trip-title">🚛 {{ v_id }} | NAVIGATORE AUTISTI</h2>
            </div>
            <div id="delivery-list">
                {{ cards_html|safe }}
            </div>
        </div>
    </div>
    <script>
        const data = {{ deliveries_js|safe }}; let map, markers = [];
        const svg_icon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>';

        async function initMap() {
            try {
                map = new google.maps.Map(document.getElementById("map"), { zoom: 12, center: { lat: data[0].lat, lng: data[0].lon }, disableDefaultUI: false });
                const directionsService = new google.maps.DirectionsService();
                const directionsRenderer = new google.maps.DirectionsRenderer({ map, suppressMarkers: true, polylineOptions: { strokeColor: "#4f46e5", strokeOpacity: 0.8, strokeWeight: 6 } });
                const waypts = data.slice(1, -1).map(d => ({ location: { lat: d.lat, lng: d.lon }, stopover: true }));
                directionsService.route({ origin: { lat: data[0].lat, lng: data[0].lon }, destination: { lat: data[data.length-1].lat, lng: data[data.length-1].lon }, waypoints: waypts, travelMode: "DRIVING" }, (status === "OK") ? res => directionsRenderer.setDirections(res) : null);
                data.forEach((p, i) => {
                    const marker = new google.maps.Marker({ position: { lat: p.lat, lng: p.lon }, map: map, label: { text: (i+1).toString(), color: "white", fontWeight: "bold" }, title: p.cliente });
                    marker.addListener("click", () => { new google.maps.InfoWindow({ content: `<div style="padding:5px;"><b>${i+1}. ${p.cliente}</b></div>` }).open(map, marker); });
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
    with open(json_path, "r", encoding="utf-8") as f: viaggi = json.load(f)

    out_folder = target_dir / "MAPPE_MOBILE_WHATSAPP"
    out_folder.mkdir(exist_ok=True)
    WEBAPP_FOLDER.mkdir(exist_ok=True, parents=True)
    
    svg_icon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>'

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
        html = HTML_TEMPLATE.replace("{{ v_id }}", v_id).replace("{{ api_key }}", GOOGLE_MAPS_API_KEY).replace("{{ first_lat }}", str(deliveries[0]['lat'])).replace("{{ first_lon }}", str(deliveries[0]['lon'])).replace("{{ cards_html|safe }}", cards_html).replace("{{ deliveries_js|safe }}", json.dumps(deliveries))
        (out_folder / fname).write_text(html, encoding="utf-8")
        (WEBAPP_FOLDER / fname).write_text(html, encoding="utf-8")

    txt_content = "🚀 LINK MAPPE PER AUTISTI (GIORNO CORRENTE)\n------------------------------------------\n\n"
    for i, v in enumerate(viaggi):
        punti_raw = v.get("lista_punti", [])
        if not punti_raw: continue
        zone_list = sorted(list(set([str(p.get('zona', '0000')) for p in punti_raw])))
        fname = f"V{i+1:02d}_Zone_{'_'.join(zone_list[:4])}.html"
        github_link = f"https://diego-stack-ai.github.io/AppLogSolution/frontend/mappe_autisti/{fname}"
        txt_content += f"🏎️ V{i+1:02d}: {github_link}\n\n"
    (out_folder / "LINK_WHATSAPP_AUTISTI.txt").write_text(txt_content, encoding="utf-8")
    (WEBAPP_FOLDER / "LINK_WHATSAPP_AUTISTI.txt").write_text(txt_content, encoding="utf-8")

    print(f"\n🚀 OPERAZIONE COMPLETATA!\n🎨 File pronti in: {out_folder}\n📄 Link salvati in: LINK_WHATSAPP_AUTISTI.txt\n🌐 Esegui 'git push' e 'firebase deploy' per aggiornare i link.")

if __name__ == "__main__": main()

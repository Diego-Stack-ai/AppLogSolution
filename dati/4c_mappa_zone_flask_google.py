from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import sys
import re
import webbrowser
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

# --- CONFIGURAZIONE ---
BASE_DIR = Path(__file__).resolve().parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GEOCODE_CACHE = BASE_DIR / "geocode_cache.json"

# INSERISCI QUI LA TUA API KEY DI GOOGLE MAPS
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Variabili globali per tracciare i file in uso
TARGET_FILE_UNIFICATO = None
TARGET_FILE_3B = None
TARGET_FILE_2B = None
ZONE_LIST_CACHE = []
DATA_GIORNO = ""

def _get_color(idx):
    palette = [
        "#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", 
        "#ec4899", "#06b6d4", "#f97316", "#14b8a6", "#6366f1",
        "#a855f7", "#3b82f6", "#22c55e", "#d946ef", "#84cc16"
    ]
    return palette[idx % len(palette)]

def _aggiorna_mappatura_destinazioni(nome, lat, lon):
    try:
        import pandas as pd
        file_path = BASE_DIR / "mappatura_destinazioni.xlsx"
        if not file_path.exists(): return False
        
        df = pd.read_excel(file_path)
        mask = df['nome'].astype(str).str.lower() == str(nome).lower()
        if mask.any():
            df.loc[mask, 'latitudine'] = lat
            df.loc[mask, 'longitudine'] = lon
            df.to_excel(file_path, index=False)
            return True
    except PermissionError:
        print(f"[ERR] Impossibile scrivere su {file_path.name}: il file è aperto in Excel!")
        return "file_aperto"
    except Exception as e:
        print(f"Errore aggiornamento Excel: {e}")
        return str(e)
    return False

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, 
                                  DATA_GIORNO=DATA_GIORNO, 
                                  JSON_ZONE=json.dumps(ZONE_LIST_CACHE, ensure_ascii=False),
                                  GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)

@app.route('/save', methods=['POST'])
def save():
    global ZONE_LIST_CACHE
    try:
        data = request.json
        ZONE_LIST_CACHE = data
        
        # 1. Aggiorna il file unificato
        if TARGET_FILE_UNIFICATO and TARGET_FILE_UNIFICATO.exists():
            unificato_raw = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
            punti_flat = unificato_raw.get("punti", [])
            
            mappa_point_to_zona = {}
            for z in data:
                for p in z["lista_punti"]:
                    pid = p.get("codice_frutta") or p.get("codice_latte") or p.get("nome")
                    mappa_point_to_zona[pid] = z["id_zona"]
            
            for p in punti_flat:
                pid = p.get("codice_frutta") or p.get("codice_latte") or p.get("nome")
                if pid in mappa_point_to_zona:
                    p["zona"] = mappa_point_to_zona[pid]
                    
            TARGET_FILE_UNIFICATO.write_text(json.dumps(unificato_raw, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 2. Salva 3b
        if TARGET_FILE_3B:
            TARGET_FILE_3B.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 3. Ricostruisci 2b
        if TARGET_FILE_2B:
            new_2b = []
            for z in data:
                new_2b.append({
                    "id_zona": z["id_zona"],
                    "nome_zona": z["nome_zona"],
                    "codici_luogo": sorted([str(p.get("codice_frutta") or p.get("codice_latte") or "") for p in z["lista_punti"]]),
                    "tipologia": z["tipologia"]
                })
            TARGET_FILE_2B.write_text(json.dumps(new_2b, indent=2, ensure_ascii=False), encoding="utf-8")
            
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Errore save: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/save_coord', methods=['POST'])
def save_coord():
    payload = request.json # {nome, lat, lon}
    result = _aggiorna_mappatura_destinazioni(payload['nome'], payload['lat'], payload['lon'])
    
    if result is True:
        return jsonify({"status": "ok", "msg": f"Posizione salvata per {payload['nome']}!"})
    elif result == "file_aperto":
        return jsonify({"status": "error", "msg": "ERRORE: Chiudi il file Excel 'mappatura_destinazioni.xlsx' e riprova!"}), 500
    else:
        return jsonify({"status": "error", "msg": f"Errore: {result}"}), 500

def _salva_html_fisico(output_base, template_html, data, zone_json, api_key):
    html_content = template_html.replace("{{DATA_GIORNO}}", data).replace("{{JSON_ZONE}}", zone_json).replace("{{GOOGLE_MAPS_API_KEY}}", api_key)
    file_path = output_base / "4_mappa_zone_google.html"
    file_path.write_text(html_content, encoding="utf-8")
    print(f"[FILE] Mappa fisica creata: {file_path.name}")

# --- TEMPLATE HTML (GOOGLE MAPS VERSION) ---
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <title>Gestione Zone {{DATA_GIORNO}}</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?key={{GOOGLE_MAPS_API_KEY}}&libraries=geometry"></script>
    <style>
        :root { --primary: #4f46e5; --bg: #f1f5f9; --text: #1e293b; }
        * { box-sizing: border-box; }
        body { margin: 0; font-family: 'Outfit', sans-serif; height: 100vh; display: flex; background: var(--bg); color: var(--text); overflow: hidden; }
        #sidebar { width: 380px; height: 100%; background: white; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; z-index: 1000; box-shadow: 4px 0 25px rgba(0,0,0,0.08); }
        #header { padding: 25px 20px; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; }
        #header h1 { margin: 0; font-size: 1.4rem; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }
        #zone-list { flex: 1; overflow-y: auto; padding: 15px; background: #f8fafc; }
        .zone-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px; margin-bottom: 10px; cursor: pointer; transition: 0.2s; }
        .zone-card:hover { border-color: #cbd5e1; }
        .zone-card.selected { border: 2px solid var(--primary); background: #f5f3ff; }
        .zone-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .color-pill { width: 12px; height: 12px; border-radius: 50%; }
        .zone-title { font-weight: 700; font-size: 0.95rem; flex: 1; }
        .badge-tipo { padding: 3px 6px; font-size: 0.6rem; border-radius: 4px; text-transform: uppercase; font-weight: 800; }
        .badge-mista { background: #fef3c7; color: #92400e; }
        .badge-latte { background: #dcfce7; color: #166534; }
        #map { flex: 1; z-index: 1; }
        .btn { flex: 1; padding: 6px; font-size: 0.7rem; font-weight: 800; border: 1px solid #e2e8f0; background: white; border-radius: 6px; cursor: pointer; color: #64748b; }
        .btn:hover { background: #f1f5f9; }
        #save-status { position: fixed; bottom: 20px; left: 400px; padding: 10px 20px; border-radius: 30px; background: #10b981; color: white; font-weight: 700; display: none; z-index: 3000; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }

        /* NUOVE ICONE PERSONALIZZATE GOOGLE MAPS */
        .custom-marker {
            position: absolute; width: 32px; height: 32px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 800; font-size: 11px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.3); border: 2px solid white;
            transition: transform 0.2s; cursor: pointer;
            pointer-events: auto; transform: translate(-50%, -100%);
        }
        .custom-marker:hover { transform: translate(-50%, -105%) scale(1.15); z-index: 999; }
        .m-tonda { border-radius: 50%; }
        .m-goccia { border-radius: 50% 50% 50% 0; transform: translate(-50%, -100%) rotate(-45deg); }
        .m-goccia span { transform: rotate(45deg); display: block; }
        .m-foglia { border-radius: 12px 2px 12px 2px; transform: translate(-50%, -100%) rotate(45deg); }
        .m-foglia span { transform: rotate(-45deg); }
    </style>
</head>
<body>
    <div id="sidebar">
        <div id="header">
            <h1>Gestione Zone <span id="tot-points" style="font-size:0.8rem; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-weight: 400;">0 Punti</span></h1>
            <div style="display:flex; justify-content: space-between; align-items: center; margin-top:5px;">
                <span style="opacity:0.7; font-size:0.8rem;">Data: {{DATA_GIORNO}}</span>
                <button onclick="saveAllToServer()" id="btn-master-save" style="background:#10b981; color:white; border:none; padding:4px 10px; border-radius:5px; font-weight:700; cursor:pointer; font-size:0.7rem;">SALVA TUTTO</button>
            </div>
        </div>
        <div id="zone-list"></div>
    </div>
    <div id="map"></div>
    <div id="save-status">Modifiche salvate con successo!</div>

    <script>
        let DATA_ZONE = {{JSON_ZONE}};
        let map;
        let gMarkers = [];
        let activeExpandedZid = null;
        let activeAction = null;
        let activeSourceZid = null;
        const DEPOT = { lat: 45.451912, lng: 11.736761 };

        function initMap() {
            map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: 45.5, lng: 12.0 },
                zoom: 10,
                mapTypeId: 'hybrid',
                disableDefaultUI: false,
                zoomControl: true,
                scaleControl: true
            });

            updateTotals();
            renderSidebar();
            renderMarkers();
            fitMap();
        }

        function fitMap() {
            if (gMarkers.length === 0) return;
            const bounds = new google.maps.LatLngBounds();
            gMarkers.forEach(m => bounds.extend(m.getPosition()));
            map.fitBounds(bounds);
        }

        function renderSidebar() {
            const list = document.getElementById('zone-list');
            list.innerHTML = DATA_ZONE.filter(z => z.numero_consegne > 0).map(z => {
                const isMista = z.tipologia === 'mista/frutta';
                const isSelectedZone = (activeExpandedZid === z.id_zona) || (activeSourceZid === z.id_zona);
                const hasMissing = z.da_mappare;
                
                return `
                <div class="zone-card ${isSelectedZone ? 'selected' : ''}" style="${hasMissing && !isSelectedZone ? 'border: 2px dashed #f59e0b; background: #fffbeb;' : ''}" id="card-${z.id_zona}" onclick="focusZone('${z.id_zona}')">
                    <div class="zone-header">
                        <div class="color-pill" style="background: ${z.color}"></div>
                        <div class="zone-title" style="display:flex; flex-direction:column; gap:2px;">
                            <span style="font-size:1rem; font-weight:800;">${z.nome_giro || z.nome_zona}</span>
                            <span style="font-weight:700; font-size:0.8rem; color:#475569;">${z.id_zona}</span>
                        </div>
                        <span class="badge-tipo ${isMista ? 'badge-mista' : 'badge-latte'}">${isMista ? 'Mista' : 'Latte'}</span>
                    </div>
                    <div style="font-size:0.75rem; color:#64748b; font-weight:600">
                        <span class="material-icons-round" style="font-size:12px">location_on</span> ${z.numero_consegne} Consegne
                    </div>
                    
                    ${isSelectedZone ? `
                        <div style="margin-top:10px; border-top:1px solid #e2e8f0; padding-top:10px; max-height:280px; overflow-y:auto;">
                            ${z.lista_punti.map(p => {
                                const pid = p.id || (p.codice_frutta + "_" + p.nome).replace(/[^a-zA-Z0-9]/g, '_');
                                let ctrl = '';
                                if (activeAction === 'dividi') {
                                    ctrl = `<input type="checkbox" id="chk-${pid}" class="dividi-chk" value="${pid}" onclick="event.stopPropagation()">`;
                                } else if (activeAction === 'sposta') {
                                    ctrl = `<select id="sel-${pid}" class="sposta-sel" data-pid="${pid}" onclick="event.stopPropagation();" style="width:100%; font-size:0.7rem; margin-top:4px;">
                                        <option value="">-- Mantieni qui --</option>
                                        ${DATA_ZONE.filter(o => o.id_zona !== z.id_zona).map(o => `<option value="${o.id_zona}">${o.nome_zona}</option>`).join('')}
                                    </select>`;
                                }
                                
                                return `<div style="background:${!p.lat ? '#fffbeb' : '#f1f5f9'}; padding:6px; margin-bottom:6px; border-radius:6px; border:1px solid ${!p.lat ? '#fcd34d' : '#e2e8f0'};">
                                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                        <b style="color:${!p.lat ? '#b45309' : '#334155'}; font-size:0.75rem;">${p.nome}</b>
                                        ${ctrl}
                                    </div>
                                    <div style="color:#64748b; font-size:0.7rem;">${p.indirizzo}</div>
                                    ${!p.lat ? '<div style="color:#dc2626; font-size:0.6rem; font-weight:800;">⚠️ POSIZIONE MANCANTE</div>' : ''}
                                </div>`;
                            }).join('')}
                        </div>
                        <div style="margin-top:12px; display:flex; gap:5px;">
                            ${activeAction ? `
                                <button class="btn" style="background:#ef4444; color:white;" onclick="event.stopPropagation(); cancelAction()">ANNULLA</button>
                                <button class="btn" style="background:#22c55e; color:white;" onclick="event.stopPropagation(); ${activeAction === 'dividi' ? 'executeDividi' : 'executeSposta'}('${z.id_zona}')">CONFERMA</button>
                            ` : `
                                <button class="btn" onclick="event.stopPropagation(); startAction('dividi', '${z.id_zona}')">DIVIDI</button>
                                <button class="btn" onclick="event.stopPropagation(); startAction('sposta', '${z.id_zona}')">SPOSTA</button>
                            `}
                        </div>
                    ` : ''}
                </div>`;
            }).join('');
        }

        function renderMarkers() {
            gMarkers.forEach(m => m.setMap(null));
            gMarkers = [];

            DATA_ZONE.forEach(z => {
                z.lista_punti.forEach((p, idx) => {
                    if (!p.lat || !p.lon) return;

                    const marker = new google.maps.Marker({
                        position: { lat: p.lat, lng: p.lon },
                        map: map,
                        title: p.nome,
                        draggable: true,
                        icon: {
                            path: z.tipologia === 'solo_latte' ? google.maps.SymbolPath.CIRCLE : "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z",
                            fillColor: z.color,
                            fillOpacity: 1,
                            strokeColor: '#FFFFFF',
                            strokeWeight: 2,
                            scale: z.tipologia === 'solo_latte' ? 12 : 1.5,
                            labelOrigin: new google.maps.Point(z.tipologia === 'solo_latte' ? 0 : 12, z.tipologia === 'solo_latte' ? 0 : 9)
                        },
                        label: {
                            text: (idx + 1).toString(),
                            color: 'white',
                            fontSize: '11px',
                            fontWeight: '800'
                        }
                    });

                    const infoWindow = new google.maps.InfoWindow({
                        content: `<div style="padding:10px;">
                            <div style="font-weight:800; color:${z.color}">${z.nome_giro}</div>
                            <b>${p.nome}</b><br>${p.indirizzo}<br>
                            <button onclick="window.open('https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}')" style="margin-top:10px; width:100%; padding:5px;">VEDI SU GOOGLE</button>
                            <button onclick="_salvaNuovaPosizione('${p.nome}', ${p.lat}, ${p.lon})" style="margin-top:5px; width:100%; padding:5px; background:#10b981; color:white; border:none; border-radius:4px; font-weight:700;">SALVA COORDINATE</button>
                        </div>`
                    });

                    marker.addListener("click", () => infoWindow.open(map, marker));
                    
                    marker.addListener("dragend", (e) => {
                        const newPos = e.latLng;
                        if (confirm(`Vuoi salvare la nuova posizione per ${p.nome}?`)) {
                            _salvaNuovaPosizione(p.nome, newPos.lat(), newPos.lng());
                        }
                    });

                    gMarkers.push(marker);
                });
            });
        }

        function _salvaNuovaPosizione(nome, lat, lon) {
            fetch('http://127.0.0.1:5000/save_coord', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome, lat, lon })
            }).then(r => r.json()).then(d => {
                alert(d.msg);
            }).catch(err => {
                alert("Errore di connessione al server: " + err);
            });
        }

        function startAction(type, zid) {
            activeAction = type; activeSourceZid = zid; renderSidebar();
        }

        function cancelAction() {
            activeAction = null; activeSourceZid = null; renderSidebar();
        }

        function focusZone(zid) {
            if (activeAction) return;
            activeExpandedZid = (activeExpandedZid === zid) ? null : zid;
            renderSidebar();
        }

        function updateTotals() {
            const total = DATA_ZONE.reduce((acc, z) => acc + (z.numero_consegne || 0), 0);
            document.getElementById('tot-points').textContent = `${total} Punti`;
        }

        function saveAllToServer() {
            const btn = document.getElementById('btn-master-save');
            btn.textContent = "..."; btn.disabled = true;
            fetch('http://127.0.0.1:5000/save', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(DATA_ZONE)
            }).then(() => {
                document.getElementById('save-status').style.display = 'block';
                setTimeout(() => document.getElementById('save-status').style.display = 'none', 3000);
            }).finally(() => { btn.textContent = "SALVA TUTTO"; btn.disabled = false; });
        }

        window.onload = initMap;
    </script>
</body>
</html>"""

def main():
    global TARGET_FILE_UNIFICATO, TARGET_FILE_3B, TARGET_FILE_2B, ZONE_LIST_CACHE, DATA_GIORNO
    
    if len(sys.argv) < 2:
        folders = sorted([d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")], reverse=True)
        if not folders: return print("Nessuna cartella CONSEGNE trovata.")
        DATA_GIORNO = folders[0].name.split("_")[1]
    else:
        DATA_GIORNO = sys.argv[1].strip()
    
    output_base = CONSEGNE_DIR / f"CONSEGNE_{DATA_GIORNO}"
    TARGET_FILE_UNIFICATO = output_base / "punti_consegna_unificati.json"
    TARGET_FILE_3B = output_base / "3b_assegna_ddt_zone.json"
    TARGET_FILE_2B = output_base / "2b_crea_zone_consegna.json"
    
    if not TARGET_FILE_UNIFICATO.exists():
        return print(f"File non trovato: {TARGET_FILE_UNIFICATO}")
    
    unificato_data = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
    punti_list = unificato_data.get("punti", [])
    
    # Raggruppamento Zone (logica esistente)
    zone_dict = {}
    for p in punti_list:
        zid = p.get("zona") or "SENZA_ZONA"
        if zid not in zone_dict:
            is_latte = bool(p.get("codici_ddt_latte") and not p.get("codici_ddt_frutta"))
            zone_dict[zid] = {
                "id_zona": zid, "nome_zona": f"Zona {zid}", "lista_punti": [],
                "tipologia": "solo_latte" if is_latte else "mista/frutta",
                "numero_consegne": 0, "da_mappare": False
            }
        zone_dict[zid]["lista_punti"].append(p)
        zone_dict[zid]["numero_consegne"] += 1
        if not p.get("lat"): zone_dict[zid]["da_mappare"] = True
    
    ZONE_LIST_CACHE = sorted(list(zone_dict.values()), key=lambda x: str(x["id_zona"]))
    for i, z in enumerate(ZONE_LIST_CACHE, 1):
        z["nome_giro"] = f"Viaggio {i}"
        z["color"] = _get_color(i-1)

    _salva_html_fisico(output_base, HTML_TEMPLATE, DATA_GIORNO, json.dumps(ZONE_LIST_CACHE, ensure_ascii=False), GOOGLE_MAPS_API_KEY)

    print(f"\n[INFO] Flask Server avviato per la data: {DATA_GIORNO}")
    print(f"[INFO] Apri: http://127.0.0.1:5000")
    
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:5000")

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(port=5000, debug=False)

if __name__ == "__main__":
    main()

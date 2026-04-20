import os
import sys
import threading
import webbrowser
import pandas as pd
from flask import Flask, render_template_string, jsonify, request

# Configurazione Percorsi
EXCEL_FILE = "mappatura_destinazioni.xlsx"
PORT = 5001
LOCK = threading.Lock()

app = Flask(__name__)

def find_col(columns, keywords):
    for k in keywords:
        for c in columns:
            if k.lower() in str(c).lower(): return c
    return None

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>Editor Massivo Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        :root { 
            --primary: #6366f1; --primary-dark: #4f46e5; --bg: #f8fafc; 
            --sidebar-bg: #ffffff; --text-main: #1e293b; --text-muted: #64748b;
            --accent: #10b981; --warning: #f59e0b; --danger: #ef4444;
        }
        body { margin: 0; font-family: 'Inter', sans-serif; height: 100vh; display: flex; background: var(--bg); overflow: hidden; }
        #sidebar { width: 380px; height: 100%; background: var(--sidebar-bg); border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; z-index: 1000; box-shadow: 10px 0 30px rgba(0,0,0,0.05); }
        #sidebar-header { padding: 20px; background: #1e293b; color: white; }
        .filter-group { padding: 15px 20px; border-bottom: 1px solid #f1f5f9; background: #fff; }
        .filter-group label { display: block; font-size: 0.7rem; font-weight: 800; color: var(--text-muted); margin-bottom: 5px; text-transform: uppercase; }
        select, input { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; background: #f8fafc; font-family: inherit; font-size: 0.9rem; margin-bottom: 12px; box-sizing: border-box; }
        #point-list { flex: 1; overflow-y: auto; padding: 10px; background: #f8fafc; }
        .point-item { background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; margin-bottom: 8px; cursor: pointer; transition: 0.2s; position: relative; }
        .point-item:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .point-item.modified { border-left: 5px solid var(--primary); }
        .point-item.missing { border-left: 5px solid var(--danger); }
        .point-item b { display: block; font-size: 0.85rem; color: var(--text-main); }
        .point-item span { font-size: 0.7rem; color: var(--text-muted); display: block; margin-top: 2px; }
        #map { flex: 1; position: relative; }
        #map-overlay { position: absolute; top: 20px; right: 20px; z-index: 1000; display: flex; gap: 10px; }
        .btn { padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; border: none; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
        .btn-save { background: var(--accent); color: white; }
        .btn-save:disabled { background: #cbd5e1; cursor: not-allowed; }
        .btn-unlock { background: white; color: var(--text-main); border: 1px solid #e2e8f0; }
        .btn-unlock.active { background: var(--warning); color: white; border-color: transparent; }
        .popup-info { font-size: 0.85rem; min-width: 180px; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 0.65rem; font-weight: 800; color: white; margin-top: 5px; }
    </style>
</head>
<body>

<div id="sidebar">
    <div id="sidebar-header">
        <h1 style="margin:0; font-size:1.15rem; letter-spacing:-0.5px; font-weight:800;">Logistics Bulk Editor</h1>
        <div style="font-size:0.7rem; opacity:0.8; margin-top:4px; font-weight:500;">Geolocalizzazione Master Excel</div>
    </div>
    <div class="filter-group">
        <label>Cerca Scuola / Cliente</label>
        <input type="text" id="search-box" placeholder="Scrivi nome o codice..." onkeyup="updateListAndMap()">
        <div style="display:flex; gap:10px;">
            <div style="flex:1">
                <label>Provincia</label>
                <select id="sel-prov" onchange="onProvChange()"><option value="">Tutte</option></select>
            </div>
            <div style="flex:1">
                <label>Comune</label>
                <select id="sel-comune" onchange="updateListAndMap()"><option value="">Tutti</option></select>
            </div>
        </div>
    </div>
    <div style="padding:8px 20px; font-size:0.65rem; font-weight:800; color:var(--text-muted); background:#f1f5f9; display:flex; justify-content: space-between; align-items:center;">
        <span>RISULTATI FILTRATI</span>
        <span id="stat-count" style="background:var(--primary); color:white; padding:2px 8px; border-radius:10px;">0</span>
    </div>
    <div id="point-list"></div>
</div>

<div id="map">
    <div id="map-overlay">
        <button id="btn-lock" class="btn btn-unlock" onclick="toggleLock()"><span class="material-icons-round">lock</span> SBLOCCA SPOSTAMENTO</button>
        <button id="btn-save" class="btn btn-save" onclick="saveAll()" disabled><span class="material-icons-round">save</span> SALVA TUTTO <span id="save-counter"></span></button>
    </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
    let map = L.map('map', { zoomControl: false }).setView([45.45, 11.5], 8);
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OSM' }).addTo(map);
    
    let markerLayer = L.layerGroup().addTo(map);
    let ALL_POINTS = [];
    let MODIFIED = {};
    let IS_LOCKED = true;

    const ICONS = {
        green: new L.Icon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png', shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png', iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41] }),
        red: new L.Icon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png', shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png', iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41] }),
        blue: new L.Icon({ iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png', shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png', iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41] })
    };

    fetch('/get_points').then(r => r.json()).then(data => {
        ALL_POINTS = data;
        const provs = [...new Set(data.map(p => p.prov))].filter(Boolean).sort();
        const sel = document.getElementById('sel-prov');
        provs.forEach(p => { let opt = document.createElement('option'); opt.value = p; opt.innerText = p; sel.appendChild(opt); });
        updateListAndMap();
    });

    function onProvChange() {
        const prov = document.getElementById('sel-prov').value;
        const selCom = document.getElementById('sel-comune');
        selCom.innerHTML = '<option value="">Tutti</option>';
        const comuni = [...new Set(ALL_POINTS.filter(p => !prov || p.prov === prov).map(p => p.comune))].filter(Boolean).sort();
        comuni.forEach(c => { let opt = document.createElement('option'); opt.value = c; opt.innerText = c; selCom.appendChild(opt); });
        updateListAndMap();
    }

    function updateListAndMap() {
        const prov = document.getElementById('sel-prov').value;
        const com = document.getElementById('sel-comune').value;
        const search = document.getElementById('search-box').value.toLowerCase();
        
        const filtered = ALL_POINTS.filter(p => {
            const mProv = (!prov || p.prov === prov);
            const mCom = (!com || p.comune === com);
            const mSearch = (!search || p.destinatario.toLowerCase().includes(search) || p.cod_f.toLowerCase().includes(search) || p.cod_l.toLowerCase().includes(search));
            return mProv && mCom && mSearch;
        });

        markerLayer.clearLayers();
        const listDiv = document.getElementById('point-list');
        listDiv.innerHTML = "";
        let bounds = [];

        filtered.forEach(p => {
            const isMissing = (!p.lat || p.lat == 0);
            const isModified = !!MODIFIED[p.cod_f];
            const mLat = isMissing ? 45.42 : p.lat;
            const mLng = isMissing ? 11.43 : p.lng;
            
            let icon = isMissing ? ICONS.red : (isModified ? ICONS.blue : ICONS.green);

            const m = L.marker([mLat, mLng], { icon: icon, draggable: !IS_LOCKED }).addTo(markerLayer);
            m.bindPopup(getPopupHtml(p, isMissing, isModified));
            m.on('dragend', (e) => {
                const pos = e.target.getLatLng();
                p.lat = pos.lat; p.lng = pos.lng;
                marcaModificato(p, m);
            });

            const item = document.createElement('div');
            item.className = 'point-item' + (isMissing ? ' missing':'') + (isModified ? ' modified':'');
            item.innerHTML = `<b>${p.destinatario}</b><span>${p.indirizzo} - ${p.comune} (${p.prov})</span><span style="color:var(--primary); font-weight:700; font-size:0.65rem; margin-top:4px">F: ${p.cod_f} | L: ${p.cod_l}</span>`;
            item.onclick = () => { map.setView([mLat, mLng], 16); m.openPopup(); };
            listDiv.appendChild(item);

            if(!isMissing) bounds.push([p.lat, p.lng]);
        });

        document.getElementById('stat-count').innerText = filtered.length;
        if(bounds.length > 0) map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
    }

    function getPopupHtml(p, missing, modified) {
        let bClass = missing ? 'background:var(--danger)' : (modified ? 'background:var(--primary)' : 'background:var(--accent)');
        let bText = missing ? 'COORDINATE MANCANTI' : (modified ? 'MODIFICATO (DA SALVARE)' : 'POSIZIONE SALVATA');
        return `<div class="popup-info"><div style="font-weight:800; font-size:0.95rem; margin-bottom:4px;">${p.destinatario}</div><div style="color:var(--text-muted); margin-bottom:5px;">${p.indirizzo}</div><div style="font-weight:700;">${p.comune} (${p.prov})</div><hr style="margin:8px 0; border:0; border-top:1px solid #eee"><div style="font-size:0.75rem">F: <b>${p.cod_f}</b> | L: <b>${p.cod_l}</b></div><div class="badge" style="${bClass}">${bText}</div></div>`;
    }

    function toggleLock() {
        IS_LOCKED = !IS_LOCKED;
        const btn = document.getElementById('btn-lock');
        btn.innerHTML = IS_LOCKED ? '<span class="material-icons-round">lock</span> SBLOCCA SPOSTAMENTO' : '<span class="material-icons-round">lock_open</span> BLOCCA SPOSTAMENTO';
        btn.classList.toggle('active', !IS_LOCKED);
        updateListAndMap();
    }

    function marcaModificato(p, m) {
        MODIFIED[p.cod_f] = { id: p.cod_f, lat: p.lat, lng: p.lng };
        m.setIcon(ICONS.blue);
        m.setPopupContent(getPopupHtml(p, false, true));
        document.getElementById('btn-save').disabled = false;
        document.getElementById('save-counter').innerText = `(${Object.keys(MODIFIED).length})`;
    }

    function saveAll() {
        const btn = document.getElementById('btn-save');
        btn.disabled = true; btn.innerText = "Salvataggio...";
        fetch('/save_all', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.values(MODIFIED)) }).then(r => r.json()).then(res => {
            if(res.status === 'success') { alert("Excel Master aggiornato correttamente!"); location.reload(); }
            else { alert("Errore: " + res.error); btn.disabled = false; }
        });
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_points')
def get_points():
    with LOCK:
        df = pd.read_excel(EXCEL_FILE)
        cols = {
            'cod_f': find_col(df.columns, ['Codice Frutta', 'Cod_F', 'Frutta']),
            'cod_l': find_col(df.columns, ['Codice Latte', 'Cod_L', 'Latte']),
            'destinatario': find_col(df.columns, ['consegnato', 'Destinatario', 'Nome']),
            'indirizzo': find_col(df.columns, ['Indirizzo']),
            'comune': find_col(df.columns, ['Citt', 'Comune']),
            'prov': find_col(df.columns, ['Prov']),
            'lat': find_col(df.columns, ['Latitudine', 'Lat']),
            'lng': find_col(df.columns, ['Longitudine', 'Lng'])
        }
        
        points = []
        for _, row in df.iterrows():
            points.append({
                'cod_f': str(row[cols['cod_f']]),
                'cod_l': str(row[cols['cod_l']]),
                'destinatario': str(row[cols['destinatario']]),
                'indirizzo': str(row[cols['indirizzo']]),
                'comune': str(row[cols['comune']]),
                'prov': str(row[cols['prov']]),
                'lat': float(row[cols['lat']]) if pd.notnull(row[cols['lat']]) else 0,
                'lng': float(row[cols['lng']]) if pd.notnull(row[cols['lng']]) else 0
            })
        return jsonify(points)

@app.route('/save_all', methods=['POST'])
def save_all():
    items = request.json
    with LOCK:
        df = pd.read_excel(EXCEL_FILE)
        col_id = find_col(df.columns, ['Codice Frutta', 'Cod_F', 'Frutta'])
        col_lat = find_col(df.columns, ['Latitudine', 'Lat'])
        col_lng = find_col(df.columns, ['Longitudine', 'Lng'])
        col_status = find_col(df.columns, ['Stato geocoding'])

        for item in items:
            mask = df[col_id].astype(str) == str(item['id'])
            if mask.any():
                df.loc[mask, col_lat] = item['lat']
                df.loc[mask, col_lng] = item['lng']
                if col_status:
                    df.loc[mask, col_status] = 'ok'
        
        df.to_excel(EXCEL_FILE, index=False)
        return jsonify({'status': 'success'})

if __name__ == '__main__':
    def open_browser():
        webbrowser.open(f'http://127.0.0.1:{PORT}')
    
    threading.Timer(1.5, open_browser).start()
    app.run(port=PORT, debug=False)

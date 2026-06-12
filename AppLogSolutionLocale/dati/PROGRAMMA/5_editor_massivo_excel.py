import os
import sys
import threading
import webbrowser
import pandas as pd
from flask import Flask, render_template_string, jsonify, request

# Configurazione Percorsi
EXCEL_FILE = "mappatura_destinazioni.xlsx"
PORT = 5002
LOCK = threading.Lock()
# API KEY (la stessa usata in 4_mappa_zone_google.py)
from pathlib import Path
import os as _os
def _carica_env():
    _p = Path(__file__).resolve().parent / '.env'
    if _p.exists():
        for _l in _p.read_text(encoding='utf-8').splitlines():
            _l = _l.strip()
            if _l and not _l.startswith('#') and '=' in _l:
                _k, _v = _l.split('=', 1)
                _os.environ.setdefault(_k.strip(), _v.strip())
_carica_env()
GOOGLE_MAPS_API_KEY = _os.environ.get('GOOGLE_MAPS_API_KEY', '')
app = Flask(__name__)

def find_col(columns, keywords):
    for k in keywords:
        for c in columns:
            if k.lower() in str(c).lower(): return c
    return None

# --- HTML TEMPLATE ESCLUSIVO GOOGLE MAPS ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>Editor Massivo Pro (Google Maps Native)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
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
        .point-item.modified { border-left: 5px solid var(--warning); }
        .point-item.missing { border-left: 5px solid var(--danger); }
        .point-item.verified { border-left: 5px solid var(--primary); }
        .point-item.unverified { border-left: 5px solid var(--accent); }
        .point-item b { display: block; font-size: 0.85rem; color: var(--text-main); }
        .point-item span { font-size: 0.7rem; color: var(--text-muted); display: block; margin-top: 2px; }
        #map { flex: 1; position: relative; }
        #map-overlay { position: absolute; top: 20px; right: 20px; z-index: 5000; display: flex; gap: 10px; }
        .btn { padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; border: none; display: flex; align-items: center; gap: 8px; font-size: 0.85rem; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
        .btn-save { background: var(--accent); color: white; }
        .btn-save:disabled { background: #cbd5e1; cursor: not-allowed; }
        .btn-unlock { background: white; color: var(--text-main); border: 1px solid #e2e8f0; }
        .btn-unlock.active { background: var(--warning); color: white; border-color: transparent; }
        .popup-info { font-size: 0.85rem; min-width: 180px; color: #334155; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 0.65rem; font-weight: 800; color: white; margin-top: 5px; }
    </style>
    <!-- GOOGLE MAPS API LOADER -->
    <script>
        (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. See https://goo.gle/js-api-loading-troubleshooting"):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
            key: "{{GOOGLE_MAPS_API_KEY}}",
            v: "beta"
        });
    </script>
</head>
<body>

<div id="sidebar">
    <div id="sidebar-header">
        <h1 style="margin:0; font-size:1.15rem; letter-spacing:-0.5px; font-weight:800;">Logistics Bulk Editor</h1>
        <div style="font-size:0.7rem; opacity:0.8; margin-top:4px; font-weight:500;">Geolocalizzazione Master Native Maps</div>
    </div>
    <div class="filter-group">
        <label>Società / Canale</label>
        <select id="sel-societa" onchange="updateProvinceOptions()">
            <option value="">Tutti i clienti (DNR + Grand Chef)</option>
            <option value="DNR">DNR (Scuole)</option>
            <option value="GRAND_CHEF">Grand Chef (Ristoranti/Hotel)</option>
        </select>
        <label>Cerca (es: "rossi" o "mancanti")</label>
        <input type="text" id="search-box" placeholder="Scrivi qui..." onkeyup="updateListAndMap()">
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

<div id="map"></div>
<div id="map-overlay">
    <button id="btn-lock" class="btn btn-unlock" onclick="toggleLock()"><span class="material-icons-round">lock</span> SBLOCCA SPOSTAMENTO</button>
    <button id="btn-save" class="btn btn-save" onclick="saveAll()" disabled><span class="material-icons-round">save</span> SALVA TUTTO <span id="save-counter"></span></button>
</div>

<script>
    let map;
    let ALL_POINTS = [];
    let MODIFIED = {};
    let IS_LOCKED = true;
    let gMarkers = [];
    let infoWindow;

    async function initMap() {
        const { InfoWindow } = await google.maps.importLibrary("maps");
        infoWindow = new google.maps.InfoWindow();
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 45.42, lng: 11.43 },
            zoom: 10,
            mapTypeId: 'hybrid',
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: false
        });
        map.setMapTypeId('hybrid');

        fetch('/get_points').then(r => r.json()).then(data => {
            ALL_POINTS = data;
            updateProvinceOptions();
            
            // Auto fit
            const bounds = new google.maps.LatLngBounds();
            let hasCoord = false;
            data.forEach(p => { if(p.lat && p.lat !== 0) { bounds.extend({lat: p.lat, lng: p.lng}); hasCoord = true; } });
            if(hasCoord) map.fitBounds(bounds);
        });
    }

    function updateProvinceOptions() {
        const soc = document.getElementById('sel-societa').value;
        const selProv = document.getElementById('sel-prov');
        const prevVal = selProv.value;
        
        // Filtra i punti in base alla società per estrarre le province disponibili
        const filteredPointsForProv = ALL_POINTS.filter(p => {
            if (soc === 'DNR') return p.tipologia !== 'GRAND CHEF';
            if (soc === 'GRAND_CHEF') return p.tipologia === 'GRAND CHEF';
            return true;
        });
        
        const provs = [...new Set(filteredPointsForProv.map(p => p.prov))].filter(Boolean).sort();
        
        selProv.innerHTML = '<option value="">Tutte</option>';
        provs.forEach(p => {
            let opt = document.createElement('option');
            opt.value = p;
            opt.innerText = p;
            if (p === prevVal) opt.selected = true;
            selProv.appendChild(opt);
        });
        
        if (!provs.includes(prevVal)) {
            selProv.value = "";
        }
        
        onProvChange();
    }

    function onProvChange() {
        const soc = document.getElementById('sel-societa').value;
        const prov = document.getElementById('sel-prov').value;
        const selCom = document.getElementById('sel-comune');
        const prevVal = selCom.value;

        const filteredPointsForComuni = ALL_POINTS.filter(p => {
            let mSoc = true;
            if (soc === 'DNR') mSoc = (p.tipologia !== 'GRAND CHEF');
            else if (soc === 'GRAND_CHEF') mSoc = (p.tipologia === 'GRAND CHEF');
            
            const mProv = (!prov || p.prov === prov);
            return mSoc && mProv;
        });

        const comuni = [...new Set(filteredPointsForComuni.map(p => p.comune))].filter(Boolean).sort();
        
        selCom.innerHTML = '<option value="">Tutti</option>';
        comuni.forEach(c => {
            let opt = document.createElement('option');
            opt.value = c;
            opt.innerText = c;
            if (c === prevVal) opt.selected = true;
            selCom.appendChild(opt);
        });

        if (!comuni.includes(prevVal)) {
            selCom.value = "";
        }

        updateListAndMap();
    }

    async function updateListAndMap() {
        const soc = document.getElementById('sel-societa').value;
        const prov = document.getElementById('sel-prov').value;
        const com = document.getElementById('sel-comune').value;
        const searchInput = document.getElementById('search-box').value.toLowerCase();
        
        const filtered = ALL_POINTS.filter(p => {
            // Filtro Società
            let mSoc = true;
            if (soc === 'DNR') {
                mSoc = (p.tipologia !== 'GRAND CHEF');
            } else if (soc === 'GRAND_CHEF') {
                mSoc = (p.tipologia === 'GRAND CHEF');
            }
            if (!mSoc) return false;

            const mProv = (!prov || p.prov === prov);
            const mCom = (!com || p.comune === com);
            const isRossiSearch = searchInput === 'rossi' || searchInput === 'mancanti';
            if (isRossiSearch) return p.is_missing && mProv && mCom;
            const mSearch = (!searchInput || p.destinatario.toLowerCase().includes(searchInput) || p.cod_f.toLowerCase().includes(searchInput) || p.cod_l.toLowerCase().includes(searchInput));
            return mProv && mCom && mSearch;
        });

        // Pulisci marker
        gMarkers.forEach(m => m.setMap(null));
        gMarkers = [];

        const listDiv = document.getElementById('point-list');
        listDiv.innerHTML = "";
        
        filtered.forEach(p => {
            const isMissing = p.is_missing;
            const isVerified = (p.stato === 'ok');
            const isModified = !!MODIFIED[p.cod_f + '_' + p.cod_l + '_' + p.destinatario];
            const mLat = (p.lat === 0) ? 45.42 : p.lat;
            const mLng = (p.lng === 0) ? 11.43 : p.lng;
            
            let iconUrl;
            if (p.tipologia === 'GRAND CHEF') {
                let pinColor = isMissing ? '#ef4444' : ((isVerified || isModified) ? '#4f46e5' : '#0284c7');
                const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="34" height="38" viewBox="0 0 38 42">
                  <path d="M19 0C8.5 0 0 8.5 0 19c0 13 19 23 19 23s19-10 19-23c0-10.5-8.5-19-19-19z" fill="${pinColor}" stroke="white" stroke-width="2"/>
                  <g transform="translate(9, 7) scale(0.85)" fill="white">
                    <path d="M16 6v8h3v8h2V6h-5z M11 9H9V6H7v3H5V6H3v3c0 2.44 1.72 4.47 4 4.9v7.1h2v-7.1c2.28-.43 4-2.46 4-4.9V6h-2v3z"/>
                  </g>
                </svg>`;
                iconUrl = 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg);
            } else {
                let color = isMissing ? 'red' : ((isVerified || isModified) ? 'blue' : 'green');
                iconUrl = `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`;
            }

            const m = new google.maps.Marker({
                position: { lat: mLat, lng: mLng },
                map: map,
                title: p.destinatario,
                icon: iconUrl,
                draggable: !IS_LOCKED
            });

            m.addListener('click', () => {
                infoWindow.setContent(getPopupHtml(p, isMissing, isVerified, isModified));
                infoWindow.open(map, m);
            });

            m.addListener('dragend', () => {
                const pos = m.getPosition();
                p.lat = pos.lat(); p.lng = pos.lng();
                marcaModificato(p, m);
            });

            gMarkers.push(m);

            const item = document.createElement('div');
            let statusClass = ' unverified';
            if (isMissing) statusClass = ' missing';
            else if (isModified) statusClass = ' modified';
            else if (isVerified) statusClass = ' verified';
            
            item.className = 'point-item' + statusClass;
            
            let socBadge = p.tipologia === 'GRAND CHEF' ? '<span style="background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-size:0.55rem; font-weight:800; float:right">GRAND CHEF</span>' : '';
            item.innerHTML = `${socBadge}<b>${p.destinatario}</b><span>${p.indirizzo} - ${p.comune} (${p.prov})</span><span style="color:var(--primary); font-weight:700; font-size:0.65rem; margin-top:4px">F: ${p.cod_f} | L: ${p.cod_l}</span>`;
            item.onclick = () => { map.setCenter(m.getPosition()); map.setZoom(18); google.maps.event.trigger(m, 'click'); };
            listDiv.appendChild(item);
        });

        document.getElementById('stat-count').innerText = filtered.length;
    }

    function getPopupHtml(p, missing, verified, modified) {
        let bClass = 'background:var(--accent)';
        let bText = 'NON VERIFICATO';
        
        if (missing) {
            bClass = 'background:var(--danger)';
            bText = `MANCANTE (${p.stato || 'not_found'})`;
        } else if (modified) {
            bClass = 'background:var(--warning)';
            bText = 'MODIFICATO';
        } else if (verified) {
            bClass = 'background:var(--primary)';
            bText = 'VERIFICATO (OK)';
        }
        
        let tipologiaHtml = p.tipologia ? `<div style="font-size:0.65rem; color:#0369a1; font-weight:800; margin-bottom:4px;">CANALE: ${p.tipologia}</div>` : '';
        
        return `
            <div class="popup-info">
                ${tipologiaHtml}
                <div style="font-weight:800; font-size:0.95rem; margin-bottom:4px;">${p.destinatario}</div>
                <div style="color:var(--text-muted); margin-bottom:5px;">${p.indirizzo}</div>
                <div style="font-weight:700;">${p.comune} (${p.prov})</div>
                <hr style="margin:8px 0; border:0; border-top:1px solid #eee">
                <div style="font-size:0.75rem">F: <b>${p.cod_f}</b> | L: <b>${p.cod_l}</b></div>
                <div class="badge" style="${bClass}">${bText}</div>
            </div>`;
    }

    function toggleLock() {
        IS_LOCKED = !IS_LOCKED;
        const btn = document.getElementById('btn-lock');
        btn.innerHTML = IS_LOCKED ? '<span class="material-icons-round">lock</span> SBLOCCA SPOSTAMENTO' : '<span class="material-icons-round">lock_open</span> BLOCCA SPOSTAMENTO';
        btn.classList.toggle('active', !IS_LOCKED);
        gMarkers.forEach(m => m.setDraggable(!IS_LOCKED));
    }

    function marcaModificato(p, m) {
        let unique_id = p.cod_f + '_' + p.cod_l + '_' + p.destinatario;
        MODIFIED[unique_id] = { cod_f: p.cod_f, cod_l: p.cod_l, dest: p.destinatario, lat: p.lat, lng: p.lng };
        
        if (p.tipologia === 'GRAND CHEF') {
            const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="34" height="38" viewBox="0 0 38 42">
              <path d="M19 0C8.5 0 0 8.5 0 19c0 13 19 23 19 23s19-10 19-23c0-10.5-8.5-19-19-19z" fill="#4f46e5" stroke="white" stroke-width="2"/>
              <g transform="translate(9, 7) scale(0.85)" fill="white">
                <path d="M16 6v8h3v8h2V6h-5z M11 9H9V6H7v3H5V6H3v3c0 2.44 1.72 4.47 4 4.9v7.1h2v-7.1c2.28-.43 4-2.46 4-4.9V6h-2v3z"/>
              </g>
            </svg>`;
            m.setIcon('data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg));
        } else {
            m.setIcon(`https://maps.google.com/mapfiles/ms/icons/blue-dot.png`);
        }
        
        document.getElementById('btn-save').disabled = false;
        document.getElementById('save-counter').innerText = `(${Object.keys(MODIFIED).length})`;
    }

    function saveAll() {
        const btn = document.getElementById('btn-save');
        btn.disabled = true; btn.innerText = "Salvataggio...";
        fetch('/save_all', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.values(MODIFIED)) }).then(r => r.json()).then(res => {
            if(res.status === 'success') { alert("Dati salvati su Excel Master!"); location.reload(); }
            else { alert("Errore: " + res.error); btn.disabled = false; }
        });
    }

    window.onload = initMap;
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)

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
            'lng': find_col(df.columns, ['Longitudine', 'Lng']),
            'stato': find_col(df.columns, ['Stato geocoding', 'Geocoding', 'Stato']),
            'tipologia': find_col(df.columns, ['Tipologia grado', 'Grado', 'Tipologia'])
        }
        
        points = []
        missing_count = 0
        for _, row in df.iterrows():
            st = str(row[cols['stato']]).lower().strip() if pd.notnull(row[cols['stato']]) else ''
            lt = float(row[cols['lat']]) if pd.notnull(row[cols['lat']]) else 0
            lg = float(row[cols['lng']]) if pd.notnull(row[cols['lng']]) else 0
            
            is_missing = (lt == 0 or lg == 0 or st != 'ok')
            if is_missing: missing_count += 1
            
            points.append({
                'cod_f': str(row[cols['cod_f']]),
                'cod_l': str(row[cols['cod_l']]),
                'destinatario': str(row[cols['destinatario']]),
                'indirizzo': str(row[cols['indirizzo']]),
                'comune': str(row[cols['comune']]),
                'prov': str(row[cols['prov']]),
                'lat': lt,
                'lng': lg,
                'stato': st,
                'is_missing': is_missing,
                'tipologia': str(row[cols['tipologia']]).strip() if pd.notnull(row[cols['tipologia']]) else ''
            })
        print(f"DEBUG: Inviati {len(points)} punti (di cui {missing_count} rossi/non verificati)")
        return jsonify(points)

@app.route('/save_all', methods=['POST'])
def save_all():
    items = request.json
    with LOCK:
        try:
            df = pd.read_excel(EXCEL_FILE)
            col_id_f = find_col(df.columns, ['Codice Frutta', 'Cod_F', 'Frutta'])
            col_id_l = find_col(df.columns, ['Codice Latte', 'Cod_L', 'Latte'])
            col_dest = find_col(df.columns, ['consegnato', 'Destinatario', 'Nome'])
            col_lat = find_col(df.columns, ['Latitudine', 'Lat'])
            col_lng = find_col(df.columns, ['Longitudine', 'Lng'])
            col_status = find_col(df.columns, ['Stato geocoding'])

            for item in items:
                mask_f = df[col_id_f].astype(str).str.strip().str.lower() == str(item['cod_f']).strip().lower()
                mask_l = df[col_id_l].astype(str).str.strip().str.lower() == str(item['cod_l']).strip().lower()
                mask_d = df[col_dest].astype(str).str.strip().str.lower() == str(item['dest']).strip().lower()
                mask = mask_f & mask_l & mask_d
                
                if mask.any():
                    df.loc[mask, col_lat] = item['lat']
                    df.loc[mask, col_lng] = item['lng']
                    if col_status:
                        df.loc[mask, col_status] = 'ok'
            
            df.to_excel(EXCEL_FILE, index=False)
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'error': str(e)})

if __name__ == '__main__':
    print("\n" + "="*40)
    print(">>> EDITOR GOOGLE MAPS NATIVE LOADED <<<")
    print(f"File Excel: {EXCEL_FILE}")
    print("Mappa: Satellite Hybrid (Original Google)")
    print("="*40 + "\n")
    
    def open_browser():
        webbrowser.open(f'http://127.0.0.1:{PORT}')
    
    threading.Timer(1.5, open_browser).start()
    app.run(port=PORT, debug=False)

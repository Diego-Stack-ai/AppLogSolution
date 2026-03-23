#!/usr/bin/env python3
"""
4b_crea_mappa_zone_interattiva.py (V3.1 - Opzione B: UI Migliorata & Sidebar Context)
1. Genera la mappa con selezione marker integrata nella sidebar.
2. Avvia un server locale per ricevere aggiornamenti (Dividi/Sposta).
3. Sovrascrive i file JSON originali (2b e 3b).
"""

import json
import sys
import re
import http.server
import socketserver
import threading
import webbrowser
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"

PORT = 8080
TARGET_FILE_UNIFICATO = None
TARGET_FILE_3B = None
TARGET_FILE_2B = None
GEOCODE_CACHE = BASE_DIR / "geocode_cache.json"

def _geocode(query: str, cache: dict, geo) -> tuple[float | None, float | None]:
    if not query or not str(query).strip(): return (None, None)
    key = " ".join(str(query).lower().split())
    if key in cache:
        c = cache[key]
        lat, lon = c.get("lat"), c.get("lon")
        if lat is not None and lon is not None: return (float(lat), float(lon))
        return (None, None)
    try:
        time.sleep(1.1)
        loc = geo.geocode(query, timeout=10, exactly_one=True)
        if loc:
            cache[key] = {"lat": loc.latitude, "lon": loc.longitude, "status": "ok"}
            return (loc.latitude, loc.longitude)
    except Exception:
        pass
    cache[key] = {"lat": None, "lon": None, "status": "not_found"}
    return (None, None)

def _geocode_photon(query: str, cache: dict) -> tuple[float | None, float | None]:
    if not query or not str(query).strip(): return (None, None)
    q_clean = " ".join(str(query).split()) + " Italia"
    key = "photon:" + " ".join(q_clean.lower().split())
    if key in cache:
        c = cache[key]
        lat, lon = c.get("lat"), c.get("lon")
        if lat is not None and lon is not None: return (float(lat), float(lon))
        return (None, None)
    try:
        url = "https://photon.komoot.io/api/?q=" + urllib.parse.quote(q_clean) + "&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "GestioneDDTViaggi/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        features = data.get("features", [])
        if features:
            coords = features[0].get("geometry", {}).get("coordinates", [])
            if len(coords) >= 2:
                lon, lat = float(coords[0]), float(coords[1])
                cache[key] = {"lat": lat, "lon": lon, "status": "photon"}
                return (lat, lon)
    except Exception:
        pass
    cache[key] = {"lat": None, "lon": None, "status": "not_found"}
    return (None, None)

def _get_color(idx):
    palette = [
        "#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", 
        "#ec4899", "#06b6d4", "#f97316", "#14b8a6", "#6366f1",
        "#a855f7", "#3b82f6", "#22c55e", "#d946ef", "#84cc16"
    ]
    return palette[idx % len(palette)]

class SaveHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # 1. Aggiorna il file unificato (cambio zona ai singoli punti)
                if TARGET_FILE_UNIFICATO:
                    unificato_raw = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
                    punti_flat = unificato_raw.get("punti", [])
                    
                    # Crea mappa rapida per aggiornare zone
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
                
                # 2. Salva 3b (Dati arricchiti) per retro-compatibilità
                if TARGET_FILE_3B:
                    TARGET_FILE_3B.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                
                # 3. Ricostruisci e salva 2b
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

                self.wfile.write(json.dumps({"status": "ok"}).encode())
                print(f"\n[SERVER] Modifiche salvate in {TARGET_FILE_UNIFICATO.name}")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                print(f"[SERVER] Errore nel salvataggio: {e}")

        elif self.path == '/save_coord':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8')) # {nome, lat, lon}
            
            _aggiorna_mappatura_destinazioni(payload['nome'], payload['lat'], payload['lon'])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "msg": "Coordinata salvata in mappatura_destinazioni.xlsx"}).encode())

    def do_OPTIONS(self): # Per CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def _aggiorna_mappatura_destinazioni(nome, lat, lon):
    try:
        import pandas as pd
        file_path = BASE_DIR / "mappatura_destinazioni.xlsx"
        if not file_path.exists(): 
            print(f"[ERR] File non trovato: {file_path}")
            return
        
        df = pd.read_excel(file_path)
        # Cerchiamo per nome (case insensitive)
        mask = df['nome'].astype(str).str.lower() == str(nome).lower()
        if mask.any():
            df.loc[mask, 'latitudine'] = lat
            df.loc[mask, 'longitudine'] = lon
            df.to_excel(file_path, index=False)
            print(f"[FIX] Coordinate salvate permanentemente per: {nome}")
        else:
            print(f"[WARN] Impossibile trovare '{nome}' nel file Excel")
    except Exception as e:
        print(f"Errore aggiornamento Excel: {e}")

def _salva_html_zone(zone_list: list, output_path: Path, data: str):
    for i, z in enumerate(zone_list):
        if "color" not in z: z["color"] = _get_color(i)

    zone_js = json.dumps(zone_list, ensure_ascii=False)
    
    html_template = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <title>Gestione Zone {{DATA_GIORNO}}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
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
        .zone-actions { display: flex; gap: 5px; margin-top: 10px; border-top: 1px solid #f1f5f9; padding-top: 8px; }
        .btn { flex: 1; padding: 6px; font-size: 0.7rem; font-weight: 800; border: 1px solid #e2e8f0; background: white; border-radius: 6px; cursor: pointer; color: #64748b; }
        .btn:hover { background: #f1f5f9; }
        .btn.active { background: var(--primary); color: white; border-color: var(--primary); }
        #map { flex: 1; z-index: 1; }
        
        /* NUOVO BOX AZIONI */
        .action-box { background: #4f46e5; color: white; border-radius: 8px; padding: 10px; margin-top: 10px; font-size: 0.8rem; display: flex; flex-direction: column; gap: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .action-box b { color: #facc15; }

        /* ICONE */
        .marker-base { width: 30px; height: 30px; display: flex !important; align-items:center; justify-content:center; color:white; font-weight:800; font-size:9px; box-shadow:0 3px 6px rgba(0,0,0,0.3); border:2px solid white; transition: 0.3s; }
        .marker-selected { border: 3px solid #facc15 !important; transform: scale(1.25); box-shadow: 0 0 15px #facc15; z-index: 1000 !important; }
        .marker-goccia { border-radius: 50% 50% 50% 0; transform: rotate(-45deg); }
        .marker-goccia span { transform: rotate(45deg); display: block; width: 100%; text-align: center; }
        .marker-tonda { border-radius: 50%; border-width: 3px; }
        .marker-foglia { border-radius: 12px 2px 12px 2px; transform: rotate(45deg); }
        .marker-foglia span { transform: rotate(-45deg); }

        .badge-tipo { padding: 3px 6px; font-size: 0.6rem; border-radius: 4px; text-transform: uppercase; font-weight: 800; }
        .badge-mista { background: #fef3c7; color: #92400e; }
        .badge-latte { background: #dcfce7; color: #166534; }
        
        #save-status { position: fixed; bottom: 20px; left: 400px; padding: 10px 20px; border-radius: 30px; background: #10b981; color: white; font-weight: 700; display: none; z-index: 3000; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    </style>
</head>
<body>
    <div id="sidebar">
        <div id="header">
            <h1>
                Gestione Zone
                <span id="tot-points" style="font-size:0.8rem; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-weight: 400;">0 Punti</span>
            </h1>
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
        let markers = [];
        let selectedPoints = [];
        let activeAction = null;
        let activeSourceZid = null;
        let activeExpandedZid = null;
        const DEPOT = "11.736761,45.451912"; // Via Alessandro Volta 25, Veggiano


        const map = L.map('map', { zoomControl: false }).setView([45.5, 12.0], 10);
        L.control.zoom({ position: 'bottomright' }).addTo(map);
        
        L.tileLayer('http://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
            maxZoom: 20, subdomains:['mt0','mt1','mt2','mt3'], attribution: '© Google Maps'
        }).addTo(map);
        
        function init() {
            updateTotals();
            renderSidebar();
            renderMarkers();
            if (markers.length > 0) {
                const group = new L.featureGroup(markers.map(m => m.layer));
                map.fitBounds(group.getBounds().pad(0.1));
            }
            fetchZoneRoutes();
        }

        async function fetchZoneRoutes() {
            for (const z of DATA_ZONE.filter(o => o.numero_consegne > 0)) {
                if (z._statsHtml) continue;
                const el = document.getElementById("route-stats-" + z.id_zona);
                const coords = [DEPOT];
                z.lista_punti.forEach(p => { if (p.lat && p.lon) coords.push(`${p.lon},${p.lat}`); });
                
                try {
                    const url = `http://router.project-osrm.org/trip/v1/driving/${coords.join(';')}?roundtrip=true&source=first&overview=false`;
                    const res = await fetch(url);
                    const data = await res.json();
                    if (data.code === "Ok" && data.trips && data.trips.length > 0) {
                        const distKm = (data.trips[0].distance / 1000).toFixed(1);
                        const routeMin = Math.round(data.trips[0].duration / 60);
                        const dropMin = z.numero_consegne * 10;
                        const totalMin = routeMin + dropMin;
                        const ore = Math.floor(totalMin / 60);
                        const min = totalMin % 60;
                        const dr = ore > 0 ? `${ore}h ${min}m` : `${min}m`;
                        z._statsHtml = `<span class="material-icons-round" style="font-size:11px; vertical-align:middle">route</span> <span style="color:#059669">${distKm} km</span> / <span style="color:#2563eb">${dr}</span> <span style="font-weight:400; color:#64748b; font-size:0.6rem;">(${dropMin}m scarichi)</span>`;
                    } else {
                        z._statsHtml = "Errore rotte OSRM";
                    }
                } catch (e) {
                    z._statsHtml = "Offline / API Error";
                }
                if (el) el.innerHTML = z._statsHtml;
                await new Promise(r => setTimeout(r, 600)); // Respect public API limit
            }
        }

        function updateTotals() {
            const total = DATA_ZONE.reduce((acc, z) => acc + (z.numero_consegne || 0), 0);
            document.getElementById('tot-points').textContent = `${total} Punti Totali`;
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
                    <div id="route-stats-${z.id_zona}" style="font-size:0.7rem; color:#f59e0b; font-weight:700; margin-top:3px;">
                        ${z._statsHtml ? z._statsHtml : '<span class="material-icons-round" style="font-size:11px; vertical-align:middle">route</span> Calcolo percorso in corso...'}
                    </div>
                    
                    ${isSelectedZone ? `
                        <div style="margin-top:10px; border-top:1px solid #e2e8f0; padding-top:10px; max-height:280px; overflow-y:auto;">
                            ${z.lista_punti.map(p => {
                                const pid = p.id || (p.codice_frutta + "_" + p.nome).replace(/[^a-zA-Z0-9]/g, '_');
                                let ctrl = '';
                                if (activeAction === 'dividi') {
                                    ctrl = `<input type="checkbox" style="transform: scale(1.3);" id="chk-${pid}" class="dividi-chk" value="${pid}" onclick="event.stopPropagation()">`;
                                } else if (activeAction === 'sposta') {
                                    ctrl = `<select id="sel-${pid}" class="sposta-sel" data-pid="${pid}" onclick="event.stopPropagation();" onchange="event.stopPropagation();" style="width:100%; font-size:0.7rem; margin-top:4px; padding:3px; border-radius:4px;">
                                        <option value="">-- Mantieni qui --</option>
                                        ${DATA_ZONE.filter(o => o.id_zona !== z.id_zona).map(o => `<option value="${o.id_zona}">${o.nome_zona}</option>`).join('')}
                                    </select>`;
                                }
                                
                                return `<div style="background:${!p.lat ? '#fffbeb' : '#f1f5f9'}; padding:6px; margin-bottom:6px; border-radius:6px; border:1px solid ${!p.lat ? '#fcd34d' : '#e2e8f0'}; position:relative;">` +
                                    '<div style="display:flex; justify-content:space-between; align-items:flex-start;">' +
                                        `<b style="color:${!p.lat ? '#b45309' : '#334155'}; font-size:0.75rem;">` + p.nome + '</b>' +
                                        (activeAction === 'dividi' ? ctrl : '') +
                                    '</div>' +
                                    '<div style="color:#64748b; font-size:0.7rem; margin-bottom:2px;">' + p.indirizzo + '</div>' +
                                    (!p.lat ? '<div style="color:#dc2626; font-size:0.6rem; font-weight:800; text-transform:uppercase;">⚠️ POSIZIONE MANCANTE</div>' : '') +
                                    (activeAction === 'sposta' ? ctrl : '') +
                                '</div>';
                            }).join('')}
                        </div>
                        
                        <div style="margin-top:12px;">
                            ${activeAction === 'dividi' ? `
                                <div style="display:flex; gap:5px;">
                                    <button class="btn" onclick="event.stopPropagation(); cancelAction()" style="background:#ef4444; color:white; border:none;">ANNULLA</button>
                                    <button class="btn" onclick="event.stopPropagation(); executeDividi('${z.id_zona}')" style="background:#22c55e; color:white; border:none;">CREA NUOVA ZONA</button>
                                </div>
                            ` : activeAction === 'sposta' ? `
                                <div style="display:flex; gap:5px;">
                                    <button class="btn" onclick="event.stopPropagation(); cancelAction()" style="background:#ef4444; color:white; border:none;">ANNULLA</button>
                                    <button class="btn" onclick="event.stopPropagation(); executeSposta('${z.id_zona}')" style="background:#22c55e; color:white; border:none;">CONFERMA SPOSTAMENTI</button>
                                </div>
                            ` : `
                                <div style="display:flex; gap:5px;">
                                    <button class="btn" onclick="event.stopPropagation(); startAction('dividi', '${z.id_zona}')">DIVIDI</button>
                                    <button class="btn" onclick="event.stopPropagation(); startAction('sposta', '${z.id_zona}')">SPOSTA</button>
                                </div>
                            `}
                        </div>
                    ` : ''}
                </div>
            `;}).join('');
        }

        function renderMarkers() {
            markers.forEach(m => map.removeLayer(m.layer));
            markers = [];
            
            DATA_ZONE.filter(z => z.numero_consegne > 0).forEach(z => {
                z.lista_punti.forEach(p => {
                    if (!p.lat || !p.lon) return;
                    
                    let classeIcona = 'marker-goccia';
                    const hasDelivery = (p.codici_ddt_frutta && p.codici_ddt_frutta.length > 0) || (p.codici_ddt_latte && p.codici_ddt_latte.length > 0);
                    const hasPickup = p.rientri_alert && p.rientri_alert.length > 0;
                    if (hasDelivery && hasPickup) classeIcona = 'marker-tonda';
                    else if (!hasDelivery && hasPickup) classeIcona = 'marker-foglia';

                    const pointId = p.id || (p.codice_frutta + "_" + p.nome).replace(/[^a-zA-Z0-9]/g, '_');
                    const iconHtml = `<div class="marker-base ${classeIcona}" id="marker-${pointId}" style="background: ${z.color}"><span>${z.id_zona}</span></div>`;
                    const icon = L.divIcon({ className: '', html: iconHtml, iconSize: [30, 30], iconAnchor: [15, 15] });

                    const m = L.marker([p.lat, p.lon], { icon, draggable: true }).addTo(map);
                    
                    const popupContent = `
                        <div style="font-family:sans-serif; min-width:180px;">
                            <div style="font-size:0.75rem; font-weight:800; color:#4f46e5; text-transform:uppercase; margin-bottom:2px;">${z.nome_giro} (${z.id_zona})</div>
                            <b style="font-size:0.9rem;">${p.nome}</b><br>
                            <span style="font-size:0.75rem; color:#64748b;">${p.indirizzo}</span><br>
                            <div style="margin-top:8px; border-top:1px solid #eee; padding-top:8px; display:flex; flex-direction:column; gap:6px;">
                                <button onclick="navigaEGeocodifica('${p.nome.replace(/'/g, "\\'")}', ${p.lat}, ${p.lon})" style="background:#4f46e5; color:white; border:none; padding:8px; border-radius:5px; font-weight:700; cursor:pointer; width:100%;">VEDI SU GOOGLE MAPS</button>
                                <div style="font-size:0.65rem; color:#ef4444; background:#fef2f2; padding:5px; border-radius:4px; text-align:center; font-weight:600;">⚠️ Puoi trascinare l'icona sulla mappa per correggere la posizione!</div>
                            </div>
                        </div>
                    `;
                    m.bindPopup(popupContent);
                    
                    m.on('dragend', (e) => {
                        const newPos = e.target.getLatLng();
                        _salvaNuovaPosizione(p.nome, newPos.lat, newPos.lng);
                    });
                    
                    m.on('click', (e) => {
                        if (activeAction) {
                            L.DomEvent.stopPropagation(e);
                            togglePointSelection(z.id_zona, p, pointId);
                        }
                    });

                    markers.push({ zid: z.id_zona, pid: pointId, layer: m, data: p });
                });
            });
        }

        function togglePointSelection(zid, p, pointId) {
            const idx = selectedPoints.findIndex(sp => (sp.pointId === pointId));
            const el = document.getElementById(`marker-${pointId}`);
            if (idx >= 0) {
                selectedPoints.splice(idx, 1);
                if (el) el.classList.remove('marker-selected');
            } else {
                if (zid !== activeSourceZid) return alert("Scegli un punto della zona che stai modificando!");
                selectedPoints.push({ zid, p, pointId });
                if (el) el.classList.add('marker-selected');
            }
            renderSidebar(); // Aggiorna il contatore nella card
        }

        function startAction(type, zid) {
            activeAction = type;
            activeSourceZid = zid;
            selectedPoints = [];
            renderSidebar();
            focusZone(zid);
        }

        function executeDividi(sourceZid) {
            const sourceZone = DATA_ZONE.find(z => z.id_zona === sourceZid);
            const checkboxes = document.querySelectorAll(`#card-${sourceZid} input.dividi-chk:checked`);
            if (checkboxes.length === 0) return alert("Seleziona almeno un indirizzo con la spunta!");
            
            const pIds = Array.from(checkboxes).map(c => c.value);
            const pointsToMove = sourceZone.lista_punti.filter(p => {
                const pid = p.id || (p.codice_frutta + "_" + p.nome).replace(/[^a-zA-Z0-9]/g, '_');
                return pIds.includes(pid);
            });
            
            sourceZone.split_count = (sourceZone.split_count || 0) + 1;
            const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            const reqIdx = sourceZone.split_count - 1;
            const letter = alphabet[reqIdx % 26];
            const nuovoGiro = (sourceZone.nome_giro || "Viaggio") + "/" + letter;
            
            const newId = sourceZid + "_" + Date.now().toString().slice(-4);
            const newZone = {
                id_zona: newId, 
                nome_zona: "Divisa da " + sourceZid,
                nome_giro: nuovoGiro,
                split_count: 0,
                lista_punti: pointsToMove,
                numero_consegne: pointsToMove.length,
                tipologia: sourceZone.tipologia,
                color: _get_random_palette_color()
            };
            DATA_ZONE.push(newZone);
            
            sourceZone.lista_punti = sourceZone.lista_punti.filter(p => !pointsToMove.includes(p));
            sourceZone.numero_consegne = sourceZone.lista_punti.length;
            sourceZone._statsHtml = null; // Forza ricalcolo
            
            cancelAction();
            init();
        }

        function executeSposta(sourceZid) {
            const sourceZone = DATA_ZONE.find(z => z.id_zona === sourceZid);
            const selects = document.querySelectorAll(`#card-${sourceZid} select.sposta-sel`);
            let moved = 0;
            let currentPoints = [...sourceZone.lista_punti];
            
            selects.forEach(sel => {
                if (sel.value) {
                    const targetZid = sel.value;
                    const pid = sel.dataset.pid;
                    const pIndex = currentPoints.findIndex(p => {
                        const cmp = p.id || (p.codice_frutta + "_" + p.nome).replace(/[^a-zA-Z0-9]/g, '_');
                        return cmp === pid;
                    });
                    if (pIndex >= 0) {
                        const pToMove = currentPoints[pIndex];
                        const targetZone = DATA_ZONE.find(z => z.id_zona === targetZid);
                        if (targetZone) {
                            targetZone.lista_punti.push(pToMove);
                            targetZone.numero_consegne = targetZone.lista_punti.length;
                            targetZone._statsHtml = null; // Forza ricalcolo target
                            currentPoints.splice(pIndex, 1);
                            moved++;
                        }
                    }
                }
            });
            
            if (moved > 0) {
                sourceZone.lista_punti = currentPoints;
                sourceZone.numero_consegne = sourceZone.lista_punti.length;
                sourceZone._statsHtml = null; // Forza ricalcolo source
                cancelAction();
                init();
            } else {
                alert("Non hai selezionato nessuno spostamento nelle tendine.");
                cancelAction();
            }
        }

        function _get_random_palette_color() {
            const p = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4"];
            return p[Math.floor(Math.random()*p.length)];
        }

        function cancelAction() {
            activeAction = null; activeSourceZid = null; selectedPoints = [];
            renderSidebar();
            document.querySelectorAll('.marker-base').forEach(m => m.classList.remove('marker-selected'));
        }

        function focusZone(zid) {
            if (activeAction) return; // Non compattare se sta facendo un'azione
            if (activeExpandedZid === zid) {
                activeExpandedZid = null; // chiude
            } else {
                activeExpandedZid = zid; // apre
            }
            renderSidebar();
            setTimeout(() => {
                const card = document.getElementById('card-' + zid);
                if (card && activeExpandedZid) card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 50);
        }

        function navigaEGeocodifica(nome, lat, lon) {
            // URL per vedere il marker su Google Maps senza avviare la navigazione
            const url = `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`;
            window.open(url, '_blank');
            
            // Chiediamo conferma all'utente se la posizione è corretta per salvarla
            setTimeout(() => {
                if (confirm(`Hai verificato la posizione di "${nome}"? \nVuoi salvarla permanentemente come coordinate ufficiali?`)) {
                    fetch('http://localhost:8080/save_coord', {
                        method: 'POST', headers: { 'Content-Type': 'application/json' },
                        mode: 'cors', body: JSON.stringify({ nome, lat, lon })
                    })
                    .then(res => res.json())
                    .then(d => alert(d.msg))
                    .catch(err => alert("Errore connessione server Python"));
                }
            }, 1000);
        }

        function _salvaNuovaPosizione(nome, lat, lon) {
            if (confirm(`Confermi di voler impostare la NUOVA POSIZIONE per "${nome}"? \nL'indirizzo verrà rilocato permanentemente.`)) {
                fetch('http://localhost:8080/save_coord', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    mode: 'cors', body: JSON.stringify({ nome, lat, lon })
                })
                .then(res => res.json())
                .then(d => {
                    const s = document.getElementById('save-status');
                    s.textContent = d.msg;
                    s.style.display = 'block'; setTimeout(() => s.style.display = 'none', 3000);
                })
                .catch(err => alert("Errore connessione server Python"));
            }
        }

        function saveAllToServer() {
            const btn = document.getElementById('btn-master-save');
            btn.textContent = "SALVATAGGIO..."; btn.disabled = true;
            fetch('http://localhost:8080/save', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                mode: 'cors', body: JSON.stringify(DATA_ZONE, (k, v) => k === 'color' ? undefined : v, 2)
            })
            .then(res => res.json())
            .then(() => {
                const s = document.getElementById('save-status');
                s.style.display = 'block'; setTimeout(() => s.style.display = 'none', 3000);
            })
            .catch(err => alert("Errore connessione: " + err))
            .finally(() => { btn.textContent = "SALVA TUTTO"; btn.disabled = false; });
        }

        window.onload = init;
    </script>
</body>
</html>"""
    
    final_html = html_template.replace("{{DATA_GIORNO}}", data).replace("{{JSON_ZONE}}", zone_js)
    output_path.write_text(final_html, encoding="utf-8")
    print(f"  Mappa generata: {output_path.name}")

def main():
    global TARGET_FILE_3B, TARGET_FILE_2B, TARGET_FILE_UNIFICATO
    if len(sys.argv) < 2:
        folders = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
        if not folders: return 1
        # Ordiniamo per NOME (data) così 24-03 viene dopo 23-03
        folders.sort(key=lambda x: x.name, reverse=True)
        data = folders[0].name.split("_")[1]
    else:
        data = sys.argv[1].strip()
    if re.match(r"^\d{2}-\d{2}$", data): data = f"{data}-2026"
    
    output_base = CONSEGNE_DIR / f"CONSEGNE_{data}"
    TARGET_FILE_UNIFICATO = output_base / "punti_consegna_unificati.json"
    TARGET_FILE_3B = output_base / "3b_assegna_ddt_zone.json" # Legacy
    TARGET_FILE_2B = output_base / "2b_crea_zone_consegna.json" # Legacy
    
    if not TARGET_FILE_UNIFICATO.exists():
        print(f"File unificato non trovato in {output_base}")
        return 1
    
    unificato_data = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
    punti_list = unificato_data.get("punti", [])
    
    # GEOCODING MANCANTI
    try: cache = json.loads(GEOCODE_CACHE.read_text(encoding="utf-8")) if GEOCODE_CACHE.exists() else {}
    except: cache = {}
    
    geo = None
    try:
        from geopy.geocoders import Nominatim
        geo = Nominatim(user_agent="GestioneDDTViaggi/1.0")
    except ImportError: pass
    
    ha_modificato_json = False
    for p in punti_list:
        if p.get("lat") is None or p.get("lon") is None:
            if geo:
                q1 = f"{p.get('nome', '')} {p.get('indirizzo', '')}"
                q2 = p.get("indirizzo", "")
                lat, lon = _geocode(q1, cache, geo)
                if lat is None and q2 and q2 != q1: lat, lon = _geocode(q2, cache, geo)
                if lat is None and q2: lat, lon = _geocode_photon(q2, cache)
                
                if lat is not None and lon is not None:
                    p["lat"], p["lon"] = lat, lon
                    ha_modificato_json = True
                    print(f"  Geocodificato: {p.get('nome')} in {lat},{lon}")

    if geo and cache:
        GEOCODE_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    if ha_modificato_json:
        TARGET_FILE_UNIFICATO.write_text(json.dumps(unificato_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # RAGGRUPPAMENTO AUTOMATICO PER ZONA
    
    zone_dict = {}
    for p in punti_list:
        zid = p.get("zona") or "SENZA_ZONA"
        if zid not in zone_dict:
            is_latte = bool(p.get("codici_ddt_latte") and not p.get("codici_ddt_frutta"))
            zone_dict[zid] = {
                "id_zona": zid,
                "nome_zona": f"Zona {zid}",
                "lista_punti": [],
                "tipologia": "solo_latte" if is_latte else "mista/frutta",
                "numero_consegne": 0,
                "da_mappare": False
            }
        zone_dict[zid]["lista_punti"].append(p)
        zone_dict[zid]["numero_consegne"] += 1
        if not p.get("lat"):
            zone_dict[zid]["da_mappare"] = True
    
    zone_list = sorted(list(zone_dict.values()), key=lambda x: str(x["id_zona"]))
    
    # ASSEGNAZIONE NOMI GIRO
    for i, z in enumerate(zone_list, 1):
        z["nome_giro"] = f"Viaggio {i}"
        z["split_count"] = 0

    html_file = output_base / "4_crea_mappa_zone_interattiva.html"
    _salva_html_zone(zone_list, html_file, data)
    
    print(f"\n[INFO] Server attivo su http://localhost:{PORT}")
    print(f"[INFO] Apri: {html_file.name}")
    print(f"[INFO] Premi CTRL+C per terminare.")
    
    try:
        webbrowser.open(f"file:///{html_file.resolve()}")
        with socketserver.TCPServer(("", PORT), SaveHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server fermato.")
    return 0

if __name__ == "__main__":
    exit(main())

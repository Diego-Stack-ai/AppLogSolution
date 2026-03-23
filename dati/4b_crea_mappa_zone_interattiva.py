#!/usr/bin/env python3
"""
4b_crea_mappa_zone_interattiva.py (V2.1 - Icone Operative Migliorate)
Genera mappa HTML con icone molto distinte per forma (Goccia, Tonda, Foglia).
"""

import json
import sys
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"

def _get_color(idx):
    palette = [
        "#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", 
        "#ec4899", "#06b6d4", "#f97316", "#14b8a6", "#6366f1",
        "#a855f7", "#3b82f6", "#22c55e", "#d946ef", "#84cc16"
    ]
    return palette[idx % len(palette)]

def _salva_html_zone(zone_list: list, output_path: Path, data: str):
    for i, z in enumerate(zone_list):
        z["color"] = _get_color(i)

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
        :root {
            --primary: #4f46e5;
            --bg: #f1f5f9;
            --card: #ffffff;
            --text: #1e293b;
        }
        * { box-sizing: border-box; }
        body { 
            margin: 0; 
            font-family: 'Outfit', sans-serif; 
            height: 100vh; 
            display: flex; 
            background: var(--bg);
            color: var(--text);
            overflow: hidden;
        }
        #sidebar {
            width: 380px;
            height: 100%;
            background: white;
            border-right: 1px solid #e2e8f0;
            display: flex;
            flex-direction: column;
            z-index: 1000;
            box-shadow: 4px 0 25px rgba(0,0,0,0.08);
        }
        #header {
            padding: 25px 20px;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
        }
        #header h1 { margin: 0; font-size: 1.4rem; font-weight: 700; }
        
        #zone-list {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            background: #f8fafc;
        }
        .zone-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: 0.2s;
        }
        .zone-card:hover { border-color: #cbd5e1; transform: translateY(-2px); }
        .zone-card.selected { border: 2px solid var(--primary); background: #f5f3ff; }
        
        .zone-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .color-pill { width: 12px; height: 12px; border-radius: 50%; }
        .zone-title { font-weight: 700; font-size: 0.95rem; flex: 1; }

        .zone-actions { display: flex; gap: 5px; margin-top: 10px; border-top: 1px solid #f1f5f9; padding-top: 8px; }
        .btn {
            flex: 1;
            padding: 6px;
            font-size: 0.7rem;
            font-weight: 800;
            border: 1px solid #e2e8f0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            color: #64748b;
        }
        .btn:hover { background: #f1f5f9; }
        .btn.active { background: var(--primary); color: white; border-color: var(--primary); }
        
        #map { flex: 1; z-index: 1; }
        
        /* ICONE OPERATIVE VERSIONI 2.1 (MOLTO DISTINTE) */
        .marker-base {
            width: 36px;
            height: 36px;
            display: flex !important;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 900;
            font-size: 14px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            border: 2px solid white;
        }
        
        /* 1. GOCCIA (Standard) */
        .marker-goccia {
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
        }
        .marker-goccia span { transform: rotate(45deg); }
        
        /* 2. TONDA (Consegna + Ritorno) - Bordo doppio per massima visibilità */
        .marker-tonda {
            border-radius: 50%;
            border-width: 4px; /* Più spessa */
            box-shadow: 0 0 0 2px black, 0 4px 8px rgba(0,0,0,0.4);
        }
        
        /* 3. FOGLIA (Solo Rientro / Fuori Giro) - Forma a rombo smussato */
        .marker-foglia {
            border-radius: 12px 2px 12px 2px;
            transform: rotate(45deg);
        }
        .marker-foglia span { transform: rotate(-45deg); }

        #ui-overlay {
            position: fixed;
            top: 20px; left: 400px; right: 20px;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(8px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            z-index: 2000;
            display: none;
        }
        .badge-tipo { padding: 3px 6px; font-size: 0.6rem; border-radius: 4px; text-transform: uppercase; font-weight: 800; }
        .badge-mista { background: #fef3c7; color: #92400e; }
        .badge-latte { background: #dcfce7; color: #166534; }
    </style>
</head>
<body>
    <div id="sidebar">
        <div id="header">
            <h1>Gestione Zone</h1>
            <p style="margin:5px 0 0; opacity:0.7; font-size:0.8rem;">Data: {{DATA_GIORNO}}</p>
        </div>
        <div id="zone-list"></div>
    </div>
    <div id="map"></div>
    
    <div id="ui-overlay">
        <div id="ui-content"></div>
        <div style="margin-top:20px; display:flex; gap:10px; justify-content:flex-end;">
            <button class="btn" style="flex:0; padding:10px 20px;" onclick="closeOverlay()">ANNULLA</button>
            <button class="btn active" style="flex:0; padding:10px 20px;" onclick="applyChanges()">CONFERMA</button>
        </div>
    </div>

    <script>
        let DATA_ZONE = {{JSON_ZONE}};
        const map = L.map('map', { zoomControl: false }).setView([45.5, 12.0], 10);
        L.control.zoom({ position: 'bottomright' }).addTo(map);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        let markers = [];
        let currentZoneId = null;

        function init() {
            renderSidebar();
            renderMarkers();
            if (markers.length > 0) {
                const group = new L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.1));
            }
        }

        function renderSidebar() {
            const list = document.getElementById('zone-list');
            list.innerHTML = DATA_ZONE.map(z => {
                const isMista = z.tipologia === 'mista/frutta';
                return `
                <div class="zone-card" id="card-${z.id_zona}" onclick="focusZone('${z.id_zona}')">
                    <div class="zone-header">
                        <div class="color-pill" style="background: ${z.color}"></div>
                        <div class="zone-title">${z.nome_zona}</div>
                        <span class="badge-tipo ${isMista ? 'badge-mista' : 'badge-latte'}">
                            ${isMista ? 'Mista' : 'Solo Latte'}
                        </span>
                    </div>
                    <div style="font-size:0.75rem; color:#64748b; font-weight:600">
                        <span class="material-icons-round" style="font-size:12px">location_on</span> ${z.numero_consegne} Punti
                    </div>
                    <div class="zone-actions">
                        <button class="btn" style="color:#22c55e" onclick="event.stopPropagation(); handleAction('ok', '${z.id_zona}')">OK</button>
                        <button class="btn" onclick="event.stopPropagation(); handleAction('dividi', '${z.id_zona}')">DIVIDI</button>
                        <button class="btn" onclick="event.stopPropagation(); handleAction('assegna', '${z.id_zona}')">SPOSTA</button>
                    </div>
                </div>
            `;}).join('');
        }

        function renderMarkers() {
            markers.forEach(m => map.removeLayer(m));
            markers = [];
            
            DATA_ZONE.forEach(z => {
                z.lista_punti.forEach(p => {
                    if (!p.lat || !p.lon) return;
                    
                    // Logica icone
                    let classeIcona = 'marker-goccia';
                    const hasDelivery = (p.codici_ddt_frutta && p.codici_ddt_frutta.length > 0) || (p.codici_ddt_latte && p.codici_ddt_latte.length > 0);
                    const hasPickup = p.rientri_alert && p.rientri_alert.length > 0;

                    if (hasDelivery && hasPickup) classeIcona = 'marker-tonda';
                    else if (!hasDelivery && hasPickup) classeIcona = 'marker-foglia';

                    const icon = L.divIcon({
                        className: '',
                        html: `<div class="marker-base ${classeIcona}" style="background: ${z.color}"><span>${p.nome.charAt(0).toUpperCase()}</span></div>`,
                        iconSize: [36, 36],
                        iconAnchor: [18, 18]
                    });

                    const m = L.marker([p.lat, p.lon], { icon }).addTo(map);
                    m.bindPopup(`<b style="font-family:Outfit">${p.nome}</b><br><span style="color:#64748b">${p.indirizzo}</span><hr><b>Zona:</b> ${z.id_zona}<br><b>Operazione:</b> ${hasPickup ? 'Consegna + Ritiro' : 'Consegna'}`);
                    markers.push(m);
                });
            });
        }

        function focusZone(zid) {
            currentZoneId = zid;
            document.querySelectorAll('.zone-card').forEach(c => c.classList.remove('selected'));
            document.getElementById('card-' + zid).classList.add('selected');
            
            const zone = DATA_ZONE.find(z => z.id_zona === zid);
            const zPoints = zone.lista_punti.filter(pt => pt.lat && pt.lon);
            if (zPoints.length > 0) {
                const bounds = L.latLngBounds(zPoints.map(pt => [pt.lat, pt.lon]));
                map.fitBounds(bounds, { padding: [40, 40] });
            }
        }

        function handleAction(type, zid) {
            if (type === 'ok') {
                document.getElementById('card-' + zid).style.opacity = '0.4';
                return;
            }
            document.getElementById('ui-overlay').style.display = 'block';
            document.getElementById('ui-content').innerHTML = `<h2>Azione: ${type.toUpperCase()} su Zona ${zid}</h2><p>Funzionalità in fase di attivazione...</p>`;
        }

        function closeOverlay() { document.getElementById('ui-overlay').style.display = 'none'; }
        function applyChanges() { closeOverlay(); }

        window.onload = init;
    </script>
</body>
</html>"""
    
    final_html = html_template.replace("{{DATA_GIORNO}}", data)
    final_html = final_html.replace("{{JSON_ZONE}}", zone_js)
    
    output_path.write_text(final_html, encoding="utf-8")
    print(f"  Salvato: {output_path.name}")

def main():
    if len(sys.argv) < 2:
        folders = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
        if not folders: return 1
        folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        data = folders[0].name.split("_")[1]
    else:
        data = sys.argv[1].strip()
    if re.match(r"^\d{2}-\d{2}$", data): data = f"{data}-2026"
    
    output_base = CONSEGNE_DIR / f"CONSEGNE_{data}"
    json_3b = output_base / "3b_assegna_ddt_zone.json"
    
    if not json_3b.exists():
        print(f"File 3b non trovato in {output_base}")
        return 1
    
    zone_list = json.loads(json_3b.read_text(encoding="utf-8"))
    html_file = output_base / f"4b_crea_mappa_zone_interattiva.html"
    _salva_html_zone(zone_list, html_file, data)
    print(f"--- Completato (v2.1) ---")
    return 0

if __name__ == "__main__":
    exit(main())

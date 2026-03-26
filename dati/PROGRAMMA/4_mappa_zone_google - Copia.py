import json, sys, re, webbrowser, threading, time, logging
import html as html_module
import xml.etree.ElementTree as ET
# Flask e Flask-CORS verranno importati solo se serve avviare il server
try:
    from flask import Flask, render_template_string, request, jsonify
    from flask_cors import CORS
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    Flask = lambda *args, **kwargs: None
    render_template_string = request = jsonify = None

from pathlib import Path

# --- CONFIGURAZIONE ---
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GEOCODE_CACHE = PROG_DIR / "geocode_cache.json"

# INSERISCI QUI LA TUA API KEY DI GOOGLE MAPS
GOOGLE_MAPS_API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

if HAS_FLASK:
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
else:
    app = None

# Configurazione Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Variabili globali per tracciare i file in uso
TARGET_FILE_UNIFICATO = None
TARGET_FILE_VIAGGI = None
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

excel_lock = threading.Lock()

def _aggiorna_mappatura_destinazioni(nome, lat, lon):
    with excel_lock:
        try:
            import pandas as pd
            file_path = PROG_DIR / "mappatura_destinazioni.xlsx"
            if not file_path.exists(): return False
            
            df = pd.read_excel(file_path)
            # Nomi colonne reali: 'A chi va consegnato', 'Latitudine', 'Longitudine'
            col_nome = 'A chi va consegnato'
            col_lat = 'Latitudine'
            col_lon = 'Longitudine'
            
            mask = df[col_nome].astype(str).str.lower() == str(nome).lower()
            if mask.any():
                df.loc[mask, col_lat] = lat
                df.loc[mask, col_lon] = lon
                df.to_excel(file_path, index=False)
                logger.info(f"💾 Coordinate salvate su Excel per: {nome}")
                return True
            else:
                logger.warning(f"❓ Cliente '{nome}' non trovato in colonna '{col_nome}'")
                return "nome_non_trovato"
        except PermissionError:
            logger.error(f"🚫 File bloccato! Chiudi '{file_path.name}' prima di salvare.")
            return "file_aperto"
        except Exception as e:
            logger.exception(f"💥 Errore critico salvataggio Excel: {e}")
            return str(e)

if HAS_FLASK:
    @app.after_request
    def add_header(r):
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    @app.route('/')
    def index():
        from pathlib import Path
        import json as _js
        is_locked_val = False
        if TARGET_FILE_UNIFICATO and TARGET_FILE_UNIFICATO.exists():
            try:
                unif = _js.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
                is_locked_val = unif.get("is_locked", False)
            except: pass
            
        return render_template_string(HTML_TEMPLATE, 
                                      DATA_GIORNO=DATA_GIORNO, 
                                      JSON_ZONE=json.dumps(ZONE_LIST_CACHE, ensure_ascii=False),
                                      GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY,
                                      IS_LOCKED_JS="true" if is_locked_val else "false")

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
                        # Usa codice_univoco come chiave stabile (mai collisione su p00000)
                        pid = p.get("codice_univoco") or f"{p.get('codice_frutta') or 'p00000'}_{p.get('codice_latte') or 'p00000'}"
                        mappa_point_to_zona[pid] = z["id_zona"]
                
                for p in punti_flat:
                    pid = p.get("codice_univoco") or f"{p.get('codice_frutta') or 'p00000'}_{p.get('codice_latte') or 'p00000'}"
                    if pid in mappa_point_to_zona:
                        p["zona"] = mappa_point_to_zona[pid]


                TARGET_FILE_UNIFICATO.write_text(json.dumps(unificato_raw, indent=2, ensure_ascii=False), encoding="utf-8")
            
            # Filtra le zone vuote (senza consegne)
            data_filtrata = [z for z in data if len(z.get("lista_punti", [])) > 0]
            ZONE_LIST_CACHE = data_filtrata

            # 2. Salva viaggi_giornalieri.json
            if TARGET_FILE_VIAGGI:
                TARGET_FILE_VIAGGI.write_text(json.dumps(data_filtrata, indent=2, ensure_ascii=False), encoding="utf-8")
                
                # Pulizia unico file vecchio 3b se esiste
                old_3b = TARGET_FILE_VIAGGI.parent / "3b_assegna_ddt_zone.json"
                if old_3b.exists():
                    try: old_3b.unlink()
                    except: pass
                
            return jsonify({"status": "ok"})
        except Exception as e:
            print(f"Errore save: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/toggle_lock', methods=['POST'])
    def toggle_lock():
        try:
            req = request.json
            action = req.get('action')
            if TARGET_FILE_UNIFICATO and TARGET_FILE_UNIFICATO.exists():
                unificato = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
                is_locked = (action == 'lock')
                unificato['is_locked'] = is_locked
                TARGET_FILE_UNIFICATO.write_text(json.dumps(unificato, indent=2, ensure_ascii=False), encoding="utf-8")
                return jsonify({"status": "ok", "is_locked": is_locked})
            return jsonify({"status": "error", "message": "File non trovato"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

if HAS_FLASK:
    @app.route('/save_coord', methods=['POST'])
    def save_coord():
        try:
            payload = request.json # {nome, lat, lon}
            logger.info(f"📥 Ricevuta richiesta salvataggio coordinate: {payload}")
            
            if not payload or 'nome' not in payload:
                return jsonify({"status": "error", "msg": "Dati mancanti nel payload"}), 400
                
            result = _aggiorna_mappatura_destinazioni(payload['nome'], payload['lat'], payload['lon'])
            
            if result is True:
                # Aggiorniamo la CACHE Python e i file JSON in background in modo che i file siano allineati senza dover fare salva tutto.
                global ZONE_LIST_CACHE
                for z in ZONE_LIST_CACHE:
                    for pt in z.get("lista_punti", []):
                        if pt.get("nome", "").lower() == payload['nome'].lower():
                            pt['lat'] = payload['lat']
                            pt['lon'] = payload['lon']
                try:
                    if TARGET_FILE_UNIFICATO and TARGET_FILE_UNIFICATO.exists():
                        d_u = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding='utf-8'))
                        for pt in d_u.get('punti', []):
                            if pt.get('nome', '').lower() == payload['nome'].lower():
                                pt['lat'] = payload['lat']
                                pt['lon'] = payload['lon']
                        TARGET_FILE_UNIFICATO.write_text(json.dumps(d_u, indent=2, ensure_ascii=False), encoding='utf-8')
                except Exception as j_err:
                    logger.error(f"Impossibile aggiornare unificato: {j_err}")
                    
                try:
                    if TARGET_FILE_VIAGGI and TARGET_FILE_VIAGGI.exists():
                        d_v = json.loads(TARGET_FILE_VIAGGI.read_text(encoding='utf-8'))
                        for z in d_v:
                            for pt in z.get('lista_punti', []):
                                if pt.get('nome', '').lower() == payload['nome'].lower():
                                    pt['lat'] = payload['lat']
                                    pt['lon'] = payload['lon']
                        TARGET_FILE_VIAGGI.write_text(json.dumps(d_v, indent=2, ensure_ascii=False), encoding='utf-8')
                except Exception as j_err:
                    logger.error(f"Impossibile aggiornare Viaggi: {j_err}")

                return jsonify({"status": "ok", "msg": f"Posizione salvata correttamente per {payload['nome']}!"})
            elif result == "file_aperto":
                return jsonify({"status": "error", "msg": "ERRORE: Chiudi l'Excel 'mappatura_destinazioni.xlsx' e riprova!"}), 500
            elif result == "nome_non_trovato":
                return jsonify({"status": "error", "msg": f"Cliente '{payload['nome']}' non trovato nel file Excel."}), 404
            else:
                return jsonify({"status": "error", "msg": f"Errore imprevisto: {result}"}), 500
                
        except Exception as e:
            logger.exception("💥 Errore durante l'elaborazione di /save_coord")
            return jsonify({"status": "error", "msg": f"Errore interno: {str(e)}"}), 500

def _escape_xml(s: str) -> str:
    if not s: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def _salva_kml(punti: list[dict], path: Path, data: str):
    """Salva KML per import in Google My Maps."""
    root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(root, "Document")
    ET.SubElement(doc, "name").text = f"Zone Google {data}"
    for i, p in enumerate(punti, 1):
        if not p.get('lat') or not p.get('lon'): continue
        pm = ET.SubElement(doc, "Placemark")
        nome = p.get("nome") or f"Punto {i}"
        ET.SubElement(pm, "name").text = f"{i}. {nome[:80]}"
        desc = [
            f"<b>{_escape_xml(nome)}</b>",
            f"Indirizzo: {_escape_xml(p.get('indirizzo', ''))}",
            f"Zona: {_escape_xml(p.get('zona', ''))}",
            f"Orario: {_escape_xml(p.get('orario_min', ''))}-{_escape_xml(p.get('orario_max', ''))}"
        ]
        ET.SubElement(pm, "description").text = "<br>".join(desc)
        pt = ET.SubElement(pm, "Point")
        ET.SubElement(pt, "coordinates").text = f"{p['lon']},{p['lat']},0"
    tree = ET.ElementTree(root)
    if hasattr(ET, "indent"): ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True, method="xml")

def _salva_html_fisico(output_base, template_html, data, zone_json, api_key, is_locked):
    is_locked_js = 'true' if is_locked else 'false'
    html_content = template_html.replace("{{DATA_GIORNO}}", data) \
                                .replace("{{JSON_ZONE | safe}}", zone_json) \
                                .replace("{{GOOGLE_MAPS_API_KEY}}", api_key) \
                                .replace("{{IS_LOCKED_JS}}", is_locked_js)
    file_path = output_base / "4_mappa_zone_google.html"
    file_path.write_text(html_content, encoding="utf-8")
    logger.info(f"✅ Mappa statica creata: {file_path.name}")

# --- TEMPLATE HTML (GOOGLE MAPS VERSION) ---
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <script>
        (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. See https://goo.gle/js-api-loading-troubleshooting"):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
            key: "{{GOOGLE_MAPS_API_KEY}}",
            v: "beta"
        });
    </script>
    <style>
        :root { 
            --primary: #6366f1; 
            --primary-dark: #4f46e5;
            --bg: #0f172a; 
            --sidebar-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --accent: #10b981;
            --glass: rgba(255, 255, 255, 0.9);
            --card-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --card-hover-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }
        * { box-sizing: border-box; -webkit-font-smoothing: antialiased; }
        body { margin: 0; font-family: 'Inter', sans-serif; height: 100vh; display: flex; background: var(--bg); color: var(--text-main); overflow: hidden; }
        
        #sidebar { 
            width: 400px; height: 100%; background: var(--sidebar-bg); 
            border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; 
            z-index: 1000; box-shadow: 10px 0 30px rgba(0,0,0,0.05);
            transition: transform 0.3s ease-in-out;
        }
        
        #header { 
            padding: 30px 24px; 
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
            color: white; 
            position: relative;
            overflow: hidden;
        }
        #header::after {
            content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }
        #header h1 { 
            margin: 0; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.025em;
            display: flex; justify-content: space-between; align-items: center; 
        }
        
        #zone-list { 
            flex: 1; overflow-y: auto; padding: 20px; background: #f8fafc;
            scrollbar-width: thin; scrollbar-color: #cbd5e1 #f8fafc;
        }
        #zone-list::-webkit-scrollbar { width: 6px; }
        #zone-list::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

        .zone-card { 
            background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; 
            padding: 18px; margin-bottom: 16px; cursor: pointer; 
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--card-shadow);
        }
        .zone-card:hover { 
            transform: translateY(-2px); border-color: var(--primary); 
            box-shadow: var(--card-hover-shadow);
        }
        .zone-card.selected { border: 2.5px solid var(--primary); background: #f5f3ff; }
        
        .zone-header { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
        .color-pill { width: 14px; height: 14px; border-radius: 6px; box-shadow: 0 0 0 2px rgba(0,0,0,0.05); }
        .zone-title { font-weight: 700; font-size: 1rem; flex: 1; color: #1e293b; }
        
        .badge-tipo { padding: 4px 8px; font-size: 0.65rem; border-radius: 6px; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; }
        .badge-mista { background: #fef3c7; color: #92400e; }
        .badge-latte { background: #dcfce7; color: #166534; }
        
        #map { flex: 1; z-index: 1; min-width: 0; }
        
        .btn { 
            flex: 1; padding: 8px 12px; font-size: 0.75rem; font-weight: 700; 
            border: 1px solid #e2e8f0; background: white; border-radius: 8px; 
            cursor: pointer; color: var(--text-muted); transition: all 0.2s;
            display: flex; align-items: center; justify-content: center; gap: 4px;
        }
        .btn:hover { background: #f1f5f9; border-color: #cbd5e1; color: var(--text-main); }
        .btn-confirm { background: var(--primary); color: white; border: none; }
        .btn-confirm:hover { background: var(--primary-dark); transform: scale(1.02); }
        
        /* Step Sicurezza: Lock Map */
        .btn-lock { background: #f1f5f9; color: #64748b; border: 1.5px solid #e2e8f0; min-width: 140px; }
        .btn-lock.locked { background: #ef4444; color: white; border: none; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3); }
        .btn-lock:hover { background: #e2e8f0; }
        .btn-lock.locked:hover { background: #dc2626; transform: scale(1.02); }
        
        #save-status { 
            position: fixed; top: 30px; left: 50%; transform: translateX(-50%);
            padding: 12px 24px; border-radius: 50px; background: rgba(16, 185, 129, 0.95);
            backdrop-filter: blur(8px); color: white; font-weight: 700; 
            display: none; z-index: 5000; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            animation: slideDown 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes slideDown { 
            from { transform: translate(-50%, -100%); opacity: 0; }
            to { transform: translate(-50%, 0); opacity: 1; }
        }

        .custom-marker {
            position: absolute; width: 34px; height: 34px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 800; font-size: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2.5px solid white;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .custom-marker:hover { transform: scale(1.3) rotate(8deg); z-index: 999; }
        .m-tonda { border-radius: 50%; }
        .m-goccia { border-radius: 50% 50% 50% 0; transform: rotate(-45deg); }
        .m-goccia span { transform: rotate(45deg); }
        .m-foglia { border-radius: 14px 4px 14px 4px; transform: rotate(45deg); }
        .m-foglia span { transform: rotate(-45deg); }
        
        /* Nuove forme per sovrapposizioni (Layering) */
        .m-quadrato { border-radius: 4px; }
        .m-triangolo { 
            background: transparent !important; 
            border-left: 20px solid transparent; 
            border-right: 20px solid transparent; 
            border-bottom: 40px solid #ccc; /* Il colore viene sovrascritto da JS */
            border-radius: 0; border: none; box-shadow: none;
            width: 0 !important; height: 0 !important;
        }
        .m-triangolo span { position: absolute; top: 18px; left: -8px; width: 16px; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
    </style>
</head>
<body>
    <div id="sidebar">
        <div id="header">
            <h1>Gestione Zone <span id="tot-points" style="font-size:0.8rem; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-weight: 500;">0 Punti</span></h1>
            <div style="display:flex; justify-content: space-between; align-items: center; margin-top:12px;">
                <div style="display:flex; flex-direction:column;">
                    <span style="opacity:0.6; font-size:0.75rem; text-transform: uppercase; font-weight:700; letter-spacing:0.05em;">Programmazione</span>
                    <span style="font-weight:700; font-size:0.9rem;">{{DATA_GIORNO}}</span>
                </div>
                <button onclick="saveAllToServer()" id="btn-master-save" style="background: var(--accent); color:white; border:none; padding:10px 20px; border-radius:12px; font-weight:800; cursor:pointer; font-size:0.8rem; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); transition: 0.2s;">
                    SALVA TUTTO
                </button>
            </div>
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <button onclick="toggleLockMap()" id="btn-lock-map" class="btn btn-lock" style="padding: 10px 14px; border-radius: 12px; font-weight: 800; cursor: pointer; flex: 1;">
                    SBLOCCATA 🔓
                </button>
                <button id="btn-toggle-drag" onclick="toggleDragging()" style="background:#4b5563; color:white; border:none; padding:10px 14px; border-radius:12px; font-weight:800; cursor:pointer; flex: 1.5; font-size:0.7rem;">
                    🔒 SPOSTA PUNTI (OFF)
                </button>
            </div>
        </div>
        <div id="zone-list"></div>
    </div>
    <div id="map"></div>
    <div id="save-status">💾 Cambiamenti salvati!</div>

    <script>
        let DATA_ZONE = {{JSON_ZONE | safe}};
        let map;
        let gMarkers = [];
        let DRAGGING_ENABLED = false;
        let activeExpandedZid = null;
        let activeAction = null;
        let activeSourceZid = null;
        const DEPOT = { lat: 45.451912, lng: 11.736761 };
        let isLockedGlobal = {{IS_LOCKED_JS}};

        async function toggleLockMap() {
            const action = isLockedGlobal ? 'unlock' : 'lock';
            try {
                const r = await fetch('/toggle_lock', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: action })
                });
                const d = await r.json();
                if (d.status === 'ok') {
                    isLockedGlobal = (action === 'lock');
                    _updateLockUI();
                } else {
                    alert("Errore cambio stato: " + d.msg);
                }
            } catch (e) {
                alert("Errore server: " + e );
            }
        }

        function _updateLockUI() {
            const btn = document.getElementById('btn-lock-map');
            if (isLockedGlobal) {
                btn.innerHTML = 'BLOCCATA 🔒';
                btn.classList.add('locked');
            } else {
                btn.innerHTML = 'SBLOCCATA 🔓';
                btn.classList.remove('locked');
            }
        }

        async function initMap() {
            const { Map } = await google.maps.importLibrary("maps");
            const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

            map = new Map(document.getElementById("map"), {
                center: { lat: 45.5, lng: 12.0 },
                zoom: 10,
                mapTypeId: 'hybrid',
                mapId: "DEMO_MAP_ID", // Richiesto per Advanced Markers
                disableDefaultUI: false,
                zoomControl: true,
                scaleControl: true
            });

            updateTotals();
            renderSidebar();
            await renderMarkers();
            renderSidebar();
            fitMap();
            _updateLockUI();
        }

        function fitMap() {
            if (gMarkers.length === 0) return;
            const bounds = new google.maps.LatLngBounds();
            gMarkers.forEach(m => bounds.extend(m.getPosition()));
            map.fitBounds(bounds);
        }

        async function toggleDragging() {
            DRAGGING_ENABLED = !DRAGGING_ENABLED;
            const btn = document.getElementById('btn-toggle-drag');
            if (DRAGGING_ENABLED) {
                btn.textContent = "🔓 SPOSTA PUNTI (ON)";
                btn.style.background = "#10b981";
            } else {
                btn.textContent = "🔒 SPOSTA PUNTI (OFF)";
                btn.style.background = "#4b5563";
            }
            await renderMarkers(); // Rigenera i marcatori con la nuova proprietà draggable
            renderSidebar(); // Aggiorna la sidebar per mostrare gli indici corretti
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
                                        <b style="color:${!p.lat ? '#b45309' : '#334155'}; font-size:0.75rem;">${p.nome} <small style="color:#666">(${p._marker_index || ''})</small></b>
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
                                <button class="btn" ${isLockedGlobal ? 'disabled style="opacity:0.4; cursor:not-allowed;"' : ''} onclick="event.stopPropagation(); if(!isLockedGlobal) startAction('dividi', '${z.id_zona}')">DIVIDI</button>
                                <button class="btn" ${isLockedGlobal ? 'disabled style="opacity:0.4; cursor:not-allowed;"' : ''} onclick="event.stopPropagation(); if(!isLockedGlobal) startAction('sposta', '${z.id_zona}')">SPOSTA</button>
                            `}
                        </div>
                    ` : ''}
                </div>`;
            }).join('');
        }

        async function renderMarkers() {
            gMarkers.forEach(m => m.setMap(null));
            gMarkers = [];

            const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

            // Mappa per contare le sovrapposizioni alle stesse coordinate
            const coordCounts = {};

            DATA_ZONE.forEach(z => {
                z.lista_punti.forEach((p, idx) => {
                    if (!p.lat || !p.lon) return;

                    // Gestione Sovrapposizioni (Layering)
                    const key = `${p.lat.toFixed(6)}_${p.lon.toFixed(6)}`;
                    if (!coordCounts[key]) coordCounts[key] = 0;
                    coordCounts[key]++;
                    const layerIdx = coordCounts[key];

                    // Nuova Logica di Business per le Forme:
                    const hasStandardDDT = (p.codici_ddt_frutta && p.codici_ddt_frutta.length > 0) || 
                                           (p.codici_ddt_latte && p.codici_ddt_latte.length > 0);
                    const hasRientro = (p.rientri_alert && p.rientri_alert.length > 0);
                    
                    let formaClasse = 'm-goccia'; // Default base
                    
                    if (!hasStandardDDT && hasRientro) {
                        formaClasse = 'm-foglia'; // Rientro orfano
                    } else if (hasStandardDDT && hasRientro) {
                        formaClasse = 'm-tonda';  // Consegna + Rientro
                    }

                    // Se è un punto sovrapposto, cambiamo forma a prescindere dal tipo DDT per visibilità
                    if (layerIdx === 2) formaClasse = 'm-quadrato';
                    if (layerIdx === 3) formaClasse = 'm-triangolo';
                    if (layerIdx > 3) formaClasse = 'm-tonda'; // Eventuale 4° punto torna tondo

                    // Crea l'elemento DOM personalizzato per il marker
                    const markerElement = document.createElement("div");
                    markerElement.className = `custom-marker ${formaClasse}`;
                    if (formaClasse === 'm-triangolo') {
                        markerElement.style.borderBottomColor = z.color;
                    } else {
                        markerElement.style.backgroundColor = z.color;
                    }
                    p._marker_index = idx + 1; // Salva l'indice per la sidebar
                    markerElement.innerHTML = `<span>${p._marker_index}</span>`;

                    const marker = new AdvancedMarkerElement({
                        position: { lat: p.lat, lng: p.lon },
                        map: map,
                        title: p.nome,
                        content: markerElement, // Usa l'elemento HTML personalizzato
                        gmpDraggable: DRAGGING_ENABLED
                    });

                    // Escape sicuro del nome per il template HTML
                    const encodedNome = encodeURIComponent(p.nome);

                    const infoWindow = new google.maps.InfoWindow({
                        content: `<div style="padding:10px;">
                            <div style="font-weight:800; color:${z.color}">${z.nome_giro}</div>
                            <b>${p.nome}</b><br>${p.indirizzo}<br>
                            <button onclick="window.open('https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}')" style="margin-top:10px; width:100%; padding:5px;">VEDI SU GOOGLE</button>
                            <button onclick="_salvaNuovaPosizione(decodeURIComponent('${encodedNome}'), ${p.lat}, ${p.lon})" style="margin-top:5px; width:100%; padding:5px; background:#10b981; color:white; border:none; border-radius:4px; font-weight:700;">SALVA COORDINATE</button>
                        </div>`
                    });

                    // Evento 2024: gmp-click per Advanced Markers
                    marker.addListener("gmp-click", () => infoWindow.open(map, marker));
                    
                    marker.addListener("dragend", () => {
                        const newPos = marker.position;
                        // Sincronizza i dati JavaScript locali in modo che Salva Tutto non li resetti
                        p.lat = newPos.lat;
                        p.lon = newPos.lng;
                        // Salvataggio Silenzioso senza popup
                        _salvaNuovaPosizione(p.nome, newPos.lat, newPos.lng, true);
                    });

                    gMarkers.push(marker);
                });
            });
        }

        function _salvaNuovaPosizione(nome, lat, lon, silent = false) {
            console.log(`Salvataggio: ${nome} -> ${lat}, ${lon}`);
            fetch('/save_coord', {
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome: nome, lat: lat, lon: lon })
            })
            .then(r => r.json())
            .then(d => {
                if(!silent) alert(d.msg);
                else if(d.status !== 'ok') {
                    console.error("Errore salvataggio:", d.msg);
                    alert("Errore salvataggio: " + d.msg);
                } else {
                    const status = document.getElementById('save-status');
                    status.textContent = "Posizione salvata: " + nome;
                    status.style.display = 'block';
                    setTimeout(() => status.style.display = 'none', 2000);
                }
            })
            .catch(err => {
                console.error("Network error:", err);
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

        function toggleDragging() {
            DRAGGING_ENABLED = !DRAGGING_ENABLED;
            const btn = document.getElementById('btn-toggle-drag');
            if (DRAGGING_ENABLED) {
                btn.textContent = "🔓 SPOSTA PUNTI (ON)";
                btn.style.background = "#10b981";
            } else {
                btn.textContent = "🔒 SPOSTA PUNTI (OFF)";
                btn.style.background = "#4b5563";
            }
            renderMarkers(); // Rigenera i marcatori con la nuova proprietà draggable
        }

        function updateTotals() {
            const total = DATA_ZONE.reduce((acc, z) => acc + (z.numero_consegne || 0), 0);
            document.getElementById('tot-points').textContent = `${total} Punti`;
        }

        function _get_random_palette_color() {
            const p = ["#4f46e5", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4"];
            return p[Math.floor(Math.random()*p.length)];
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
                color: _get_random_palette_color(),
                da_mappare: pointsToMove.some(p => !p.lat)
            };
            DATA_ZONE.push(newZone);
            
            sourceZone.lista_punti = sourceZone.lista_punti.filter(p => !pointsToMove.includes(p));
            sourceZone.numero_consegne = sourceZone.lista_punti.length;
            
            cancelAction();
            updateTotals();
            renderMarkers();
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
                            targetZone.da_mappare = targetZone.lista_punti.some(p => !p.lat);
                            currentPoints.splice(pIndex, 1);
                            moved++;
                        }
                    }
                }
            });
            
            if (moved > 0) {
                sourceZone.lista_punti = currentPoints;
                sourceZone.numero_consegne = sourceZone.lista_punti.length;
                sourceZone.da_mappare = sourceZone.lista_punti.some(p => !p.lat);
                cancelAction();
                updateTotals();
                renderMarkers();
            } else {
                alert("Non hai selezionato nessuno spostamento nelle tendine.");
                cancelAction();
            }
        }


        function saveAllToServer() {
            const btn = document.getElementById('btn-master-save');
            btn.textContent = "..."; btn.disabled = true;
            fetch('/save', {
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

def _carica_e_genera(data_giorno: str) -> bool:
    """
    Carica i dati JSON e genera i file HTML + KML per la data indicata.
    Ritorna True se tutto ok, False in caso di errore.
    """
    global TARGET_FILE_UNIFICATO, TARGET_FILE_VIAGGI, TARGET_FILE_2B, ZONE_LIST_CACHE, DATA_GIORNO
    DATA_GIORNO = data_giorno

    output_base = CONSEGNE_DIR / f"CONSEGNE_{DATA_GIORNO}"
    TARGET_FILE_UNIFICATO = output_base / "punti_consegna_unificati.json"
    TARGET_FILE_VIAGGI = output_base / "viaggi_giornalieri.json"
    TARGET_FILE_2B = output_base / "2b_crea_zone_consegna.json"

    if not TARGET_FILE_UNIFICATO.exists():
        print(f"[ERRORE] File non trovato: {TARGET_FILE_UNIFICATO}")
        return False

    try:
        unificato_data = json.loads(TARGET_FILE_UNIFICATO.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERRORE] Impossibile leggere il JSON: {e}")
        return False

    punti_list = unificato_data.get("punti", [])
    logger.info(f"📋 Punti caricati: {len(punti_list)}")

    # Raggruppamento per zona
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
        if not p.get("lat"):
            zone_dict[zid]["da_mappare"] = True

    ZONE_LIST_CACHE = sorted(list(zone_dict.values()), key=lambda x: str(x["id_zona"]))
    for i, z in enumerate(ZONE_LIST_CACHE, 1):
        z["nome_giro"] = f"Viaggio {i}"
        z["color"] = _get_color(i - 1)

    # ── Genera HTML statico ──
    is_locked = unificato_data.get("is_locked", False)
    _salva_html_fisico(
        output_base, HTML_TEMPLATE, DATA_GIORNO,
        json.dumps(ZONE_LIST_CACHE, ensure_ascii=False),
        GOOGLE_MAPS_API_KEY,
        is_locked
    )

    # ── Genera KML per Google My Maps ──
    kml_path = output_base / f"zone_google_{DATA_GIORNO.replace('-', '_')}.kml"
    _salva_kml(punti_list, kml_path, DATA_GIORNO)
    logger.info(f"✅ KML creato: {kml_path.name}")

    return True


def _libera_porta_5000():
    """Termina eventuali processi che occupano già la porta 5000."""
    import subprocess as _sp
    try:
        # Trova il PID che usa la porta 5000
        result = _sp.run(
            ["netstat", "-ano"],
            capture_output=True, text=True
        )
        pids_da_terminare = set()
        for line in result.stdout.splitlines():
            if ":5000 " in line and "LISTENING" in line:
                parts = line.strip().split()
                pid = parts[-1]
                if pid.isdigit():
                    pids_da_terminare.add(int(pid))

        for pid in pids_da_terminare:
            try:
                _sp.run(["taskkill", "/PID", str(pid), "/F"],
                        capture_output=True)
                print(f"  🔪 Processo precedente (PID {pid}) terminato.")
            except Exception:
                pass

        if pids_da_terminare:
            time.sleep(0.8)  # lascia il tempo al SO di rilasciare la porta
    except Exception as e:
        print(f"  ⚠️  Pulizia porta 5000: {e}")


def _avvia_server():
    """Avvia il server Flask interattivo sulla porta 5000."""
    if not HAS_FLASK:
        print("\n" + "!"*60)
        print("❌ ERRORE: Libreria 'flask' non trovata nel tuo sistema.")
        print("   Per usare la mappa interattiva, scrivi nel terminale:")
        print("   python -m pip install flask flask-cors")
        print("!"*60 + "\n")
        return

    _libera_porta_5000()  # pulizia automatica prima di avviare

    print(f"\n🌐 Flask Server avviato per la data: {DATA_GIORNO}")
    print(f"   Apri: http://127.0.0.1:5000")
    print(f"   (premi CTRL+C per fermare)\n")

    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:5000")

    threading.Thread(target=open_browser, daemon=True).start()
    try:
        app.run(port=5000, debug=False)
    except OSError as e:
        print(f"\n[ERRORE] Impossibile avviare sulla porta 5000: {e}")
        sys.exit(1)



def main():
    # Argomenti: [data] [--serve | --no-serve]
    # --no-serve : crea solo HTML+KML e termina (usato dal master script)
    # --serve    : crea HTML+KML poi avvia Flask (default quando eseguito manualmente)
    args = sys.argv[1:]
    serve_flag = True   # default: avvia il server

    # Filtra i flag
    filtered_args = []
    for a in args:
        if a == "--no-serve":
            serve_flag = False
        elif a == "--serve":
            serve_flag = True
        else:
            filtered_args.append(a)

    # Determina la data
    if filtered_args:
        data_giorno = filtered_args[0].strip()
    else:
        # Auto-detect: cartella con orario di modifica più recente
        folders = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
        if not folders:
            return print("[ERRORE] Nessuna cartella CONSEGNE trovata.")
        folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        data_giorno = folders[0].name.replace("CONSEGNE_", "")
        logger.info(f"Data auto-rilevata: {data_giorno}")

    # Genera i file
    ok = _carica_e_genera(data_giorno)
    if not ok:
        sys.exit(1)

    # Avvia Flask solo se richiesto
    if serve_flag:
        _avvia_server()
    else:
        print(f"[OK] File generati. Server Flask NON avviato (--no-serve).")


if __name__ == "__main__":
    main()

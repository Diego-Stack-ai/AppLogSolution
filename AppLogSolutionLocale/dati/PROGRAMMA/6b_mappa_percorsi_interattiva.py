"""
6b_mappa_percorsi_interattiva.py — Strumento Unificato BAT 3+
─────────────────────────────────────────────────────────────
FASE 1: Editing giri  (marker statici, DIVIDI / SPOSTA / RINOMINA)  [nessuna API]
FASE 2: Calcolo percorsi per giro  (OR-Tools + Google API, asincrono per giro)
FASE 3: Revisione post-calcolo  (frecce riordino + ricalcolo parziale dirty-flag)

Legge:  punti_consegna_unificati.json  (o viaggi_giornalieri.json se già esiste)
Scrive: viaggi_giornalieri.json  +  PERCORSI_VEGGIANO/*.html
"""

import json, sys, time, threading, webbrowser, queue, re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS

# ── Import funzioni core da BAT 3 (evita duplicazione di codice) ──────────────
import importlib.util as _ilu
def _load_bat3():
    p = Path(__file__).parent / "6_genera_percorsi_veggiano.py"
    spec = _ilu.spec_from_file_location("bat3_core", p)
    m = _ilu.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
bat3 = _load_bat3()
# ─────────────────────────────────────────────────────────────────────────────

PROG_DIR         = Path(__file__).resolve().parent
BASE_DIR         = PROG_DIR.parent
CONSEGNE_DIR     = BASE_DIR / "CONSEGNE"
GOOGLE_MAPS_API_KEY = bat3.GOOGLE_MAPS_API_KEY

COLORI = ["#4f46e5","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4",
          "#ec4899","#84cc16","#f97316","#6366f1","#14b8a6","#a855f7",
          "#eab308","#22c55e","#3b82f6"]

NOMI_DNR      = ["BS","FUORI BS","LAGO BS 1","LAGO BS 2","LAGO BS 3",
                 "VR","FUORI VR","MN","VR MN",
                 "LAGO VR 1","LAGO VR 2","LAGO VR 3"]
NOMI_GRANCHEF = ["GranChef " + n for n in NOMI_DNR]

# ── Stato globale (thread-safe) ───────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

DATA_GIORNO = ""
TARGET_DIR  = None
ZONE_CACHE  = []      # lista giri in memoria (fonte di verità)
STATO_GIRI  = {}      # {id_zona: {stato, polylines, stats, err}}
_lock       = threading.Lock()
_sse_queues = []      # code SSE per broadcast ai client
_executor   = ThreadPoolExecutor(max_workers=3)

# ── Utility ───────────────────────────────────────────────────────────────────
def _get_latest_dir():
    dirs = [d for d in CONSEGNE_DIR.iterdir()
            if d.is_dir() and d.name.startswith("CONSEGNE_")]
    if not dirs: return None
    return max(dirs, key=lambda d: d.stat().st_mtime)

def _colore(i): return COLORI[i % len(COLORI)]

def _broadcast(event, data):
    """Invia un evento SSE a tutti i client connessi."""
    msg  = f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
    dead = []
    for q in _sse_queues:
        try: q.put_nowait(msg)
        except: dead.append(q)
    for d in dead:
        try: _sse_queues.remove(d)
        except: pass

# ── Caricamento dati ──────────────────────────────────────────────────────────
def _carica_dati(data_dir: Path) -> bool:
    global ZONE_CACHE, STATO_GIRI, DATA_GIORNO, TARGET_DIR
    TARGET_DIR  = data_dir
    DATA_GIORNO = data_dir.name.replace("CONSEGNE_", "")

    viaggi_path = data_dir / "viaggi_giornalieri.json"
    unif_path   = data_dir / "punti_consegna_unificati.json"

    if viaggi_path.exists():
        # Lavoro già iniziato → ripristina da viaggi_giornalieri.json
        raw = json.loads(viaggi_path.read_text(encoding="utf-8"))
        ZONE_CACHE = raw if isinstance(raw, list) else []
    elif unif_path.exists():
        # Primo avvio → leggi unificati e raggruppa per zona
        unif      = json.loads(unif_path.read_text(encoding="utf-8"))
        punti_raw = unif.get("punti", []) if isinstance(unif, dict) else unif

        zone_dict: dict = {}
        for p in punti_raw:
            zona = p.get("zona") or "SENZA_ZONA"
            zone_dict.setdefault(zona, []).append(p)

        def sort_key(zid):
            if zid == "DDT_DA_INSERIRE": return "zzz_" + zid
            if zid == "SENZA_ZONA":      return "zzy_" + zid
            if zid.startswith("GranChef"): return "m_" + zid
            return "a_" + zid

        ZONE_CACHE = []
        i = 0
        for zid in sorted(zone_dict.keys(), key=sort_key):
            pts      = zone_dict[zid]
            is_gc    = zid.startswith("GranChef")
            is_spec  = zid in ("DDT_DA_INSERIRE", "SENZA_ZONA")
            nome     = zid.replace("_", " ") if (is_gc or is_spec) else f"V{i+1:02d}"
            ZONE_CACHE.append({
                "id_zona":    zid,
                "nome_giro":  nome,
                "color":      _colore(i),
                "lista_punti": pts
            })
            if not is_spec: i += 1
    else:
        return False

    # Inizializza stati
    STATO_GIRI = {}
    for z in ZONE_CACHE:
        zid = z.get("id_zona", "")
        if zid not in ("DDT_DA_INSERIRE",):
            STATO_GIRI[zid] = {"stato": "da_calcolare", "polylines": [], "stats": {}, "err": ""}
    return True

# ── Calcolo asincrono per singolo giro ────────────────────────────────────────
def _calcola_giro(zid: str, punti: list, usa_or_tools: bool = True):
    """Calcola percorso ottimizzato per un giro. Gira in thread separato."""
    try:
        with _lock:
            if zid in STATO_GIRI:
                STATO_GIRI[zid].update({"stato": "in_elaborazione", "err": ""})
        _broadcast("stato_giro", {"id_zona": zid, "stato": "in_elaborazione"})

        depot = bat3.get_depot_for_points(punti)
        perc  = bat3.ottimizza_percorso(punti, depot) if usa_or_tools else list(punti)
        km, t_guida, t_sosta, t_tot, polylines = bat3.get_google_trip_data(perc, depot)

        is_gc = any("GRAND" in str(p.get("tipologia_grado","")).upper() or
                    "CHEF"  in str(p.get("tipologia_grado","")).upper()
                    for p in perc)
        tot_ddt = 0
        if not is_gc:
            for p in perc:
                tot_ddt += len([c for c in p.get("codici_ddt_frutta",[]) if c and c != "p00000"])
                tot_ddt += len([c for c in p.get("codici_ddt_latte",  []) if c and c != "p00000"])
                if not p.get("codici_ddt_frutta") and not p.get("codici_ddt_latte"):
                    if p.get("codice_frutta") and p.get("codice_frutta") != "p00000": tot_ddt += 1
                    if p.get("codice_latte")  and p.get("codice_latte")  != "p00000": tot_ddt += 1

        stats = {
            "km": km, "t_guida": t_guida, "t_sosta": t_sosta, "t_tot": t_tot,
            "tot_ddt": tot_ddt,
            "fatturato": f"{tot_ddt * 16.50:.2f}" if not is_gc else "GranChef",
            "depot": depot["nome"], "is_gc": is_gc
        }

        with _lock:
            for z in ZONE_CACHE:
                if z["id_zona"] == zid:
                    z["lista_punti"] = perc
                    break
            STATO_GIRI[zid].update({"stato": "calcolato", "polylines": polylines, "stats": stats, "err": ""})

        _broadcast("stato_giro", {
            "id_zona": zid, "stato": "calcolato",
            "polylines": polylines, "stats": stats, "punti": perc
        })

    except Exception as e:
        with _lock:
            if zid in STATO_GIRI:
                STATO_GIRI[zid].update({"stato": "errore", "err": str(e)})
        _broadcast("stato_giro", {"id_zona": zid, "stato": "errore", "err": str(e)})

# ── Flask routes ──────────────────────────────────────────────────────────────
@app.after_request
def _no_cache(r):
    r.headers["Cache-Control"] = "no-store, no-cache"
    return r

@app.route("/")
def index():
    return HTML_TEMPLATE.replace("{{DATA_GIORNO}}", DATA_GIORNO) \
                        .replace("{{GOOGLE_MAPS_API_KEY}}", GOOGLE_MAPS_API_KEY) \
                        .replace("{{NOMI_DNR_JS}}", json.dumps(NOMI_DNR)) \
                        .replace("{{NOMI_GC_JS}}",  json.dumps(NOMI_GRANCHEF)) \
                        .replace("{{POPUP_MODE}}", "false")

@app.route("/sidebar")
def sidebar():
    """Pannello di controllo standalone per secondo schermo (aperto via window.open)."""
    return HTML_TEMPLATE.replace("{{DATA_GIORNO}}", DATA_GIORNO) \
                        .replace("{{GOOGLE_MAPS_API_KEY}}", GOOGLE_MAPS_API_KEY) \
                        .replace("{{NOMI_DNR_JS}}", json.dumps(NOMI_DNR)) \
                        .replace("{{NOMI_GC_JS}}",  json.dumps(NOMI_GRANCHEF)) \
                        .replace("{{POPUP_MODE}}", "true")

@app.route("/api/zone")
def api_zone():
    return jsonify(ZONE_CACHE)

@app.route("/api/stati")
def api_stati():
    return jsonify(STATO_GIRI)

@app.route("/api/save", methods=["POST"])
def api_save():
    global ZONE_CACHE
    try:
        ZONE_CACHE = request.json
        (TARGET_DIR / "viaggi_giornalieri.json").write_text(
            json.dumps(ZONE_CACHE, indent=2, ensure_ascii=False), encoding="utf-8")
        with _lock:
            for z in ZONE_CACHE:
                zid = z.get("id_zona")
                if zid and zid not in ("DDT_DA_INSERIRE",):
                    STATO_GIRI.setdefault(zid, {
                        "stato":"da_calcolare","polylines":[],"stats":{},"err":""})
                    # Marca modificato se era calcolato e ora cambia
                    if STATO_GIRI[zid].get("stato") == "calcolato":
                        STATO_GIRI[zid]["stato"] = "modificato"
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "err": str(e)}), 500

@app.route("/api/calcola", methods=["POST"])
def api_calcola():
    """Avvia calcolo asincrono. Se id_zone è [], calcola tutto."""
    try:
        body      = request.json or {}
        id_zone   = body.get("id_zone", [])
        or_tools  = body.get("usa_or_tools", True)
        avviati   = []
        with _lock:
            snapshot = [(z["id_zona"], list(z["lista_punti"])) for z in ZONE_CACHE
                        if z.get("id_zona") not in ("DDT_DA_INSERIRE",)
                        and z.get("lista_punti")
                        and (not id_zone or z["id_zona"] in id_zone)]
        for zid, punti in snapshot:
            _executor.submit(_calcola_giro, zid, punti, or_tools)
            avviati.append(zid)
        return jsonify({"ok": True, "avviati": avviati})
    except Exception as e:
        return jsonify({"ok": False, "err": str(e)}), 500

@app.route("/api/riordina", methods=["POST"])
def api_riordina():
    """Salva ordine manuale fermate. Marca giro come modificato → ricalcolo solo Directions."""
    try:
        body  = request.json
        zid   = body["id_zona"]
        nuovi = body["lista_punti"]
        with _lock:
            for z in ZONE_CACHE:
                if z["id_zona"] == zid:
                    z["lista_punti"] = nuovi
                    break
            if zid in STATO_GIRI:
                STATO_GIRI[zid]["stato"] = "modificato"
        (TARGET_DIR / "viaggi_giornalieri.json").write_text(
            json.dumps(ZONE_CACHE, indent=2, ensure_ascii=False), encoding="utf-8")
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "err": str(e)}), 500

@app.route("/api/dividi", methods=["POST"])
def api_dividi():
    """Divide un giro: sposta le fermate agli indici indicati in un nuovo sub-giro."""
    try:
        body   = request.json
        zid    = body["id_zona"]
        indici = set(body["indici"])  # indici delle fermate da spostare

        with _lock:
            zona_orig = next((z for z in ZONE_CACHE if z["id_zona"] == zid), None)
            if not zona_orig:
                return jsonify({"ok": False, "err": f"Zona {zid} non trovata"}), 400

            punti_orig = zona_orig["lista_punti"]
            if len(indici) >= len(punti_orig):
                return jsonify({"ok": False, "err": "Devi lasciare almeno una fermata"}), 400

            # Separa le fermate
            rimanenti  = [p for i, p in enumerate(punti_orig) if i not in indici]
            spostate   = [p for i, p in enumerate(punti_orig) if i in indici]

            # Genera nuovo id_zona univoco
            base = zid
            idx  = 2
            while any(z["id_zona"] == f"{base}_{idx}" for z in ZONE_CACHE):
                idx += 1
            nuovo_zid = f"{base}_{idx}"

            # Aggiorna zona originale
            zona_orig["lista_punti"] = rimanenti

            # Crea nuova zona
            colori = ["#4f46e5","#059669","#d97706","#dc2626","#7c3aed",
                      "#0891b2","#65a30d","#db2777","#ea580c","#0284c7"]
            nuovo_color = colori[len(ZONE_CACHE) % len(colori)]
            nuova_zona = {
                "id_zona":    nuovo_zid,
                "nome_giro":  nuovo_zid.replace("_", " "),
                "color":      nuovo_color,
                "lista_punti": spostate
            }
            ZONE_CACHE.append(nuova_zona)

        # Salva JSON aggiornato
        (TARGET_DIR / "viaggi_giornalieri.json").write_text(
            json.dumps(ZONE_CACHE, indent=2, ensure_ascii=False), encoding="utf-8")

        return jsonify({"ok": True, "nuovo_id": nuovo_zid, "zone": ZONE_CACHE})
    except Exception as e:
        return jsonify({"ok": False, "err": str(e)}), 500

@app.route("/api/genera", methods=["POST"])
def api_genera():
    """Genera file HTML finali per tutti i giri (PERCORSI_VEGGIANO + RIEPILOGO)."""
    try:
        out_dir = TARGET_DIR / "PERCORSI_VEGGIANO"
        if out_dir.exists():
            for f in out_dir.glob("*.html"):
                try: f.unlink()
                except: pass
        out_dir.mkdir(exist_ok=True)

        summary = []
        for z in ZONE_CACHE:
            zid   = z.get("id_zona")
            if not zid or zid == "DDT_DA_INSERIRE": continue
            punti = z.get("lista_punti", [])
            if not punti: continue

            st    = STATO_GIRI.get(zid, {})
            poly  = st.get("polylines", [])
            stats = st.get("stats", {})
            km    = stats.get("km", 0)
            t_g   = stats.get("t_guida", 0)
            t_s   = stats.get("t_sosta", 0)
            t_tot = stats.get("t_tot", 0)

            v_id   = z.get("nome_giro") or zid
            z_str  = ", ".join(sorted(set(str(p.get("zona","")) for p in punti)))
            depot  = bat3.get_depot_for_points(punti)
            is_gc  = stats.get("is_gc", False)
            tot_ddt    = stats.get("tot_ddt", 0)
            fatturato  = stats.get("fatturato", "0.00")

            fname = bat3.sanitize_filename(f"{v_id}_Zone_{zid}.html")
            bat3.genera_html_giro(v_id, z_str, punti,
                                  (km, t_g, t_s, t_tot),
                                  poly, out_dir / fname, depot)
            summary.append({
                "v_id": v_id, "zone_str": z_str, "fname": fname,
                "km": km, "t_guida": t_g, "t_sosta": t_s, "t_tot": t_tot,
                "punti": len(punti), "tot_ddt": tot_ddt,
                "fatturato": fatturato, "is_grand_chef": is_gc
            })

        bat3.gera_riepilogo(summary, out_dir / "RIEPILOGO_GIRI.html")
        # viaggi_giornalieri.json = tutto (incluso GranChef, DDT ecc.)
        (TARGET_DIR / "viaggi_giornalieri.json").write_text(
            json.dumps(ZONE_CACHE, indent=2, ensure_ascii=False), encoding="utf-8")

        # viaggi_giornalieri_OTTIMIZZATO.json = tutti i giri con autista assegnato
        # Escluse solo le zone tecniche senza consegna reale
        ZONE_ESCLUSE = {"DDT_DA_INSERIRE", "SENZA_ZONA"}
        zone_ottimizzato = [
            z for z in ZONE_CACHE
            if z.get("id_zona") not in ZONE_ESCLUSE
            and z.get("lista_punti")   # solo zone con almeno un punto
        ]
        (TARGET_DIR / "viaggi_giornalieri_OTTIMIZZATO.json").write_text(
            json.dumps(zone_ottimizzato, indent=2, ensure_ascii=False), encoding="utf-8")

        return jsonify({"ok": True, "giri": len(summary), "out": str(out_dir)})
    except Exception as e:
        return jsonify({"ok": False, "err": str(e)}), 500

@app.route("/api/sse")
def api_sse():
    """Server-Sent Events: stream real-time aggiornamenti al browser."""
    q = queue.Queue(maxsize=200)
    _sse_queues.append(q)
    def generate():
        try:
            yield f"event: connected\ndata: {{}}\n\n"
            while True:
                try:
                    msg = q.get(timeout=25)
                    yield msg
                except queue.Empty:
                    yield ": keepalive\n\n"
        except GeneratorExit:
            try: _sse_queues.remove(q)
            except: pass
    return Response(stream_with_context(generate()),
                    mimetype="text/event-stream",
                    headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"})

# ── HTML Template ─────────────────────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mappa Percorsi Interattiva — {{DATA_GIORNO}}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;display:flex;height:100vh;overflow:hidden;background:#0f172a;}
:root{--p:#4f46e5;--s:#10b981;--w:#f59e0b;--d:#ef4444;--bg:#f8fafc;--card:#fff;--border:#e2e8f0;--txt:#1e293b;--sub:#64748b;}

/* ── SIDEBAR ── */
#sidebar{width:420px;min-width:300px;background:var(--bg);display:flex;flex-direction:column;border-right:1px solid var(--border);overflow:hidden;position:relative;z-index:10;}
/* ── FLOATING SIDEBAR ── */
#sidebar.floating{position:fixed!important;z-index:9999;border-radius:16px;box-shadow:0 24px 64px rgba(0,0,0,0.45);border:1.5px solid rgba(255,255,255,0.08);overflow:hidden;width:400px!important;}
#sidebar.floating #hdr{cursor:grab;border-radius:14px 14px 0 0;}
#sidebar.floating #hdr.dragging{cursor:grabbing;}
#sidebar.floating #zone-list{max-height:calc(100vh - 180px);}
#sidebar.snap-back{transition:box-shadow 0.35s ease,border-radius 0.35s ease;}
.btn-sgancia{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);color:#94a3b8;border-radius:7px;padding:3px 8px;font-size:0.8rem;cursor:pointer;transition:all 0.2s;line-height:1;flex-shrink:0;}
.btn-sgancia:hover{background:rgba(255,255,255,0.18);color:#fff;}
.btn-sgancia.active{background:rgba(79,70,229,0.4);border-color:#4f46e5;color:#a5b4fc;}
/* Popup mode (secondo schermo) */
body.popup-mode{display:block!important;overflow:auto;}
body.popup-mode #sidebar{width:100vw!important;height:100vh!important;border-right:none;}
body.popup-mode #map{display:none!important;}
body.popup-mode .btns-sgancia-wrap{display:none!important;}

/* ── HEADER ── */
#hdr{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:14px 16px;flex-shrink:0;}
#hdr .logo{color:#fff;font-size:1rem;font-weight:800;letter-spacing:-0.3px;display:flex;align-items:center;gap:8px;}
#hdr .logo span{font-size:1.2rem;}
#hdr .data-badge{background:rgba(255,255,255,0.1);color:#94a3b8;font-size:0.7rem;font-weight:600;padding:2px 8px;border-radius:20px;margin-top:6px;display:inline-block;}
.hdr-btns{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;}

/* ── PULSANTI HEADER ── */
.btn-hdr{border:none;border-radius:8px;font-family:'Inter',sans-serif;font-size:0.72rem;font-weight:700;cursor:pointer;padding:7px 12px;transition:all 0.2s;display:flex;align-items:center;gap:4px;}
.btn-salva{background:#10b981;color:#fff;}
.btn-salva:hover{background:#059669;}
.btn-calcola{background:var(--p);color:#fff;}
.btn-calcola:hover{background:#4338ca;}
.btn-calcola:disabled{background:#475569;cursor:not-allowed;}
.btn-genera{background:#f59e0b;color:#fff;}
.btn-genera:hover{background:#d97706;}
.btn-genera:disabled{background:#475569;cursor:not-allowed;}
.btn-aggiorna{background:#8b5cf6;color:#fff;}
.btn-aggiorna:hover{background:#7c3aed;}
.btn-aggiorna:disabled{background:#475569;cursor:not-allowed;display:none;}
.btn-lock{font-weight:800;letter-spacing:0.3px;}
.btn-lock.locked{background:#ef4444;color:#fff;}
.btn-lock.locked:hover{background:#dc2626;}
.btn-lock.unlocked{background:#10b981;color:#fff;}
.btn-lock.unlocked:hover{background:#059669;}

/* Matita nell'header card */
.btn-matita{background:none;border:1.5px solid #e2e8f0;border-radius:50%;width:30px;height:30px;cursor:pointer;font-size:0.85rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s;margin-left:4px;}
.btn-matita:hover{background:#eef2ff;border-color:#4f46e5;transform:scale(1.1);}

/* ── FASE INDICATOR ── */
#fase-bar{display:flex;gap:0;margin-top:10px;}
.fase-pill{flex:1;text-align:center;padding:4px 6px;font-size:0.65rem;font-weight:700;border-radius:0;cursor:default;color:#475569;background:rgba(255,255,255,0.05);}
.fase-pill:first-child{border-radius:6px 0 0 6px;}
.fase-pill:last-child{border-radius:0 6px 6px 0;}
.fase-pill.active{background:var(--p);color:#fff;}
.fase-pill.done{background:#10b981;color:#fff;}

/* ── ZONA LISTA ── */
#zone-list{flex:1;overflow-y:auto;padding:12px 10px;}
#zone-list::-webkit-scrollbar{width:5px;}
#zone-list::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:4px;}

/* ── ZONE CARD ── */
.zone-card{background:var(--card);border:1.5px solid var(--border);border-radius:12px;margin-bottom:10px;overflow:hidden;transition:box-shadow 0.2s;}
.zone-card:hover{box-shadow:0 4px 16px rgba(0,0,0,0.08);}
.zone-card.active{border-color:var(--p);box-shadow:0 0 0 3px rgba(79,70,229,0.12);}
.zc-head{display:flex;align-items:center;gap:10px;padding:11px 14px;cursor:pointer;}
.zc-pill{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:0.78rem;flex-shrink:0;}
.zc-info{flex:1;min-width:0;}
.zc-name{font-size:0.9rem;font-weight:800;color:var(--txt);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:6px;}
.zc-sub{font-size:0.7rem;color:var(--sub);margin-top:1px;}
.zc-badge{font-size:0.6rem;font-weight:700;padding:2px 6px;border-radius:4px;white-space:nowrap;}
.badge-calcolato{background:#d1fae5;color:#065f46;}
.badge-elaborazione{background:#dbeafe;color:#1e40af;animation:pulse 1.5s infinite;}
.badge-modificato{background:#fef3c7;color:#92400e;}
.badge-errore{background:#fee2e2;color:#991b1b;}
.badge-da-calcolare{background:#f1f5f9;color:#64748b;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.6;}}

/* Stats barra */
.zc-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:0 14px 10px;border-top:1px solid var(--border);margin-top:-2px;}
.stat-item{text-align:center;padding:6px 4px;background:#f8fafc;border-radius:6px;}
.stat-val{font-size:0.85rem;font-weight:800;color:var(--txt);}
.stat-lbl{font-size:0.58rem;color:var(--sub);font-weight:600;text-transform:uppercase;margin-top:1px;}

/* Corpo card espanso */
.zc-body{padding:10px 14px;border-top:1px solid var(--border);display:none;}
.zc-body.open{display:block;}

/* Punti lista */
.point-row{display:flex;align-items:center;gap:8px;padding:6px 8px;background:#f8fafc;border-radius:8px;margin-bottom:5px;border:1px solid var(--border);transition:background 0.15s;}
.point-row:hover{background:#eef2ff;}
.pt-num{width:22px;height:22px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:800;flex-shrink:0;}
.pt-info{flex:1;min-width:0;}
.pt-nome{font-size:0.78rem;font-weight:700;color:var(--txt);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pt-addr{font-size:0.65rem;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.pt-eta{font-size:0.65rem;color:var(--p);font-weight:700;white-space:nowrap;}
.pt-arrow-btns{display:flex;flex-direction:column;gap:2px;}
.pt-arrow{background:none;border:1px solid var(--border);border-radius:4px;width:20px;height:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:0.65rem;color:var(--sub);transition:all 0.15s;}
.pt-arrow:hover{background:var(--p);border-color:var(--p);color:#fff;}
.pt-arrow:disabled{opacity:0.3;cursor:not-allowed;}

/* Pulsanti azione zona */
.zc-actions{display:flex;gap:6px;padding:8px 14px 12px;}
.btn-zona{flex:1;border:none;border-radius:7px;padding:7px 4px;font-size:0.7rem;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif;transition:all 0.2s;}
.btn-dividi{background:#eef2ff;color:var(--p);}
.btn-dividi:hover{background:var(--p);color:#fff;}
/* Occhio visibilita zona sulla mappa */
.btn-eye{background:none;border:1.5px solid #e2e8f0;border-radius:50%;width:28px;height:28px;cursor:pointer;font-size:0.82rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s;margin-left:2px;}
.btn-eye:hover{background:#f1f5f9;}
.btn-eye.hidden-zone{background:#fef3c7;border-color:#f59e0b;}
/* Modalita DIVIDI */
.dividi-mode .point-row{cursor:pointer;border-radius:6px;}
.dividi-mode .point-row:hover{background:#eff6ff!important;}
.point-row.dividi-sel{background:#dbeafe!important;border-color:#3b82f6!important;}
.dividi-bar{background:#3b82f6;color:#fff;padding:7px 10px;border-radius:8px;font-size:0.72rem;font-weight:700;display:flex;align-items:center;gap:6px;margin-bottom:6px;flex-wrap:wrap;}
.dividi-bar button{background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.4);color:#fff;border-radius:6px;padding:3px 9px;cursor:pointer;font-size:0.7rem;font-weight:700;}
.dividi-bar button:hover{background:rgba(255,255,255,0.35);}
.dividi-bar .btn-annulla{background:rgba(239,68,68,0.3);border-color:rgba(239,68,68,0.5);}
.btn-sposta{background:#f0fdf4;color:#059669;}
.btn-sposta:hover{background:#10b981;color:#fff;}
.btn-rinomina{background:#fefce8;color:#92400e;}
.btn-rinomina:hover{background:#f59e0b;color:#fff;}
.btn-ricalcola-giro{background:#ede9fe;color:#7c3aed;}
.btn-ricalcola-giro:hover{background:#8b5cf6;color:#fff;}

/* sposta overlay */
#sposta-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:100;display:none;align-items:center;justify-content:center;}
#sposta-overlay.open{display:flex;}
.sposta-box{background:#fff;border-radius:16px;padding:24px;max-width:380px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,0.3);}
.sposta-title{font-size:1rem;font-weight:800;color:var(--txt);margin-bottom:4px;}
.sposta-sub{font-size:0.78rem;color:var(--sub);margin-bottom:16px;}
.sposta-chips{display:flex;flex-wrap:wrap;gap:8px;}
.sposta-chip{padding:6px 14px;border-radius:20px;border:2px solid var(--border);font-size:0.75rem;font-weight:700;cursor:pointer;transition:all 0.2s;}
.sposta-chip:hover{border-color:var(--p);color:var(--p);}
.sposta-cancel{width:100%;margin-top:14px;border:none;background:#f1f5f9;border-radius:8px;padding:8px;font-size:0.75rem;font-weight:700;cursor:pointer;color:var(--sub);}

/* MODAL RINOMINA */
#modal-overlay{position:fixed;inset:0;background:rgba(15,23,42,0.6);z-index:200;display:none;align-items:center;justify-content:center;backdrop-filter:blur(4px);}
#modal-overlay.open{display:flex;}
.modal-box{background:#fff;border-radius:20px;padding:28px;width:360px;box-shadow:0 24px 64px rgba(0,0,0,0.25);}
.modal-title{font-size:1.05rem;font-weight:800;color:var(--txt);margin-bottom:4px;}
.modal-sub{font-size:0.78rem;color:var(--sub);margin-bottom:18px;}
.modal-box select,.modal-box input{width:100%;border:1.5px solid var(--border);border-radius:10px;padding:10px 12px;font-size:0.85rem;font-family:'Inter',sans-serif;outline:none;margin-bottom:10px;}
.modal-box select:focus,.modal-box input:focus{border-color:var(--p);}
.modal-btns{display:flex;gap:10px;margin-top:6px;}
.modal-ok{flex:1;background:var(--p);color:#fff;border:none;border-radius:10px;padding:10px;font-weight:700;cursor:pointer;font-size:0.85rem;}
.modal-cancel{flex:1;background:#f1f5f9;color:var(--sub);border:none;border-radius:10px;padding:10px;font-weight:700;cursor:pointer;font-size:0.85rem;}

/* TOAST */
#toast{position:fixed;bottom:24px;right:24px;background:#1e293b;color:#fff;padding:12px 20px;border-radius:12px;font-size:0.8rem;font-weight:600;z-index:999;opacity:0;transition:opacity 0.3s;pointer-events:none;max-width:320px;}
#toast.show{opacity:1;}

/* MAPPA */
#map{flex:1;height:100vh;}

/* Responsive */
@media(max-width:768px){
  #sidebar{width:100%;height:50vh;}
  body{flex-direction:column;}
  #map{height:50vh;}
}
</style>
</head>
<body>

<!-- SPOSTA OVERLAY -->
<div id="sposta-overlay">
  <div class="sposta-box">
    <div class="sposta-title">↔ Sposta consegna</div>
    <div class="sposta-sub" id="sposta-sub-txt"></div>
    <div class="sposta-chips" id="sposta-chips"></div>
    <button class="sposta-cancel" onclick="chiudiSposta()">Annulla</button>
  </div>
</div>

<!-- MODAL RINOMINA -->
<div id="modal-overlay">
  <div class="modal-box">
    <div class="modal-title" id="modal-title">✏️ Rinomina giro</div>
    <div class="modal-sub" id="modal-sub"></div>
    <select id="modal-select" onchange="onSelectChange()">
      <option value="">— Seleziona nome —</option>
    </select>
    <input id="modal-input" type="text" placeholder="Oppure scrivi nome personalizzato…">
    <div class="modal-btns">
      <button class="modal-ok" onclick="salvaRinomina()">Salva</button>
      <button class="modal-cancel" onclick="chiudiModal()">Annulla</button>
    </div>
  </div>
</div>

<!-- TOAST -->
<div id="toast"></div>

<!-- SIDEBAR -->
<div id="sidebar">
  <div id="hdr">
    <div class="logo" style="justify-content:space-between;"><span style="display:flex;align-items:center;gap:8px;"><span>🗺️</span> Mappa Percorsi Interattiva</span><span class="btns-sgancia-wrap" style="display:flex;gap:4px;"><button class="btn-sgancia" id="btn-sgancia" onclick="toggleSgancia(event)" title="Sgancia pannello (galleggiante)">&#10697;</button><button class="btn-sgancia" id="btn-popup" onclick="apriPopup(event)" title="Apri su secondo schermo">&#8599;</button></span></div>
    <div class="data-badge">{{DATA_GIORNO}}</div>
    <div class="hdr-btns">
      <button class="btn-hdr btn-lock locked" id="btn-lock" onclick="toggleLock()">BLOCCATA 🔒</button>
      <button class="btn-hdr btn-calcola" id="btn-calcola" onclick="calcolaTutto()">▶ Calcola percorsi</button>
      <button class="btn-hdr btn-aggiorna" id="btn-aggiorna" onclick="aggiornaModificati()" style="display:none;">🔄 Aggiorna modificati</button>
      <button class="btn-hdr btn-genera" id="btn-genera" onclick="generaFile()" disabled>💾 Salva e Genera file</button>
    </div>
    <div id="fase-bar">
      <div class="fase-pill active" id="fase1-pill">1 · Editing</div>
      <div class="fase-pill" id="fase2-pill">2 · Calcolo</div>
      <div class="fase-pill" id="fase3-pill">3 · Revisione</div>
    </div>
  </div>
  <div id="zone-list"></div>
</div>

<!-- MAPPA -->
<div id="map"></div>

<script>
// ── Costanti ────────────────────────────────────────────────────────────────
const IS_POPUP      = {{POPUP_MODE}};  // true quando aperto come popup secondo schermo
if(IS_POPUP){
  document.body.classList.add('popup-mode');
  // Se la finestra principale viene chiusa → chiudi anche questo popup
  setInterval(()=>{
    try{ if(!window.opener || window.opener.closed) window.close(); }
    catch(e){ window.close(); } // errore cross-origin = opener sparito
  }, 1000);
}
const NOMI_DNR      = {{NOMI_DNR_JS}};
const NOMI_GC       = {{NOMI_GC_JS}};
const API_KEY       = "{{GOOGLE_MAPS_API_KEY}}";

// ── Stato applicazione ───────────────────────────────────────────────────────
let ZONE      = [];          // lista giri (fonte verità locale)
let STATI     = {};          // {id_zona: {stato, polylines, stats}}
let gMap      = null;        // istanza Google Map
let gMarkers  = [];          // tutti i AdvancedMarker
let gInfoWindow = null;      // InfoWindow attivo sul marker
let gPolylines= {};          // {id_zona: [google.maps.Polyline]}
let activeZid = null;        // id zona espansa
let faseCorrente = 1;
let isLocked  = true;        // default: bloccato (come BAT 2)

// Stato operazioni editing
let spostaPunto   = null;    // {punto, fromZid}
let dividiZid     = null;    // zid in modalita DIVIDI
let dividiSel     = new Set(); // indici fermate selezionate
let ZONE_HIDDEN   = new Set(); // zid nascosti dalla mappa
let modalZid      = null;

// ── Funzioni di supporto ─────────────────────────────────────────────────────
function toast(msg, ms=2800){
  const el=document.getElementById('toast');
  el.textContent=msg; el.classList.add('show');
  setTimeout(()=>el.classList.remove('show'), ms);
}

function fmtMin(m){
  if(!m && m!==0) return '--';
  m=Math.round(m);
  return m>=60 ? `${Math.floor(m/60)}h ${m%60}m` : `${m}m`;
}

function colorContrast(hex){
  const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
  return (r*299+g*587+b*114)/1000>128 ? '#1e293b' : '#ffffff';
}

function badgeStato(stato){
  const m={
    'calcolato':'badge-calcolato',
    'in_elaborazione':'badge-elaborazione',
    'modificato':'badge-modificato',
    'errore':'badge-errore',
    'da_calcolare':'badge-da-calcolare'
  };
  const labels={
    'calcolato':'✅ Pronto','in_elaborazione':'⏳ Calcolo...','modificato':'🔄 Modificato',
    'errore':'❌ Errore','da_calcolare':'⏸ Da calcolare'
  };
  const cls=m[stato]||'badge-da-calcolare';
  return `<span class="zc-badge ${cls}">${labels[stato]||stato}</span>`;
}

// ── Caricamento iniziale ──────────────────────────────────────────────────────
async function init(){
  const [zoneRes, statiRes] = await Promise.all([
    fetch('/api/zone').then(r=>r.json()),
    fetch('/api/stati').then(r=>r.json())
  ]);
  ZONE  = zoneRes;
  STATI = statiRes;
  renderSidebar();
  if(!IS_POPUP){
    await initMap();
    renderMarkers();
    renderPolylines();
  }
  // Rimuovi silenziosamente i giri vuoti appena caricati (es. da BAT 2 con zone extra)
  await pulisciZoneVuote(true);
  connectSSE();
  aggiornaFase();
}

// ── SSE ───────────────────────────────────────────────────────────────────────
function connectSSE(){
  const es = new EventSource('/api/sse');
  es.addEventListener('stato_giro', e=>{
    const d = JSON.parse(e.data);
    const zid = d.id_zona;
    if(!STATI[zid]) STATI[zid]={};
    Object.assign(STATI[zid], {stato:d.stato, polylines:d.polylines||STATI[zid].polylines||[], stats:d.stats||STATI[zid].stats||{}});
    if(d.punti){
      const z=ZONE.find(x=>x.id_zona===zid);
      if(z) z.lista_punti=d.punti;
    }
    renderCardById(zid);
    if(d.polylines && d.polylines.length) renderPolylinesZona(zid, d.polylines, ZONE.find(x=>x.id_zona===zid)?.color||'#4f46e5');
    aggiornaFase();
    if(d.stato==='calcolato') toast(`✅ ${ZONE.find(x=>x.id_zona===zid)?.nome_giro||zid} calcolato!`);
    if(d.stato==='errore')    toast(`❌ Errore su ${zid}: ${d.err||''}`, 5000);
  });
  es.addEventListener('connected', ()=>console.log('SSE connesso'));
  es.onerror=()=>setTimeout(connectSSE, 3000);
}

// ── Fase indicator ────────────────────────────────────────────────────────────
function aggiornaFase(){
  const stati    = Object.values(STATI).map(s=>s.stato);
  const tuttiCal = stati.length>0 && stati.every(s=>s==='calcolato');
  const alcuniCal= stati.some(s=>s==='calcolato');
  const inCalc   = stati.some(s=>s==='in_elaborazione');
  const modificati = stati.filter(s=>s==='modificato').length;

  document.getElementById('fase1-pill').className = 'fase-pill ' + (alcuniCal?'done':'active');
  document.getElementById('fase2-pill').className = 'fase-pill ' + (inCalc?'active':(alcuniCal?'done':''));
  document.getElementById('fase3-pill').className = 'fase-pill ' + (tuttiCal?'active':'');

  document.getElementById('btn-calcola').disabled = inCalc;

  // Genera abilitato SOLO se tutti i giri sono calcolati e nessuno in modifica
  const prontoPerGenerare = tuttiCal && modificati === 0 && !inCalc;
  const btnGenera = document.getElementById('btn-genera');
  btnGenera.disabled = !prontoPerGenerare;
  btnGenera.title = !prontoPerGenerare
    ? (inCalc ? 'Attendi il completamento del calcolo…' :
       modificati > 0 ? 'Clicca prima su Aggiorna modificati' :
       'Calcola tutti i percorsi prima di generare')
    : 'Salva e genera i file per BAT 5';

  const btnAgg = document.getElementById('btn-aggiorna');
  if(modificati > 0){ btnAgg.style.display='flex'; btnAgg.textContent=`🔄 Aggiorna (${modificati})`; }
  else { btnAgg.style.display='none'; }
}

// ── Render sidebar ────────────────────────────────────────────────────────────
function renderSidebar(){
  const list = document.getElementById('zone-list');
  list.innerHTML = ZONE.map(z=>renderCard(z)).join('');
}

function renderCard(z){
  const zid    = z.id_zona;
  const isSpec = zid==='DDT_DA_INSERIRE' || zid==='SENZA_ZONA';
  const st     = STATI[zid]||{stato:'da_calcolare',stats:{}};
  const stats  = st.stats||{};
  const isCalc = st.stato==='calcolato';
  const punti  = z.lista_punti||[];
  const isOpen = activeZid===zid;
  const col    = z.color||'#4f46e5';
  const txt    = colorContrast(col);
  const isHidden = ZONE_HIDDEN.has(zid);

  // Stat bar (solo se calcolato)
  const statsBar = isCalc ? `
    <div class="zc-stats">
      <div class="stat-item"><div class="stat-val">${stats.km||0} km</div><div class="stat-lbl">Distanza</div></div>
      <div class="stat-item"><div class="stat-val">${fmtMin(stats.t_guida)}</div><div class="stat-lbl">Guida</div></div>
      <div class="stat-item"><div class="stat-val">${fmtMin(stats.t_tot)}</div><div class="stat-lbl">Totale</div></div>
    </div>` : '';

  // Modalita DIVIDI attiva su questo giro?
  const isDividiActive = dividiZid === zid;

  // Lista punti espansa
  const listaPunti = isOpen ? `
    <div class="zc-body open">
      ${isDividiActive ? `<div class="dividi-bar">&#9986; Seleziona fermate da spostare <b>${dividiSel.size}</b> sel.<button onclick="confermaDividi('${zid}')">Crea giro</button><button class="btn-annulla" onclick="annullaDividi()">Annulla</button></div>` : ''}
      ${punti.map((p,i)=>renderPuntoRow(p,i,zid,punti,isCalc,isSpec,isDividiActive)).join('')}
      ${!isSpec && !isLocked && !isDividiActive ? `
      <div class="zc-actions">
        <button class="btn-zona btn-dividi" onclick="avviaDividi('${zid}')">&#9986; Dividi</button>
        <button class="btn-zona btn-rinomina" onclick="apriModal('${zid}')">&#9998; Rinomina</button>
        ${isCalc?`<button class="btn-zona btn-ricalcola-giro" onclick="ricalcolaGiro('${zid}')">&#8635; Ricalcola</button>`:''}
      </div>` : ''}
    </div>` : '';;

  const nDDT = punti.reduce((a,p)=>{
    const cf=p.codici_ddt_frutta||[]; const cl=p.codici_ddt_latte||[];
    return a + cf.filter(c=>c&&c!=='p00000').length + cl.filter(c=>c&&c!=='p00000').length;
  }, 0);

  return `
  <div class="zone-card${isOpen?' active':''}" id="zcard-${zid}" data-zid="${zid}">
    <div class="zc-head" onclick="toggleCard('${zid}')">
      <div class="zc-pill" style="background:${col};color:${txt}">${punti.length}</div>
      <div class="zc-info">
        <div class="zc-name">
          ${z.nome_giro||zid}
          ${badgeStato(st.stato)}
        </div>
        <div class="zc-sub">${punti.length} fermate${nDDT?' &middot; '+nDDT+' DDT':''}${stats.fatturato&&stats.fatturato!=='GranChef'?' &middot; &euro;'+stats.fatturato:''}</div>
      </div>
      <button class="btn-eye${ZONE_HIDDEN.has(zid)?' hidden-zone':''}" title="${ZONE_HIDDEN.has(zid)?'Mostra':'Nascondi'} sulla mappa" onclick="event.stopPropagation();toggleHidden('${zid}')">&#128065;</button>
      ${!isLocked && !isSpec ? `<button class="btn-matita" title="Rinomina giro" onclick="event.stopPropagation();apriModal('${zid}')">&#9998;</button>` : ''}
    </div>
    ${statsBar}
    ${listaPunti}
  </div>`;
}

function renderPuntoRow(p,i,zid,punti,isCalc,isSpec,isDividiActive=false){
  const eta    = p.ora_arrivo ? `&#9201; ${p.ora_arrivo}` : '';
  // Fascia oraria di consegna (da BAT 1: orario_min / orario_max)
  const oMin   = p.orario_min || p.orario_min_frutta || p.orario_min_latte || '';
  const oMax   = p.orario_max || p.orario_max_frutta || p.orario_max_latte || '';
  const fascia = (oMin||oMax) ? `&#128344; ${oMin||'?'}&ndash;${oMax||'?'}` : '';
  const nota   = (p.note || '').trim();
  const isLate = p.ritardo ? 'border-color:#fca5a5;background:#fff1f2;' : '';
  const isSel  = isDividiActive && dividiSel.has(i);
  return `
  <div class="point-row${isSel?' dividi-sel':''}" style="${isLate}" id="pr-${zid}-${i}" ${isDividiActive?`onclick="toggleDividiSel(${i})"`:''}>
    <div class="pt-num" style="${p.ritardo?'background:#ef4444':isSel?'background:#3b82f6':''}">`+(isSel?'&#10003;':(i+1))+`</div>
    <div class="pt-info" onclick="${isDividiActive?'event.stopPropagation();toggleDividiSel('+i+')':'panToPoint('+(p.lat||0)+','+(p.lon||0)+')'}">
      <div class="pt-nome">${p.nome||'&mdash;'}</div>
      <div class="pt-addr">${(p.indirizzo||'').substring(0,45)}</div>
      ${fascia?`<div class="pt-eta" style="color:#0369a1;">${fascia}</div>`:''}
      ${eta?`<div class="pt-eta">${eta}</div>`:''}
      ${nota?`<div class="pt-addr" style="color:#92400e;font-style:italic;">&#128221; ${nota.substring(0,50)}</div>`:''}
    </div>
    ${!isSpec && !isLocked && !isDividiActive ? `
    <div class="pt-arrow-btns">
      <button class="pt-arrow" title="Su" onclick="muoviPunto('${zid}',`+i+`,-1)" ${i===0?'disabled':''}>&#9650;</button>
      <button class="pt-arrow" title="Giu" onclick="muoviPunto('${zid}',`+i+`,+1)" ${i===punti.length-1?'disabled':''}>&#9660;</button>
    </div>
    <button class="pt-arrow" title="Sposta in altro giro" style="margin-left:2px;width:24px;height:42px;" onclick="avviaSposta('${zid}',`+i+`)">&#8596;</button>
    ` : ''}
  </div>`;
}

function renderCardById(zid){
  const z = ZONE.find(x=>x.id_zona===zid);
  if(!z) return;
  const el = document.getElementById(`zcard-${zid}`);
  if(!el) return;
  el.outerHTML = renderCard(z);
}

// Rimuove automaticamente le zone rimaste senza fermate (anche al caricamento)
async function pulisciZoneVuote(silenzioso=false){
  const vuote = ZONE.filter(z => (z.lista_punti||[]).length === 0
    && z.id_zona !== 'DDT_DA_INSERIRE' && z.id_zona !== 'SENZA_ZONA');
  if(!vuote.length) return;
  vuote.forEach(z => {
    const idx = ZONE.indexOf(z);
    if(idx > -1) ZONE.splice(idx, 1);
    delete STATI[z.id_zona];
  });
  // Salva su disco: la zona vuota non riappare al prossimo riavvio
  await salvaTutto();
  if(!silenzioso){
    const nomi = vuote.map(z=>z.nome_giro||z.id_zona).join(', ');
    toast(`&#128465; Giro/i vuoti rimossi: ${nomi}`);
  }
  renderSidebar();
  if(gMap) renderMarkers();
}

function toggleCard(zid){
  activeZid = (activeZid===zid) ? null : zid;
  renderSidebar();
  if(activeZid){
    const z=ZONE.find(x=>x.id_zona===zid);
    if(z && z.lista_punti.length && z.lista_punti[0].lat)
      gMap.panTo({lat:z.lista_punti[0].lat, lng:z.lista_punti[0].lon});
  }
}

// ── Google Maps ───────────────────────────────────────────────────────────────
async function initMap(){
  const {Map} = await google.maps.importLibrary("maps");
  gMap = new Map(document.getElementById('map'),{
    center:{lat:45.5,lng:11.0}, zoom:8,
    mapId:"interactive_percorsi",
    mapTypeId:"hybrid",
    mapTypeControl:false, streetViewControl:false
  });
  // Chiudi InfoWindow cliccando su punto vuoto della mappa
  gMap.addListener('click', ()=>{ if(gInfoWindow){ gInfoWindow.close(); gInfoWindow=null; } });
}

function renderMarkers(){
  gMarkers.forEach(m=>{ if(m.map) m.map=null; });
  gMarkers=[];
  const bounds = new google.maps.LatLngBounds();
  let hasPoints=false;

  ZONE.forEach(z=>{
    const col = z.color||'#4f46e5';
    const zid = z.id_zona;
    if(ZONE_HIDDEN.has(zid)) return; // zona nascosta - salta
    (z.lista_punti||[]).forEach((p,i)=>{
      if(!p.lat||!p.lon) return;
      hasPoints=true;
      bounds.extend({lat:p.lat,lng:p.lon});
      const isGC = (p.tipologia_grado||'').toUpperCase().includes('GRAND') || (p.tipologia_grado||'').toUpperCase().includes('CHEF');

      // Wrapper: AdvancedMarkerElement ancora il bottom-center del content alla coordinata.
      // Il wrapper include il cerchio + il triangolino puntato sotto (solo per DNR).
      const el = document.createElement('div');
      el.style.cssText = 'display:flex;flex-direction:column;align-items:center;cursor:pointer;';

      const circle = document.createElement('div');
      // Il numero è SEMPRE visibile su tutti i marker per corrispondere alle card
      if(isGC){
        // GranChef: emoji + numero come etichetta sotto
        circle.style.cssText = `width:28px;height:28px;border-radius:50%;background:${col};border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;font-size:14px;transition:transform 0.15s;flex-shrink:0;`;
        circle.innerHTML = '&#x1F468;&#x200D;&#x1F373;';
        el.appendChild(circle);
        // Numero sotto l'emoji (piccola pill)
        const numBadge = document.createElement('div');
        numBadge.style.cssText = `background:${col};color:white;font-size:10px;font-weight:800;line-height:15px;padding:0 4px;border-radius:6px;margin-top:1px;border:1px solid white;`;
        numBadge.textContent = `${i+1}`;
        el.appendChild(numBadge);
      } else {
        // DNR: cerchio numerato + triangolino (goccia)
        circle.style.cssText = `width:28px;height:28px;border-radius:50%;background:${col};border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:800;transition:transform 0.15s;flex-shrink:0;`;
        circle.innerHTML = `${i+1}`;
        el.appendChild(circle);
        // Triangolino puntato giù — fa "toccare" la coordinata con la punta
        const tip = document.createElement('div');
        tip.style.cssText = `width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-top:7px solid ${col};margin-top:-1px;flex-shrink:0;`;
        el.appendChild(tip);
      }


      el.addEventListener('mouseenter', ()=>{ circle.style.transform='scale(1.15)'; });
      el.addEventListener('mouseleave', ()=>{ circle.style.transform='scale(1)'; });
      el.addEventListener('click', ()=>{
        toggleCard(zid);
        setTimeout(()=>panToPoint(p.lat,p.lon),200);
        mostraInfoMarker(p);
      });

      const {AdvancedMarkerElement} = google.maps.marker||{};
      if(AdvancedMarkerElement){
        const m = new AdvancedMarkerElement({position:{lat:p.lat,lng:p.lon},map:gMap,title:p.nome,content:el});
        gMarkers.push(m);
      }
    });
  });
  if(hasPoints) gMap.fitBounds(bounds,{padding:60});
}

// InfoWindow al click sul marker
function mostraInfoMarker(p){
  if(gInfoWindow){ gInfoWindow.close(); gInfoWindow=null; }
  const orario = (p.orario_min||p.ora_arrivo) ?
    `<div style="font-size:0.72rem;color:#4f46e5;font-weight:700;margin-bottom:4px;">&#9201; ${
      (p.orario_min&&p.orario_max) ? p.orario_min+' &ndash; '+p.orario_max :
      p.orario_min||p.ora_arrivo||''
    }</div>` : '';
  const nota = p.note||p.note_consegna||p.note_cliente||'';
  const noteHtml = nota ? `<div style="font-size:0.7rem;color:#92400e;background:#fef3c7;border-radius:5px;padding:4px 7px;margin-top:3px;">&#128221; ${nota}</div>` : '';
  gInfoWindow = new google.maps.InfoWindow({
    content: `<div style="font-family:'Inter',sans-serif;max-width:230px;padding:2px 4px;">`+
      `<div style="font-weight:800;font-size:0.88rem;color:#1e293b;margin-bottom:2px;">${p.nome||''}</div>`+
      `<div style="font-size:0.72rem;color:#64748b;margin-bottom:4px;">${p.indirizzo||p.via||''}</div>`+
      orario + noteHtml +
    `</div>`,
    position: {lat: p.lat, lng: p.lon},
    pixelOffset: new google.maps.Size(0,-32)
  });
  gInfoWindow.open(gMap);
}

function renderPolylines(){
  Object.keys(gPolylines).forEach(zid=>renderPolylinesZona(zid,STATI[zid]?.polylines||[],ZONE.find(x=>x.id_zona===zid)?.color||'#4f46e5'));
}

function renderPolylinesZona(zid, polylines, color){
  if(gPolylines[zid]){ gPolylines[zid].forEach(pl=>pl.setMap(null)); }
  gPolylines[zid]=[];
  if(!polylines||!polylines.length) return;
  if(ZONE_HIDDEN.has(zid)) return; // zona nascosta - non disegnare
  polylines.forEach(enc=>{
    if(!enc) return;
    const path = google.maps.geometry.encoding.decodePath(enc);
    const pl = new google.maps.Polyline({
      path, map:gMap,
      strokeColor: color,
      strokeOpacity:0.85, strokeWeight:4,
      geodesic:true
    });
    gPolylines[zid].push(pl);
  });
}

function panToPoint(lat,lng){
  if(!gMap||!lat||!lng) return;
  gMap.panTo({lat,lng});
  gMap.setZoom(Math.max(gMap.getZoom(),13));
}

// ── Lock / Unlock ─────────────────────────────────────────────────────────────
function toggleLock(){
  isLocked = !isLocked;
  const btn = document.getElementById('btn-lock');
  const btnSalva = document.getElementById('btn-salva');
  if(isLocked){
    btn.textContent = 'BLOCCATA 🔒';
    btn.className = 'btn-hdr btn-lock locked';
    btnSalva.style.display = 'none';
  } else {
    btn.textContent = 'SBLOCCATA 🔓';
    btn.className = 'btn-hdr btn-lock unlocked';
    btnSalva.style.display = 'flex';
  }
  renderSidebar();
  toast(isLocked ? '🔒 Mappa bloccata' : '🔓 Mappa sbloccata - ora puoi modificare');
}

// ── Visibilita zona sulla mappa ───────────────────────────────────────────────
function toggleHidden(zid){
  if(ZONE_HIDDEN.has(zid)) ZONE_HIDDEN.delete(zid);
  else ZONE_HIDDEN.add(zid);
  renderMarkers();
  renderPolylines();
  renderCardById(zid);
}

// ── DIVIDI giro ───────────────────────────────────────────────────────────────
function avviaDividi(zid){
  dividiZid = zid;
  dividiSel = new Set();
  if(activeZid !== zid) toggleCard(zid);
  else renderCardById(zid);
  toast('Seleziona le fermate da spostare nel nuovo giro, poi clicca Crea giro');
}

function toggleDividiSel(idx){
  if(dividiSel.has(idx)) dividiSel.delete(idx);
  else dividiSel.add(idx);
  renderCardById(dividiZid);
}

async function confermaDividi(zid){
  if(dividiSel.size === 0){ toast('Seleziona almeno una fermata'); return; }
  const z = ZONE.find(x=>x.id_zona===zid);
  if(!z){ annullaDividi(); return; }
  if(dividiSel.size >= z.lista_punti.length){ toast('Devi lasciare almeno una fermata nel giro originale'); return; }
  const r = await fetch('/api/dividi',{method:'POST',headers:{'Content-Type':'application/json'},
    body: JSON.stringify({id_zona: zid, indici: Array.from(dividiSel)})});
  const d = await r.json();
  if(!d.ok){ toast('❌ ' + (d.err||'Errore'), 4000); return; }
  ZONE = d.zone;
  STATI = {};
  ZONE.forEach(z=>{ STATI[z.id_zona]={stato:'da_calcolare',polylines:[],stats:{}}; });
  annullaDividi();
  renderSidebar();
  renderMarkers();
  aggiornaFase();
  toast('&#9986; Giro diviso: ' + d.nuovo_id + ' creato con ' + dividiSel.size + ' fermate');
}

function annullaDividi(){
  dividiZid = null;
  dividiSel = new Set();
  renderSidebar();
}

// ── Azioni principali ─────────────────────────────────────────────────────────
async function salvaTutto(){
  const r = await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ZONE)});
  const d = await r.json();
  toast(d.ok ? '💾 Salvato!' : '❌ Errore salvataggio: '+d.err);
}


async function calcolaTutto(){
  document.getElementById('btn-calcola').disabled=true;
  const r = await fetch('/api/calcola',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id_zone:[],usa_or_tools:true})});
  const d = await r.json();
  if(!d.ok){ toast('❌ Errore: '+d.err, 5000); document.getElementById('btn-calcola').disabled=false; return; }
  toast(`▶ Calcolo avviato per ${d.avviati.length} giri…`);
}

async function aggiornaModificati(){
  const modificati = Object.entries(STATI).filter(([,v])=>v.stato==='modificato').map(([k])=>k);
  if(!modificati.length){ toast('Nessun giro modificato.'); return; }
  // Per giri modificati manualmente: salta OR-Tools, ricalcola solo Directions
  const r = await fetch('/api/calcola',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id_zone:modificati,usa_or_tools:false})});
  const d = await r.json();
  toast(d.ok ? `🔄 Aggiornamento avviato (${modificati.length} giri)…` : '❌ Errore: '+d.err);
}

async function ricalcolaGiro(zid){
  const r = await fetch('/api/calcola',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id_zone:[zid],usa_or_tools:true})});
  const d = await r.json();
  toast(d.ok ? `▶ Ricalcolo ${zid} avviato…` : '❌ Errore: '+d.err);
}

async function generaFile(){
  // Sicurezza: verifica che tutti i giri siano calcolati
  const nonPronti = Object.entries(STATI).filter(([,v])=>v.stato!=='calcolato').map(([k])=>k);
  if(nonPronti.length > 0){
    toast(`⚠️ ${nonPronti.length} giri non ancora calcolati. Calcola tutto prima di generare.`, 5000);
    return;
  }
  // Prima salva lo stato corrente, poi genera gli HTML
  const rs = await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ZONE)});
  const ds = await rs.json();
  if(!ds.ok){ toast('❌ Errore salvataggio: '+ds.err, 5000); return; }
  toast('💾 Salvato. Generazione file in corso…', 8000);
  const r = await fetch('/api/genera',{method:'POST'});
  const d = await r.json();
  if(d.ok) toast(`✅ File generati! ${d.giri} giri → pronti per BAT 5`, 5000);
  else     toast('❌ Errore generazione: '+d.err, 5000);
}

// ── Riordino frecce ───────────────────────────────────────────────────────────
async function muoviPunto(zid, idx, dir){
  const z = ZONE.find(x=>x.id_zona===zid);
  if(!z) return;
  const arr = z.lista_punti;
  const newIdx = idx+dir;
  if(newIdx<0||newIdx>=arr.length) return;
  [arr[idx],arr[newIdx]] = [arr[newIdx],arr[idx]];
  // Marca giro come modificato
  if(STATI[zid]) STATI[zid].stato='modificato';
  renderCardById(zid);
  aggiornaFase();
  // Salva su disco
  await fetch('/api/riordina',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id_zona:zid, lista_punti:arr})});
}

// ── SPOSTA punto tra giri ─────────────────────────────────────────────────────
let _spostaPunto=null, _spostaFromZid=null, _spostaPIdx=null;

function avviaSposta(zid, idx){
  const z = ZONE.find(x=>x.id_zona===zid);
  if(!z) return;
  _spostaPunto   = z.lista_punti[idx];
  _spostaFromZid = zid;
  _spostaPIdx    = idx;
  document.getElementById('sposta-sub-txt').textContent = `"${_spostaPunto.nome}" → scegli destinazione:`;
  const chips = document.getElementById('sposta-chips');
  chips.innerHTML = ZONE.filter(x=>x.id_zona!==zid && x.id_zona!=='DDT_DA_INSERIRE').map(x=>`
    <div class="sposta-chip" style="border-color:${x.color}" onclick="eseguiSposta('${x.id_zona}')">
      <span style="color:${x.color}">●</span> ${x.nome_giro||x.id_zona}
    </div>`).join('');
  document.getElementById('sposta-overlay').classList.add('open');
}

async function eseguiSposta(toZid){
  chiudiSposta();
  const fromZ = ZONE.find(x=>x.id_zona===_spostaFromZid);
  const toZ   = ZONE.find(x=>x.id_zona===toZid);
  if(!fromZ||!toZ||!_spostaPunto) return;
  fromZ.lista_punti.splice(_spostaPIdx,1);
  toZ.lista_punti.push(_spostaPunto);
  // Marca entrambi i giri come modificati
  if(STATI[_spostaFromZid]) STATI[_spostaFromZid].stato='modificato';
  if(STATI[toZid])          STATI[toZid].stato='modificato';
  renderSidebar();
  renderMarkers();
  await pulisciZoneVuote();  // se la zona sorgente è rimasta vuota, la rimuove e salva
  aggiornaFase();
  await salvaTutto();         // salva comunque (aggiorna gli stati modificato)
  toast(`↔ Spostato: ${_spostaPunto.nome} → ${toZ.nome_giro}`);
}

function chiudiSposta(){ document.getElementById('sposta-overlay').classList.remove('open'); }

// ── MODAL RINOMINA ─────────────────────────────────────────────────────────────
function apriModal(zid){
  modalZid=zid;
  const z=ZONE.find(x=>x.id_zona===zid);
  const isGC = (zid||'').startsWith('GranChef');
  const nomi = isGC ? NOMI_GC : NOMI_DNR;
  document.getElementById('modal-title').textContent = isGC ? '🍽️ Rinomina giro GranChef' : '🚚 Rinomina giro';
  document.getElementById('modal-sub').textContent   = `ID zona: ${zid}`;
  const sel = document.getElementById('modal-select');
  sel.innerHTML = '<option value="">— Seleziona nome —</option>' + nomi.map(n=>`<option value="${n}"${z&&z.nome_giro===n?' selected':''}>${n}</option>`).join('');
  document.getElementById('modal-input').value = '';
  document.getElementById('modal-overlay').classList.add('open');
}

function onSelectChange(){
  const v=document.getElementById('modal-select').value;
  if(v) document.getElementById('modal-input').value='';
}

async function salvaRinomina(){
  const v = document.getElementById('modal-input').value.trim() || document.getElementById('modal-select').value;
  if(!v){ toast('Inserisci un nome.'); return; }
  const z=ZONE.find(x=>x.id_zona===modalZid);
  if(z) z.nome_giro=v;
  chiudiModal();
  renderCardById(modalZid);
  await salvaTutto();
  toast(`✏️ Rinominato: ${v}`);
}

function chiudiModal(){ document.getElementById('modal-overlay').classList.remove('open'); }
document.addEventListener('keydown', e=>{ if(e.key==='Escape'){ chiudiModal(); chiudiSposta(); }});

// ── Google Maps callback (chiamato quando le API sono pronte) ─────────────────
async function onGoogleMapsReady(){
  await init();
}
</script>
<script>
// ── PANNELLO FLOTTANTE ────────────────────────────────────────────────────────
let _sganciato = false;
let _dragOX=0, _dragOY=0;

function toggleSgancia(e){
  e && e.stopPropagation();
  const sb  = document.getElementById('sidebar');
  const btn = document.getElementById('btn-sgancia');
  if(!_sganciato){
    // Sgancia: diventa fixed nella posizione attuale
    const rect = sb.getBoundingClientRect();
    sb.style.left   = rect.left   + 'px';
    sb.style.top    = rect.top    + 'px';
    sb.style.width  = rect.width  + 'px';
    sb.style.height = rect.height + 'px';
    sb.classList.add('floating');
    document.body.style.overflow = 'visible';  // ← rimuove clipping del body
    btn.innerHTML = '&#8617;'; btn.title='Aggancia pannello'; btn.classList.add('active');
    _sganciato = true;
    if(gMap) setTimeout(()=>google.maps.event.trigger(gMap,'resize'),60);
  } else {
    // Aggancia: torna nel flusso normale con animazione
    sb.classList.add('snap-back');
    sb.classList.remove('floating');
    sb.style.left = sb.style.top = sb.style.width = sb.style.height = '';
    document.body.style.overflow = 'hidden';   // ← ripristina clipping
    btn.innerHTML = '&#10697;'; btn.title='Sgancia pannello'; btn.classList.remove('active');
    _sganciato = false;
    setTimeout(()=>sb.classList.remove('snap-back'), 380);
    if(gMap) setTimeout(()=>google.maps.event.trigger(gMap,'resize'),60);
  }
}

// Apri pannello su secondo schermo (popup window)
let _popupRef     = null;
let _popupChecker = null;

function apriPopup(e){
  e && e.stopPropagation();

  // Se popup già aperto → portalo in primo piano
  if(_popupRef && !_popupRef.closed){
    _popupRef.focus();
    return;
  }

  // Se il pannello era flottante, riaggancia prima
  if(_sganciato) toggleSgancia();

  const w = window.open(
    '/sidebar',
    'pannello_controllo',
    'width=460,height=920,toolbar=0,location=0,menubar=0,status=0,scrollbars=1,resizable=1'
  );
  if(!w){
    toast('\u26a0\ufe0f Popup bloccato \u2014 consenti i popup per localhost:5001 nelle impostazioni del browser');
    return;
  }
  _popupRef = w;

  // Chiudi popup quando la finestra principale viene chiusa
  window.addEventListener('beforeunload', function(){
    if(_popupRef && !_popupRef.closed) _popupRef.close();
  });

  // Nasconde sidebar nella finestra principale (mappa a tutto schermo)
  const sb = document.getElementById('sidebar');
  sb.style.display = 'none';
  document.getElementById('btn-popup').classList.add('active');
  if(gMap) setTimeout(()=>google.maps.event.trigger(gMap,'resize'), 80);

  // Polling ogni 500ms: rileva chiusura popup e ripristina sidebar
  _popupChecker = setInterval(()=>{
    if(_popupRef && _popupRef.closed){
      clearInterval(_popupChecker);
      _popupRef = null; _popupChecker = null;
      sb.style.display = '';
      document.getElementById('btn-popup').classList.remove('active');
      if(gMap) setTimeout(()=>google.maps.event.trigger(gMap,'resize'), 80);
    }
  }, 500);
}

// Drag: trascina il pannello tenendo premuto sull'header
(function initFloatDrag(){
  const hdr = document.getElementById('hdr');
  hdr.addEventListener('mousedown', function(e){
    if(!_sganciato) return;
    if(e.target.tagName==='BUTTON'||e.target.tagName==='INPUT'||e.target.tagName==='SELECT') return;
    const sb   = document.getElementById('sidebar');
    const rect = sb.getBoundingClientRect();
    _dragOX = e.clientX - rect.left;
    _dragOY = e.clientY - rect.top;
    hdr.classList.add('dragging');
    e.preventDefault();
    function onMove(ev){
      sb.style.left = (ev.clientX - _dragOX) + 'px';
      sb.style.top  = (ev.clientY - _dragOY) + 'px';
    }
    function onUp(){ hdr.classList.remove('dragging'); document.removeEventListener('mousemove',onMove); document.removeEventListener('mouseup',onUp); }
    document.addEventListener('mousemove',onMove);
    document.addEventListener('mouseup',onUp);
  });
})();
</script>
<script
  src="https://maps.googleapis.com/maps/api/js?key={{GOOGLE_MAPS_API_KEY}}&libraries=maps,marker,geometry&v=weekly&callback=onGoogleMapsReady"
  async defer>
</script>
</body>
</html>"""

# ── Main ──────────────────────────────────────────────────────────────────────
def _libera_porta():
    import subprocess
    try:
        r = subprocess.run(["netstat","-ano"], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if ":5001" in line and "LISTENING" in line:
                pid = line.split()[-1]
                subprocess.run(["taskkill","/F","/PID",pid], capture_output=True)
    except: pass

def main():
    args = sys.argv[1:]
    data_arg = next((a for a in args if not a.startswith("--")), "")
    if data_arg:
        target = CONSEGNE_DIR / f"CONSEGNE_{data_arg}"
        if not target.exists():
            print(f"Cartella non trovata: {target}"); return
    else:
        target = _get_latest_dir()
        if not target:
            print("Nessuna cartella CONSEGNE trovata."); return

    print(f"\n📁 Cartella: {target.name}")
    if not _carica_dati(target):
        print("❌ Errore: nessun dato trovato (punti_consegna_unificati.json o viaggi_giornalieri.json)."); return

    print(f"   Giri caricati: {len([z for z in ZONE_CACHE if z.get('id_zona') not in ('DDT_DA_INSERIRE',)])}")
    _libera_porta()
    print(f"\n🗺️  MAPPA INTERATTIVA PERCORSI: http://127.0.0.1:5001\n")
    threading.Thread(target=lambda: (time.sleep(1.4), webbrowser.open("http://127.0.0.1:5001")), daemon=True).start()
    app.run(port=5001, debug=False, threaded=True, use_reloader=False)

if __name__ == "__main__":
    main()

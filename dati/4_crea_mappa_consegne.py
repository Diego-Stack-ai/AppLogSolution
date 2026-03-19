#!/usr/bin/env python3
"""
Crea la mappa HTML dei punti di consegna dalla lista unificata (punti_consegna_unificati.json).
Usa coordinate M,N dalla mappatura; se mancano: geocodifica con C+D+indirizzo, poi solo indirizzo.

Regola: 1) coordinate M,N se presenti; 2) altrimenti geocode C+D+indirizzo; 3) altrimenti geocode indirizzo.

Genera anche file KML per Google My Maps (mymaps.google.com).

Uso: py crea_mappa_consegne.py <data> [--no-geocode]
     --no-geocode: non geocodificare i punti senza coordinate (solo M,N)
"""

import html as html_module
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
GEOCODE_CACHE = BASE_DIR / "geocode_cache.json"


def _val(x):
    if x is None:
        return ""
    s = str(x).strip()
    return "" if s.lower() == "nan" else s


def _escape_xml(s: str) -> str:
    if not s:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _salva_kml(punti: list[dict], path: Path, data: str):
    """Salva KML per import in Google My Maps (mymaps.google.com)."""
    ns = {"gx": "http://www.google.com/kml/ext/2.2", "kml": "http://www.opengis.net/kml/2.2"}
    root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    doc = ET.SubElement(root, "Document")
    ET.SubElement(doc, "name").text = f"Punti consegna {data}"
    for i, p in enumerate(punti, 1):
        pm = ET.SubElement(doc, "Placemark")
        nome = _val(p.get("nome")) or _val(p.get("indirizzo")) or f"Punto {i}"
        ET.SubElement(pm, "name").text = f"{i}. {nome[:80]}"
        desc_parts = [
            f"<b>{_escape_xml(nome)}</b>",
            f"Indirizzo: {_escape_xml(p.get('indirizzo', ''))}",
            f"Cod. Frutta: {_escape_xml(p.get('codice_frutta', ''))} | Latte: {_escape_xml(p.get('codice_latte', ''))}",
            f"Orario: {_escape_xml(p.get('orario_min', ''))}-{_escape_xml(p.get('orario_max', ''))}",
        ]
        tipo = "Frutta+Latte" if (p.get("codici_ddt_frutta") and p.get("codici_ddt_latte")) else ("Frutta" if p.get("codici_ddt_frutta") else "Latte")
        desc_parts.append(f"Tipo: {tipo}")
        ET.SubElement(pm, "description").text = "<br>".join(desc_parts)
        pt = ET.SubElement(pm, "Point")
        ET.SubElement(pt, "coordinates").text = f"{p['lon']},{p['lat']},0"
    tree = ET.ElementTree(root)
    if hasattr(ET, "indent"):
        ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True, method="xml")


def _salva_html_app(punti: list[dict], output_base: Path, data: str):
    """Genera HTML tipo app per telefono: lista destinazioni, 'Consegna completata', navigazione."""
    punti_js = json.dumps([
        {
            "i": i, "nome": _val(p.get("nome")) or _val(p.get("indirizzo")) or f"Punto {i}",
            "indirizzo": _val(p.get("indirizzo")),
            "lat": p["lat"], "lon": p["lon"],
            "orario": f"{_val(p.get('orario_min'))}-{_val(p.get('orario_max'))}",
            "cod_f": _val(p.get("codice_frutta")), "cod_l": _val(p.get("codice_latte")),
            "color": "#d32f2f" if any(a.get("status") == "red" for a in p.get("rientri_alert", [])) 
                     else ("#fbc02d" if p.get("rientri_alert") else "#2e7d32")
        }
        for i, p in enumerate(punti, 1)
    ], ensure_ascii=False)
    storage_key = f"consegne_{data.replace('-', '_')}"
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Consegne {data}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:system-ui,sans-serif;height:100vh;display:flex;flex-direction:column;background:#f5f5f5}}
#header{{background:#2e7d32;color:#fff;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}}
#header h1{{margin:0;font-size:1.1rem}} #progress{{font-size:0.9rem;opacity:.9}}
#tabs{{display:flex;background:#e0e0e0}} .tab{{flex:1;padding:12px;text-align:center;cursor:pointer;border:none;font-size:1rem}}
.tab.active{{background:#fff;font-weight:600}}
#map{{flex:1;min-height:200px}} #list{{flex:1;overflow-y:auto;padding:8px}}
.punto{{background:#fff;margin:6px 0;padding:12px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
.punto.fatto{{background:#e8f5e9;border-left:4px solid #2e7d32}}
.punto h3{{margin:0 0 6px;font-size:1rem}} .punto .ind{{font-size:0.85rem;color:#666;margin-bottom:8px}}
.punto .btns{{display:flex;gap:8px;flex-wrap:wrap}}
.btn{{padding:10px 16px;border:none;border-radius:6px;font-size:0.95rem;cursor:pointer;text-decoration:none;display:inline-block;text-align:center}}
.btn-nav{{background:#4285f4;color:#fff}} .btn-fatto{{background:#2e7d32;color:#fff}}
.btn-fatto:disabled{{background:#9e9e9e;cursor:default}}
</style>
</head>
<body>
<div id="header"><h1>Consegne {data}</h1><span id="progress">0 / {len(punti)}</span></div>
<div id="tabs"><button class="tab active" data-t="list">Lista</button><button class="tab" data-t="map">Mappa</button></div>
<div id="panels" style="flex:1;display:flex;flex-direction:column;min-height:0">
  <div id="list" style="display:block"><div id="lista"></div></div>
  <div id="map" style="display:none"></div>
</div>
<script>
const PUNTI = {punti_js};
const KEY = "{storage_key}";
let fatto = JSON.parse(localStorage.getItem(KEY) || "[]");
function save() {{ localStorage.setItem(KEY, JSON.stringify(fatto)); updateUI(); }}
function updateUI() {{
  document.getElementById("progress").textContent = fatto.length + " / " + PUNTI.length;
  const lista = document.getElementById("lista");
  lista.innerHTML = PUNTI.map(p => {{
    const ok = fatto.includes(p.i);
    return '<div class="punto' + (ok ? ' fatto' : '') + '" data-i="' + p.i + '" style="border-left:5px solid ' + p.color + '"><h3>' + p.i + '. ' + (p.nome||'').replace(/</g,'&lt;') + '</h3><div class="ind">' + (p.indirizzo||'').replace(/</g,'&lt;') + '</div><div class="btns"><a class="btn btn-nav" href="https://www.google.com/maps/dir/?api=1&destination=' + p.lat + ',' + p.lon + '" target="_blank">Naviga</a><button class="btn btn-fatto" ' + (ok ? 'disabled' : '') + ' onclick="toggle(' + p.i + ')">' + (ok ? 'Fatto' : 'Consegna completata') + '</button></div></div>';
  }}).join("");
}}
function toggle(i) {{ if (!fatto.includes(i)) {{ fatto.push(i); fatto.sort((a,b)=>a-b); save(); }} }}
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", function() {{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active")); this.classList.add("active");
  document.getElementById("list").style.display = this.dataset.t==="list" ? "block" : "none";
  document.getElementById("map").style.display = this.dataset.t==="map" ? "block" : "none";
  if (this.dataset.t==="map" && !window._mapInit) {{ setTimeout(initMap, 100); window._mapInit=true; }}
}}));
function initMap() {{
  const c = PUNTI[0]; const m = L.map("map").setView([c.lat,c.lon], 10);
  L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{attribution:"© OSM"}}).addTo(m);
  setTimeout(function() {{ m.invalidateSize(); }}, 200);
  PUNTI.forEach(p => {{
    const ok = fatto.includes(p.i);
    const bg = ok ? "#bdbdbd" : p.color;
    L.marker([p.lat,p.lon], {{icon: L.divIcon({{html:'<div style="background:' + bg + ';color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;border:1px solid #000">' + p.i + '</div>', iconSize:[28,28], iconAnchor:[14,14]}})}})
      .bindPopup('<b>' + (p.nome||'').replace(/</g,'&lt;') + '</b><br>' + (p.indirizzo||'').replace(/</g,'&lt;') + '<br><a href="https://www.google.com/maps/dir/?api=1&destination=' + p.lat + ',' + p.lon + '" target="_blank">Naviga</a> <button onclick="toggle(' + p.i + '); this.disabled=true; this.textContent=\\'Fatto\\'">Consegna completata</button>')
      .addTo(m);
  }});
}}
updateUI();
</script>
</body>
</html>"""
    app_path = output_base / f"consegne_app_{data.replace('-', '_')}.html"
    app_path.write_text(html, encoding="utf-8")
    return app_path


def _geocode(query: str, cache: dict, geo) -> tuple[float | None, float | None]:
    """Geocodifica con Nominatim. Ritorna (lat, lon) o (None, None)."""
    if not query or not str(query).strip():
        return (None, None)
    key = " ".join(str(query).lower().split())
    if key in cache:
        c = cache[key]
        lat, lon = c.get("lat"), c.get("lon")
        if lat is not None and lon is not None:
            return (float(lat), float(lon))
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
    """Fallback: Photon (Komoot) - spesso trova indirizzi italiani che Nominatim non trova."""
    if not query or not str(query).strip():
        return (None, None)
    q_clean = " ".join(str(query).split()) + " Italia"
    key = "photon:" + " ".join(q_clean.lower().split())
    if key in cache:
        c = cache[key]
        lat, lon = c.get("lat"), c.get("lon")
        if lat is not None and lon is not None:
            return (float(lat), float(lon))
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


def main():
    if len(sys.argv) < 2:
        print("Uso: py crea_mappa_consegne.py <data> [--no-geocode]")
        print("  Per i punti senza coordinate: usa C+D+indirizzo, poi solo indirizzo (default)")
        print("  --no-geocode: salta geocoding, solo punti con coordinate M,N")
        return 1

    if len(sys.argv) < 2:
        # Cerca l'ultima cartella creata
        folders = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
        if not folders:
            print("Uso: py 4_crea_mappa_consegne.py <data>")
            return 1
        folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        data = folders[0].name.split("_")[1]
        print(f"Nessuna data specificata. Uso l'ultima cartella trovata: {data}")
    else:
        data = sys.argv[1].strip()
    usa_geocode = "--no-geocode" not in [a.lower() for a in sys.argv[2:]]

    output_base = CONSEGNE_DIR / f"CONSEGNE_{data}"
    json_path = output_base / "punti_consegna_unificati.json"

    print("\n--- Mappa punti consegna ---\n")
    if not json_path.exists():
        print(f"Eseguire prima: py crea_lista_punti_unificata.py {data}")
        return 1

    with open(json_path, "r", encoding="utf-8") as f:
        dati = json.load(f)
    punti = dati.get("punti", [])

    punti_con_coord = []
    cache = {}
    geo = None
    if usa_geocode:
        try:
            cache = json.loads(GEOCODE_CACHE.read_text(encoding="utf-8")) if GEOCODE_CACHE.exists() else {}
        except Exception:
            pass
        from geopy.geocoders import Nominatim
        geo = Nominatim(user_agent="GestioneDDTViaggi/1.0")

    n_geocodificati = 0
    for p in punti:
        lat, lon = p.get("lat"), p.get("lon")
        if lat is not None and lon is not None:
            punti_con_coord.append(p)
        elif usa_geocode and geo:
            q1 = p.get("geo_query_nome_indirizzo", "")
            q2 = p.get("geo_query_indirizzo", "")
            lat, lon = _geocode(q1, cache, geo)
            if lat is None and q2 and q2 != q1:
                lat, lon = _geocode(q2, cache, geo)
            if lat is None and q2:
                lat, lon = _geocode_photon(q2, cache)
            if lat is not None and lon is not None:
                p["lat"], p["lon"] = lat, lon
                punti_con_coord.append(p)
                n_geocodificati += 1

    if usa_geocode and cache:
        GEOCODE_CACHE.parent.mkdir(parents=True, exist_ok=True)
        GEOCODE_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    if not punti_con_coord:
        print("Nessun punto con coordinate (né M,N né da geocoding C+D+indirizzo / indirizzo).")
        return 1

    try:
        import folium
    except ImportError:
        print("Per la mappa: pip install folium")
        return 1

    lat_med = sum(p["lat"] for p in punti_con_coord) / len(punti_con_coord)
    lon_med = sum(p["lon"] for p in punti_con_coord) / len(punti_con_coord)
    m = folium.Map(location=[lat_med, lon_med], zoom_start=9)

    for i, p in enumerate(punti_con_coord, 1):
        nome = _val(p.get("nome")) or _val(p.get("indirizzo")) or "-"
        ind = _val(p.get("indirizzo")) or "-"
        cod_f = _val(p.get("codice_frutta")) or ""
        cod_l = _val(p.get("codice_latte")) or ""
        if cod_f and cod_l and cod_l != "p00000":
            cod_ref = f"A: {html_module.escape(cod_f)} | B: {html_module.escape(cod_l)}"
        elif cod_f:
            cod_ref = f"A: {html_module.escape(cod_f)}"
        elif cod_l and cod_l != "p00000":
            cod_ref = f"B: {html_module.escape(cod_l)}"
        else:
            cod_ref = "-"
        om = _val(p.get("orario_min")) or "-"
        oM = _val(p.get("orario_max")) or "-"
        dest_url = f"https://www.google.com/maps/dir/?api=1&destination={p['lat']},{p['lon']}"
        tipo_label = ""
        if p.get("codici_ddt_frutta") and p.get("codici_ddt_latte"):
            tipo_label = " Frutta+Latte"
        elif p.get("codici_ddt_frutta"):
            tipo_label = " Frutta"
        elif p.get("codici_ddt_latte"):
            tipo_label = " Latte"
        popup_html = f"""<div style="font-family:sans-serif; min-width:220px;">
          <b>{i}. {html_module.escape(nome)}</b><small>{tipo_label}</small><br>
          {html_module.escape(ind)}<br>
          <small>{cod_ref}</small><br>
          <small>Orario: {om}-{oM}</small><br>
          <a href="{dest_url}" target="_blank" style="display:inline-block; margin-top:6px;
             padding:8px 14px; background:#4285f4; color:white; text-decoration:none;
             border-radius:4px; font-size:14px;">Apri navigazione</a></div>"""
        
        alerts = p.get("rientri_alert", [])
        f_color = "darkgreen"
        if alerts:
            f_color = "red" if any(a.get("status")=="red" for a in alerts) else "orange"
        
        folium.Marker(
            location=[p['lat'], p['lon']],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{i}. {nome[:40]} | {oM}",
            icon=folium.Icon(color=f_color, icon="info-sign")
        ).add_to(m)

    html_path = output_base / f"mappa_consegne_{data.replace('-', '_')}.html"
    kml_path = output_base / f"punti_consegna_{data.replace('-', '_')}.kml"
    m.save(str(html_path))
    content = html_path.read_text(encoding="utf-8")
    if "<head>" in content and "viewport" not in content.lower():
        content = content.replace(
            "<head>",
            "<head>\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">"
        )
        html_path.write_text(content, encoding="utf-8")

    _salva_kml(punti_con_coord, kml_path, data)

    # HTML "app" per telefono: lista + consegna completata + navigazione
    app_path = _salva_html_app(punti_con_coord, output_base, data)

    print(f"Punti in mappa: {len(punti_con_coord)} / {len(punti)}")
    print(f"Mappa HTML: {html_path.resolve()}")
    print(f"App telefono: {app_path.resolve()}")
    print(f"KML (Google My Maps): {kml_path.resolve()}")
    print("  Importa su mymaps.google.com: Crea nuova mappa > Importa > carica il file .kml")
    if n_geocodificati > 0:
        print(f"  (Geocodificati da C+D+indirizzo / indirizzo: {n_geocodificati})")
    print("\n--- Completato ---\n")
    return 0


if __name__ == "__main__":
    exit(main())

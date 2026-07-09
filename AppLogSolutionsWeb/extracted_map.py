def _genera_html_mappa(viaggio_id, punti, km, sec_guida, polylines, depot=None, distinta_url=None, ora_partenza_dep="07:00", actual_viaggio_id=None):
    """Genera HTML mappa mobile-first con polyline strade vere."""
    if depot is None:
        depot = _get_depot_for_points_cloud(punti)
    t_guida_min = sec_guida // 60
    t_sosta_min = len(punti) * TIME_PER_STOP_MIN
    t_tot_min   = t_guida_min + t_sosta_min

    def fmt_min(m):
        hh, mm = divmod(m, 60)
        return f"{hh}h {mm}m" if hh > 0 else f"{mm}m"

    depot_nome = depot.get("nome", "Deposito").title() if depot else "Deposito"
    
    fermate_html = ""
    
    # 1. Card di Partenza
    if distinta_url:
        fermate_html += f'''
            <div class="card" style="background:#f1f5f9; border-color:#94a3b8; grid-template-columns: 42px 1.4fr 1fr; padding: 10px; gap: 8px; align-items: stretch; cursor: default;">
                <div class="stop-num" style="background:#475569; align-self: center;"><span class="material-icons-round">home</span></div>
                <div class="stop-info" style="justify-content: center;">
                    <b class="name" style="font-size: 0.8rem;">PARTENZA</b>
                    <span class="addr" style="font-size: 0.7rem;">{depot_nome}</span>
                    <span class="orario-badge" style="background:#1e293b; color:white; margin-top:2px; font-size: 0.6rem;"><span class="material-icons-round" style="font-size: 10px !important;">schedule</span>Partenza: {ora_partenza_dep}</span>
                </div>
                <div style="border-left: 2px solid #bae6fd; background: #f0f9ff; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4px; border-radius: 8px; gap: 4px;">
                    <div style="font-size: 0.52rem; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: #0369a1;">📋 Distinta</div>
                    <a href="{distinta_url}" target="_blank" onclick="event.stopPropagation()" style="background: #0284c7; color: white; border: none; border-radius: 6px; padding: 5px 6px; font-size: 0.62rem; font-weight: 800; text-decoration: none; display: flex; align-items: center; gap: 3px; width: 100%; justify-content: center;">🔗 Apri PDF</a>
                </div>
            </div>'''
    else:
        fermate_html += f'''
            <div class="card" style="background:#f1f5f9; border-color:#94a3b8; grid-template-columns: 42px 1fr; cursor: default;">
                <div class="stop-num" style="background:#475569;"><span class="material-icons-round">home</span></div>
                <div class="stop-info">
                    <b class="name">PARTENZA</b>
                    <span class="addr">{depot_nome}</span>
                    <span class="orario-badge" style="background:#1e293b; color:white; margin-top:4px;"><span class="material-icons-round">schedule</span>Partenza: {ora_partenza_dep}</span>
                </div>
            </div>'''

    for idx, p in enumerate(punti):
        nome = p.get("nome", p.get("codice_cliente", f"Tappa {idx+1}"))
        rag_sociale = p.get("ragione_sociale", p.get("nome_cliente", ""))
        ind  = p.get("indirizzo", "")
        lat  = p.get("lat", "")
        lon  = p.get("lon", p.get("lng", ""))
        nav  = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving"
        
        is_parz = any(r.get("is_parziale") for r in p.get("rientri_alert", []) if isinstance(r, dict))
        warn_class = " warning" if is_parz else ""
        
        # Note
        note_txt = str(p.get("note", p.get("nota_integrativa", p.get("Note", ""))) or "").strip()
        note_html = ""
        if note_txt and note_txt.lower() != "nan":
            note_safe = note_txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            note_html = f'<div class="note-chip"><span class="material-icons-round">sticky_note_2</span>Note: {note_safe}</div>'
            
        # Orari
        om_val = str(p.get("orario_min") or p.get("orario_min_frutta", p.get("orario_min_latte", ""))).strip()
        oM_val = str(p.get("orario_max") or p.get("orario_max_frutta", p.get("orario_max_latte", ""))).strip()
        
        orario_html = ""
        if (om_val and om_val.lower() != "nan") or (oM_val and oM_val.lower() != "nan"):
            if om_val and oM_val:
                orario_txt = f"{om_val} - {oM_val}"
            elif om_val:
                orario_txt = f"Dalle {om_val}"
            else:
                orario_txt = f"Entro le {oM_val}"
            orario_html = f'<span class="orario-badge"><span class="material-icons-round">schedule</span>Fascia: {orario_txt}</span>'
            
        # Orario stimato arrivo / ripartenza
        ora_arr = str(p.get("ora_arrivo") or "").strip()
        ora_rip = str(p.get("ora_ripartenza") or "").strip()
        eta_html = ""
        if ora_arr and ora_rip:
            eta_html = f'<span class="eta-badge"><span class="material-icons-round">timer</span>Arrivo {ora_arr} &mdash; Ripart. {ora_rip}</span>'
        elif ora_arr:
            eta_html = f'<span class="eta-badge"><span class="material-icons-round">timer</span>Arrivo stimato {ora_arr}</span>'
            
        # Chiamata
        phone_num = _extract_phone(p)
        if phone_num:
            action_col = (
                f'<div class="nav-col">'
                f'<a href="{nav}" target="_blank" class="btn-nav" onclick="event.stopPropagation()"><span class="material-icons-round">navigation</span></a>'
                f'<a href="tel:{phone_num}" class="btn-call" onclick="event.stopPropagation()"><span class="material-icons-round">call</span></a>'
                f'<button class="btn-cam" onclick="openCamera(event, {idx})"><span class="material-icons-round">photo_camera</span></button>'
                f'</div>'
            )
            card_style = 'grid-template-columns: 42px 1fr auto;'
        else:
            action_col = (
                f'<div class="nav-col">'
                f'<a href="{nav}" target="_blank" class="btn-nav" onclick="event.stopPropagation()"><span class="material-icons-round">navigation</span></a>'
                f'<button class="btn-cam" onclick="openCamera(event, {idx})"><span class="material-icons-round">photo_camera</span></button>'
                f'</div>'
            )
            card_style = 'grid-template-columns: 42px 1fr auto;'
            
        fermate_html += (
            f'<div class="card" id="card-{idx}" onclick="selectCard({idx})" style="{card_style}">'
            f'<div class="stop-num{warn_class}">{idx+1}</div>'
            f'<div class="stop-info">'
            f'<span class="name">{nome}</span>'
            f'<span class="addr">{ind}</span>'
            f'{orario_html}'
            f'{eta_html}'
            f'{note_html}'
            f'</div>'
            f'{action_col}</div>'
        )

    # 3. Card di Arrivo
    ora_rientro_dep = ""
    try:
        part_m = re.match(r"(\d{2}):(\d{2})", str(ora_partenza_dep).strip())
        start_min = int(part_m.group(1)) * 60 + int(part_m.group(2)) if part_m else 420
        
        t_tot_min = (sec_guida // 60) + len(punti) * TIME_PER_STOP_MIN
        hh_ret, mm_ret = divmod(start_min + int(t_tot_min), 60)
        hh_ret = hh_ret % 24
        ora_rientro_dep = f"{hh_ret:02d}:{mm_ret:02d}"
    except Exception as e_time:
        print(f"[WARN] Impossibile calcolare ora rientro: {e_time}")

    rientro_badge = f'<span class="orario-badge" style="background:#1e293b; color:white; margin-top:4px;"><span class="material-icons-round">schedule</span>Rientro stimato: {ora_rientro_dep}</span>' if ora_rientro_dep else ''
    
    fermate_html += f'''
        <div class="card" style="background:#f1f5f9; border-color:#94a3b8; grid-template-columns: 42px 1fr; cursor: default;">
            <div class="stop-num" style="background:#475569;"><span class="material-icons-round">flag</span></div>
            <div class="stop-info">
                <b class="name">ARRIVO</b>
                <span class="addr">{depot_nome}</span>
                {rientro_badge}
            </div>
        </div>'''

    punti_js_list = []
    for p in punti:
        is_parz = any(r.get("is_parziale") for r in p.get("rientri_alert", []) if isinstance(r, dict))
        punti_js_list.append({
            "lat": float(p.get("lat", 0)),
            "lng": float(p.get("lon", p.get("lng", 0))),
            "nome": p.get("nome", ""),
            "codice_cliente": p.get("codice_cliente", ""),
            "ragione_sociale": p.get("ragione_sociale", p.get("nome_cliente", "")),
            "indirizzo": p.get("indirizzo", ""),
            "is_parziale": is_parz
        })
    punti_js     = json.dumps(punti_js_list)
    polylines_js = json.dumps(polylines)

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>Mappa {viaggio_id}</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
<script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&libraries=geometry&callback=initMap" async defer></script>
<style>
:root{{--p:#4f46e5;--accent:#10b981;--call:#16a34a}}
body,html{{margin:0;padding:0;height:100%;font-family:'Outfit',sans-serif;overflow:hidden}}
.main-container{{display:flex;flex-direction:column;height:100vh}}
#map{{height:42vh;width:100%;background:#dfe5eb}}
#sidebar{{flex:1;display:flex;flex-direction:column;background:white;border-top:2px solid #cbd5e1;overflow:hidden}}
.header{{padding:8px 12px;background:#1e293b;color:white;border-bottom:2px solid var(--accent)}}
.trip-title{{margin:0;font-size:.65rem;font-weight:800;text-transform:uppercase;color:var(--accent)}}
.stats-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}}
.stat-val{{font-size:.85rem;font-weight:800;color:white}}
.stat-lbl{{font-size:.52rem;color:#94a3b8;text-transform:uppercase}}
#delivery-list{{flex:1;overflow-y:auto;padding:8px;background:#f1f5f9;padding-bottom:60px}}
.card{{background:white;border-radius:12px;padding:10px;margin-bottom:8px;display:grid;gap:8px;align-items:center;border:1px solid #cbd5e1;cursor:pointer;transition:all .2s;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}}
.card.active{{border-color:var(--p);border-left:5px solid var(--p);background:#eef2ff}}
.stop-num{{width:32px;height:32px;background:var(--p);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;flex-shrink:0}}
.stop-num.warning {{
background: repeating-linear-gradient(45deg, #000, #000 4px, #f59e0b 4px, #f59e0b 8px) !important;
color: white !important;
text-shadow: 1px 1px 2px black, -1px -1px 2px black, 0px 0px 3px black;
border: 2px solid black;
}}
.stop-info{{display:flex;flex-direction:column;gap:3px;min-width:0}}
.name{{font-size:.85rem;font-weight:800;color:#1e293b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.addr{{font-size:.75rem;color:#64748b;font-weight:600;line-height:1.1}}
.orario-badge{{display:inline-flex;align-items:center;gap:3px;background:#eff6ff;color:#2563eb;font-size:0.65rem;font-weight:800;padding:2px 7px;border-radius:20px;border:1px solid #bfdbfe;margin-top:1px;width:fit-content}}
.orario-badge .material-icons-round{{font-size:12px !important}}
.eta-badge{{display:inline-flex;align-items:center;gap:3px;background:#e0f2fe;color:#0369a1;font-size:0.65rem;font-weight:800;padding:2px 7px;border-radius:20px;border:1px solid #bae6fd;margin-top:1px;width:fit-content}}
.eta-badge .material-icons-round{{font-size:12px !important}}
.note-chip{{display:flex;align-items:flex-start;gap:4px;background:#fffbeb;color:#92400e;font-size:0.65rem;font-weight:700;padding:4px 7px;border-radius:8px;border:1px solid #fde68a;margin-top:3px;line-height:1.3}}
.note-chip .material-icons-round{{font-size:12px !important;flex-shrink:0;margin-top:1px}}
.btn-nav{{background:var(--accent);color:white;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center;text-decoration:none}}
.btn-call{{background:var(--call);color:white;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center;text-decoration:none}}
.btn-cam{{background:#f59e0b;color:white;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center;border:none;cursor:pointer}}
.nav-col{{display:flex;flex-direction:column;gap:5px;align-items:center}}
.material-icons-round{{font-size:18px !important}}
.fab-save{{position:fixed;bottom:20px;right:20px;background:var(--accent);color:white;border:none;border-radius:30px;padding:12px 20px;font-weight:800;font-family:'Outfit',sans-serif;box-shadow:0 4px 12px rgba(16,185,129,0.4);display:none;align-items:center;gap:8px;cursor:pointer;z-index:1000;font-size:1rem;transition:transform 0.2s;}}
.fab-save:active{{transform:scale(0.95);}}

/* Stili Modale Riordino */
#reorder-modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#f8fafc;z-index:9999;flex-direction:column;}}
.rm-header{{padding:16px;background:#1e293b;color:white;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);}}
.rm-title{{margin:0;font-size:1.1rem;font-weight:800;display:flex;align-items:center;gap:8px;}}
.rm-body{{flex:1;overflow-y:auto;padding:12px;}}
.rm-footer{{padding:16px;background:white;border-top:1px solid #e2e8f0;display:flex;gap:12px;}}
.rm-btn-cancel{{flex:1;padding:14px;border:none;background:#f1f5f9;color:#475569;font-weight:700;border-radius:12px;cursor:pointer;}}
.rm-btn-save{{flex:2;padding:14px;border:none;background:var(--accent);color:white;font-weight:800;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 12px rgba(16,185,129,0.3);}}
.rm-item{{background:white;border:1px solid #cbd5e1;border-radius:12px;padding:12px;margin-bottom:8px;display:flex;align-items:center;gap:12px;}}
.rm-handle{{color:#94a3b8;cursor:grab;padding:4px;}}
.rm-num{{width:28px;height:28px;background:var(--p);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0;}}
.rm-info{{flex:1;min-width:0;display:flex;flex-direction:column;line-height:1.2;}}
.rm-name{{font-weight:800;color:#0f172a;font-size:0.9rem;}}
.rm-sub{{font-size:0.75rem;color:#64748b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.sortable-ghost{{opacity:0.4;}}
</style>
</head>
<body>
<div class="main-container">
<div id="map"></div>
<div id="sidebar">
<div class="header">
<p class="trip-title">&#x1F69B; {viaggio_id}</p>
<div class="stats-row">
<div><div class="stat-val">&#x23F0; {ora_partenza_dep}</div><div class="stat-lbl">Partenza</div></div>
<div><div class="stat-val">&#x1F6E3;&#xFE0F; {float(km or 0):.1f} km</div><div class="stat-lbl">Km Reali</div></div>
<div><div class="stat-val">&#x1F552; {fmt_min(t_guida_min)}</div><div class="stat-lbl">Guida</div></div>
<div><div class="stat-val">&#x23F1;&#xFE0F; {fmt_min(t_tot_min)}</div><div class="stat-lbl">Totale</div></div>
<div><div class="stat-val">&#x1F4E6; {len(punti)}</div><div class="stat-lbl">Tappe</div></div>
</div>
</div>
<div id="delivery-list">{fermate_html}</div>
</div>
<button id="fab-save" class="fab-save" onclick="saveSequence()"><span class="material-icons-round">save</span> Salva Sequenza</button>
<div id="cam-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; flex-direction:column; align-items:center; justify-content:center; padding:20px;">
    <div style="background:white; border-radius:12px; padding:20px; width:100%; max-width:400px; text-align:center; box-sizing:border-box;">
        <h3 style="margin-top:0; font-family:'Outfit',sans-serif;">Segnalazione</h3>
        <p id="cam-cliente-name" style="font-weight:bold; color:var(--p); margin-bottom:15px; font-family:'Outfit',sans-serif;"></p>
        <button onclick="selectCamType('merce_rotta')" style="width:100%; padding:15px; margin-bottom:10px; background:#ef4444; color:white; border:none; border-radius:8px; font-weight:bold; font-size:16px; font-family:'Outfit',sans-serif;">🔴 Merce Rifiutata / Rotta</button>
        <button onclick="selectCamType('reso_pregresso')" style="width:100%; padding:15px; margin-bottom:15px; background:#3b82f6; color:white; border:none; border-radius:8px; font-weight:bold; font-size:16px; font-family:'Outfit',sans-serif;">🔵 Reso / Ritiro</button>
        <button onclick="closeCamModal()" style="width:100%; padding:15px; background:#e2e8f0; color:#475569; border:none; border-radius:8px; font-weight:bold; font-size:16px; font-family:'Outfit',sans-serif;">Annulla</button>
    </div>
</div>
<input type="file" id="cameraInput" accept="image/*" capture="environment" style="display:none;" onchange="handleFile(event)">
</div>
<script>
const PUNTI={punti_js};
const POLYLINES={polylines_js};
const DEPOT={{lat:{depot["lat"]},lng:{depot["lon"]}}};
let map,markers=[];
function initMap(){{
map=new google.maps.Map(document.getElementById("map"),{{
center:PUNTI.length?{{lat:PUNTI[0].lat,lng:PUNTI[0].lng}}:DEPOT,
zoom:11,mapTypeId:"roadmap",disableDefaultUI:true,zoomControl:true}});
POLYLINES.forEach(enc=>{{
const path=google.maps.geometry.encoding.decodePath(enc);
new google.maps.Polyline({{path,geodesic:true,strokeColor:"#4f46e5",strokeOpacity:.85,strokeWeight:4,map}});
}});
new google.maps.Marker({{position:DEPOT,map,
icon:{{path:google.maps.SymbolPath.CIRCLE,scale:14,fillColor:"#1e293b",fillOpacity:1,strokeWeight:0}},
label:{{text:"D",color:"white",fontWeight:"bold"}}}});
PUNTI.forEach((p,i)=>{{
let fillColor = "#4f46e5";
let strokeColor = "white";
let strokeWeight = 2;
let labelColor = "white";
if (p.is_parziale) {{
fillColor = "#f59e0b";
strokeColor = "#000000";
strokeWeight = 3;
labelColor = "#000000";
}}
const m=new google.maps.Marker({{position:{{lat:p.lat,lng:p.lng}},map,
icon:{{path:google.maps.SymbolPath.CIRCLE,scale:13,fillColor:fillColor,fillOpacity:1,strokeWeight:strokeWeight,strokeColor:strokeColor}},
label:{{text:String(i+1),color:labelColor,fontWeight:"bold",fontSize:"12px"}}}});
m.addListener("click",()=>selectCard(i));
markers.push(m);
}});
}}
function selectCard(i){{
document.querySelectorAll(".card").forEach(c=>c.classList.remove("active"));
const card=document.getElementById("card-"+i);
if(card){{card.classList.add("active");card.scrollIntoView({{behavior:"smooth",block:"center"}});}}
if(markers[i]){{map.panTo(markers[i].getPosition());map.setZoom(16);}}
}}

let sequenceChanged = false;
document.addEventListener("DOMContentLoaded", () => {{
    const list = document.getElementById("delivery-list");
    if(list) {{
        new Sortable(list, {{
            handle: ".drag-handle",
            animation: 150,
            delay: 150,
            delayOnTouchOnly: true,
            fallbackTolerance: 3,
            onEnd: function(evt) {{
                if(evt.oldIndex !== evt.newIndex) {{
                    sequenceChanged = true;
                    document.getElementById("fab-save").style.display = "flex";
                }}
            }}
        }});
    }}
}});

async function saveSequence() {{
    if(!sequenceChanged) return;
    const btn = document.getElementById("fab-save");
    btn.innerHTML = '<span class="material-icons-round">autorenew</span> Salvataggio...';
    btn.style.pointerEvents = "none";
    
    const cards = document.querySelectorAll("#delivery-list .card");
    const sequenza = Array.from(cards)
        .filter(c => c.id.startsWith("card-"))
        .map(c => parseInt(c.id.replace("card-", "")));
        
    try {{
        let realViaggioId = "{actual_viaggio_id if actual_viaggio_id else viaggio_id}";
        if (realViaggioId.includes(" - ")) {{
            realViaggioId = realViaggioId.split(" - ")[1];
        }}
        
        const url = `https://europe-west1-{PROJECT_ID}.cloudfunctions.net/autista_aggiorna_sequenza`;
        const res = await fetch(url, {{
            method: "POST",
            headers: {{"Content-Type": "application/json"}},
            body: JSON.stringify({{ viaggio_id: realViaggioId, sequenza: sequenza }})
        }});
        if(res.ok) {{
            btn.innerHTML = '<span class="material-icons-round">check</span> Fatto!';
            setTimeout(() => window.location.reload(), 1000);
        }} else {{
            throw new Error("Errore salvataggio");
        }}
    }} catch(e) {{
        alert("Errore durante l'aggiornamento. Riprova.");
        btn.innerHTML = '<span class="material-icons-round">save</span> Salva Sequenza';
        btn.style.pointerEvents = "auto";
    }}
}}

let currentCamIdx = -1;
let currentCamType = "";
function openCamera(e, idx) {{
    e.stopPropagation();
    currentCamIdx = idx;
    document.getElementById("cam-cliente-name").innerText = PUNTI[idx].nome;
    document.getElementById("cam-modal").style.display = "flex";
}}
function closeCamModal() {{
    document.getElementById("cam-modal").style.display = "none";
}}
function selectCamType(type) {{
    currentCamType = type;
    closeCamModal();
    document.getElementById("cameraInput").click();
}}
function handleFile(e) {{
    const file = e.target.files[0];
    if(!file) return;
    
    const btn = document.getElementById("fab-save");
    const origHtml = btn.innerHTML;
    btn.innerHTML = '<span class="material-icons-round" style="animation: spin 1s linear infinite;">autorenew</span> Invio in corso...';
    btn.style.display = "flex";
    btn.style.pointerEvents = "none";
    
    const reader = new FileReader();
    reader.onload = function(event) {{
        const img = new Image();
        img.onload = async function() {{
            const canvas = document.createElement("canvas");
            let width = img.width;
            let height = img.height;
            const MAX_DIM = 1200;
            if (width > height) {{
                if (width > MAX_DIM) {{ height *= MAX_DIM / width; width = MAX_DIM; }}
            }} else {{
                if (height > MAX_DIM) {{ width *= MAX_DIM / height; height = MAX_DIM; }}
            }}
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);
            const base64 = canvas.toDataURL("image/jpeg", 0.7);
            
            try {{
                let realViaggioId = "{actual_viaggio_id if actual_viaggio_id else viaggio_id}";
                if (realViaggioId.includes(" - ")) realViaggioId = realViaggioId.split(" - ")[1];
                
                const url = `https://europe-west1-{PROJECT_ID}.cloudfunctions.net/autista_salva_reso`;
                const res = await fetch(url, {{
                    method: "POST",
                    headers: {{"Content-Type": "application/json"}},
                    body: JSON.stringify({{
                        viaggio_id: realViaggioId,
                        codice_cliente: PUNTI[currentCamIdx].codice_cliente || "UNK",
                        nome_cliente: PUNTI[currentCamIdx].nome,
                        tipo_segnalazione: currentCamType,
                        foto_base64: base64
                    }})
                }});
                if(res.ok) {{
                    alert("Foto inviata in ufficio con successo!");
                }} else {{
                    alert("Errore nell'invio della foto.");
                }}
            }} catch(err) {{
                alert("Errore di rete durante l'invio.");
            }} finally {{
                btn.innerHTML = origHtml;
                if(!sequenceChanged) btn.style.display = "none";
                btn.style.pointerEvents = "auto";
                document.getElementById("cameraInput").value = "";
            }}
        }}
        img.src = event.target.result;
    }}
    reader.readAsDataURL(file);
}}
</script>

<!-- Modal Riordino -->
<div id="reorder-modal">
    <div class="rm-header">
        <h2 class="rm-title"><span class="material-icons-round">low_priority</span> Riordina Tappe</h2>
    </div>
    <div class="rm-body" id="rm-list">
        <!-- populated by JS -->
    </div>
    <div class="rm-footer">
        <button class="rm-btn-cancel" onclick="chiudiModalRiordino()">Annulla</button>
        <button class="rm-btn-save" id="rm-btn-save" onclick="applicaESalvaRiordino()">
            <span class="material-icons-round">save</span> Salva Ordine
        </button>
    </div>
</div>

<script>
let modalSortable = null;
const puntiDati = {punti_js};

function apriModalRiordino() {{
    const list = document.getElementById("rm-list");
    list.innerHTML = "";
    puntiDati.forEach((p, idx) => {{
        const div = document.createElement("div");
        div.className = "rm-item";
        div.dataset.index = idx;
        const addressParts = (p.indirizzo || "").split(",");
        const city = addressParts.length > 1 ? addressParts[1].trim() : (p.indirizzo || "");
        div.innerHTML = `
            <div class="material-icons-round rm-handle">drag_indicator</div>
            <div class="rm-num">${{idx + 1}}</div>
            <div class="rm-info">
                <span class="rm-name">${{p.nome}}</span>
                <span class="rm-sub">${{p.ragione_sociale || ''}}</span>
            </div>
            <div class="rm-sub" style="flex-shrink:0; text-align:right;">${{city}}</div>
        `;
        list.appendChild(div);
    }});
    
    document.getElementById("reorder-modal").style.display = "flex";
    
    if (modalSortable) modalSortable.destroy();
    modalSortable = new Sortable(list, {{
        animation: 150,
        handle: ".rm-handle",
        ghostClass: "sortable-ghost"
    }});
}}

function chiudiModalRiordino() {{
    document.getElementById("reorder-modal").style.display = "none";
}}

async function applicaESalvaRiordino() {{
    const list = document.getElementById("rm-list");
    const items = list.querySelectorAll(".rm-item");
    const nuovaSequenza = Array.from(items).map(item => parseInt(item.dataset.index));
    
    const changed = nuovaSequenza.some((val, i) => val !== i);
    if (!changed) {{
        chiudiModalRiordino();
        return;
    }}
    
    const btn = document.getElementById("rm-btn-save");
    btn.innerHTML = '<span class="material-icons-round">autorenew</span> Salvataggio...';
    btn.style.pointerEvents = "none";
    
    try {{
        let realViaggioId = '{actual_viaggio_id if actual_viaggio_id else viaggio_id}';
        if (realViaggioId.includes(" - ")) {{
            realViaggioId = realViaggioId.split(" - ").pop();
        }}
        
        const resp = await fetch("https://europe-west1-log-solution-60007.cloudfunctions.net/autista_aggiorna_sequenza", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{
                viaggio_id: realViaggioId,
                sequenza: nuovaSequenza
            }})
        }});
        
        const res = await resp.json();
        if (res.status === "ok") {{
            alert("Sequenza aggiornata con successo! La pagina si ricaricherà.");
            window.location.reload();
        }} else {{
            alert("Errore nel salvataggio: " + res.message);
            btn.innerHTML = '<span class="material-icons-round">save</span> Salva Ordine';
            btn.style.pointerEvents = "auto";
        }}
    }} catch(err) {{
        alert("Errore di rete: " + err.message);
        btn.innerHTML = '<span class="material-icons-round">save</span> Salva Ordine';
        btn.style.pointerEvents = "auto";
    }}
}}
</script>
</body></html>"""



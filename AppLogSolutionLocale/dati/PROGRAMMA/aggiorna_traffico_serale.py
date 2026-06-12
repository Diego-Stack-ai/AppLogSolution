"""
AGGIORNA_TRAFFICO_SERALE.py
============================
Da lanciare a fine giornata (o la mattina successiva) DOPO che i giri sono stati completati.

Legge viaggi_giornalieri_OTTIMIZZATO.json, simula le ETA per trovare quali tratte
avvengono nella fascia 10:00-13:00, poi chiama la Matrix API con departure_time
per quelle coppie (solo quelle non ancora in cache) e salva i dati.

Costo: ~$0.30/giorno -> 0 con i $200 di credito gratuito Google.
"""
import json
import math
import requests
import datetime
import time
import sys
from pathlib import Path

PROG_DIR  = Path(__file__).resolve().parent
BASE_DIR  = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"

# Importa il modulo principale per riusare cache e costanti
sys.path.insert(0, str(PROG_DIR))
import importlib
gen_percorsi = importlib.import_module("6_genera_percorsi_veggiano")

GOOGLE_MAPS_API_KEY = gen_percorsi.GOOGLE_MAPS_API_KEY
dist_cache    = gen_percorsi.dist_cache
traffic_cache = gen_percorsi.traffic_cache
DEPOT         = gen_percorsi.DEPOT_VEGGIANO

AVG_SPEED_KMH = 45.0
SOSTA_DNR     = 8    # minuti
SOSTA_GC      = 12   # minuti
TRAFFIC_SLOTS_MIN = gen_percorsi.TRAFFIC_SLOTS_MIN  # [600,630,...,780]

# ── Helper ────────────────────────────────────────────────────────────────────

def fmt_time(minutes):
    minutes = int(minutes) % 1440
    return f"{minutes//60:02d}:{minutes%60:02d}"

def haversine(p1, p2):
    lat1, lon1 = float(p1.get('lat',0)), float(p1.get('lon',p1.get('lng',0)))
    lat2, lon2 = float(p2.get('lat',0)), float(p2.get('lon',p2.get('lng',0)))
    R = 6371
    dlat = math.radians(lat2-lat1); dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def nearest_slot(current_minutes):
    slots = TRAFFIC_SLOTS_MIN
    if current_minutes < slots[0]-15 or current_minutes > slots[-1]+15:
        return None
    nearest = min(slots, key=lambda s: abs(s-current_minutes))
    return f"{nearest//60:02d}{nearest%60:02d}"

def get_weekday_timestamp(hour, minute):
    """Timestamp del prossimo giorno feriale (Lun-Ven) a quell'orario."""
    now = datetime.datetime.now()
    days_ahead = 0
    while True:
        candidate = now + datetime.timedelta(days=days_ahead)
        if candidate.weekday() < 5:  # Mon-Fri
            ts = candidate.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if ts > now:
                return int(ts.timestamp())
        days_ahead += 1

def get_traffic_duration(p1, p2, slot_str):
    """Chiama Matrix API con departure_time per ottenere duration_in_traffic."""
    h = int(slot_str[:2])
    m = int(slot_str[2:])
    dep_ts = get_weekday_timestamp(h, m)
    orig  = f"{p1['lat']},{p1.get('lon',p1.get('lng',0))}"
    dest  = f"{p2['lat']},{p2.get('lon',p2.get('lng',0))}"
    url   = (f"https://maps.googleapis.com/maps/api/distancematrix/json"
             f"?origins={orig}&destinations={dest}"
             f"&departure_time={dep_ts}&traffic_model=best_guess"
             f"&key={GOOGLE_MAPS_API_KEY}")
    try:
        resp = requests.get(url, timeout=10).json()
        if resp.get('status') == 'OK':
            el = resp['rows'][0]['elements'][0]
            if el.get('status') == 'OK':
                # Preferisci duration_in_traffic se disponibile
                dur = el.get('duration_in_traffic', el.get('duration', {})).get('value')
                return dur
    except Exception as e:
        print(f"    Errore API: {e}")
    return None

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Trova la cartella CONSEGNE piu recente
    dirs = [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")]
    if not dirs:
        print("ERR Nessuna cartella CONSEGNE trovata.")
        return
    target_dir = max(dirs, key=lambda d: d.stat().st_mtime)
    print(f"Cartella: {target_dir.name}")

    json_path = target_dir / "viaggi_giornalieri_OTTIMIZZATO.json"
    if not json_path.exists():
        json_path = target_dir / "viaggi_giornalieri.json"
    if not json_path.exists():
        print("ERR Nessun file viaggi trovato.")
        return

    viaggi = json.loads(json_path.read_text(encoding="utf-8"))
    viaggi = [v for v in viaggi if v.get("id_zona","") != "DDT_DA_INSERIRE" and v.get("lista_punti")]

    print(f"Giri da analizzare: {len(viaggi)}")
    print(f"Fasce orarie: 10:00-13:00 ogni 30 min\n")

    coppie_da_aggiornare = []  # lista di (p_prec, p_dest, slot_str)
    totale_gia_in_cache  = 0

    for v in viaggi:
        punti  = v.get("lista_punti", [])
        depot  = gen_percorsi.get_depot_for_points(punti)
        is_gc  = any("GRAND" in str(p.get("tipologia_grado","")).upper() or
                     "CHEF"  in str(p.get("tipologia_grado","")).upper() for p in punti)
        sosta  = SOSTA_GC if is_gc else SOSTA_DNR
        nome   = v.get("nome_giro", v.get("id_zona","?"))

        # Simula ETA dall'inizio per trovare la tratta giusta
        current_time = 420  # 07:00
        punti_pieni  = [depot] + punti

        for idx in range(len(punti)):
            p_prec = punti_pieni[idx]
            p_dest = punti[idx]

            # Tempo di percorrenza dalla cache distanze
            cached = dist_cache.get(p_prec, p_dest)
            if cached:
                dur_min = cached['dur'] / 60.0 + 4  # + parking overhead
            else:
                d = haversine(p_prec, p_dest) * 1.3
                dur_min = (d / AVG_SPEED_KMH) * 60

            arr_time = current_time + dur_min  # orario di arrivo (minuti da mezzanotte)

            # La tratta viene percorsa tra current_time e arr_time
            # Il departure_time della tratta e' current_time (ora in cui si parte)
            slot = nearest_slot(current_time)
            if slot:
                if traffic_cache.has(p_prec, p_dest, slot):
                    totale_gia_in_cache += 1
                else:
                    coppie_da_aggiornare.append((p_prec, p_dest, slot, nome))

            current_time = arr_time + sosta  # ripartenza dopo la sosta

    print(f"Tratte gia in traffic_cache: {totale_gia_in_cache}")
    print(f"Tratte da aggiornare (nuove chiamate API): {len(coppie_da_aggiornare)}")
    if coppie_da_aggiornare:
        costo_stimato = len(coppie_da_aggiornare) * 0.01
        print(f"Costo stimato: ${costo_stimato:.2f}")
        print()

    if not coppie_da_aggiornare:
        print("Nessuna nuova chiamata necessaria - traffic_cache gia aggiornato!")
        return

    chiamate_ok  = 0
    chiamate_err = 0

    for i, (p1, p2, slot, nome_giro) in enumerate(coppie_da_aggiornare):
        h, m = int(slot[:2]), int(slot[2:])
        print(f"  [{i+1}/{len(coppie_da_aggiornare)}] {nome_giro}: "
              f"{p1.get('nome','DEPOSITO')[:20]} -> {p2.get('nome','?')[:20]} @ {h:02d}:{m:02d} ...", end=" ")

        dur = get_traffic_duration(p1, p2, slot)
        if dur:
            traffic_cache.set(p1, p2, slot, dur)
            chiamate_ok += 1
            print(f"OK ({dur//60}min)")
        else:
            chiamate_err += 1
            print("SKIP (errore API)")

        # Pausa per rispettare rate limit Google (10 req/sec)
        time.sleep(0.12)

    # Salva il cache aggiornato
    traffic_cache.save()

    print(f"\nAggiornamento completato!")
    print(f"  OK: {chiamate_ok} | Errori: {chiamate_err}")
    print(f"  Traffic cache totale: {len(traffic_cache.data)} coppie")
    print(f"  File: {gen_percorsi.TRAFFIC_CACHE_FILE}")

if __name__ == "__main__":
    main()

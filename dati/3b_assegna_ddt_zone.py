#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"

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
    json_2b = output_base / "2b_crea_zone_consegna.json"
    json_unificato = output_base / "punti_consegna_unificati.json"
    
    if not json_2b.exists() or not json_unificato.exists():
        print(f"File necessari non trovati in {output_base}")
        return 1

    print(f"\n--- Arricchimento ZONE per Mappa (3b) [{data}] ---")
    
    zone_raw = json.loads(json_2b.read_text(encoding="utf-8"))
    dati_unificati = json.loads(json_unificato.read_text(encoding="utf-8"))
    
    # Crea un dizionario veloce per cercare i dati dei punti p####
    punti_dettaglio = {}
    for p in dati_unificati.get("punti", []):
        cf = str(p.get("codice_frutta") or "").lower().strip()
        cl = str(p.get("codice_latte") or "").lower().strip()
        if cf: punti_dettaglio[cf] = p
        if cl: punti_dettaglio[cl] = p

    # Arricchimento
    for zona in zone_raw:
        lista_arricchita = []
        for cod in zona.get("codici_luogo", []):
            info = punti_dettaglio.get(cod)
            if info:
                # Evitiamo duplicati all'interno della stessa zona (un cliente potrebbe essere sia frutta che latte)
                if info not in lista_arricchita:
                    lista_arricchita.append(info)
        
        zona["lista_punti"] = lista_arricchita
        zona["numero_consegne"] = len(lista_arricchita)
        if "codici_luogo" in zona: del zona["codici_luogo"]

    out_file = output_base / "3b_assegna_ddt_zone.json"
    out_file.write_text(json.dumps(zone_raw, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"  Arricchite {len(zone_raw)} zone con i dettagli dei punti consegna.")
    print(f"  Salvato: {out_file.name}")
    return 0

if __name__ == "__main__":
    exit(main())

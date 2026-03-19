import json
from pathlib import Path

def analyze_suspect_points():
    p = Path("CONSEGNE/CONSEGNE_19-03-2026/punti_consegna_unificati.json")
    if not p.exists(): return
    
    data = json.loads(p.read_text(encoding="utf-8"))["punti"]
    print("--- PUNTI CON 3+ DDT O DOPPIONI STESSO TIPO (19-03) ---")
    found = 0
    for x in data:
        f = x.get("codici_ddt_frutta", [])
        l = x.get("codici_ddt_latte", [])
        # Caso 1: 3 o più DDT totali
        # Caso 2: Più di un DDT Frutta (o Latte) per lo stesso punto
        if (len(f) + len(l)) >= 3 or len(f) > 1 or len(l) > 1:
            found += 1
            print(f"\n- {x['nome']} ({x['indirizzo']})")
            print(f"  DDT Frutta ({len(f)}): {', '.join(f)}")
            print(f"  DDT Latte  ({len(l)}): {', '.join(l)}")
    
    print(f"\nTotale casi anomali trovati: {found}")

if __name__ == "__main__":
    analyze_suspect_points()

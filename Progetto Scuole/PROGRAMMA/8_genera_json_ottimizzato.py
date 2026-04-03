#!/usr/bin/env python3
"""
7_genera_json_ottimizzato.py
════════════════════════════
Legge i file HTML generati da 6_genera_percorsi_veggiano.py
nella cartella PERCORSI_VEGGIANO e ne estrae l'ordine ottimizzato
(calcolato da OR-Tools) per ogni viaggio.

Genera: CONSEGNE_{data}/viaggi_giornalieri_OTTIMIZZATO.json

Struttura output:
[
  {
    "nome_giro": "V01",
    "zone": ["3110", "4110"],
    "num_fermate": 24,
    "lista_punti": [   ← ordine ottimizzato OR-Tools
      { "nome": "...", "codice_frutta": "p2067", "codice_latte": "p00000", ... },
      ...
    ]
  },
  ...
]

Uso: py 7_genera_json_ottimizzato.py [data]
     es: py 7_genera_json_ottimizzato.py 26-03-2026
     Senza argomento usa l'ultima cartella CONSEGNE trovata.
"""

import json
import re
import sys
from pathlib import Path

# --- CONFIGURAZIONE ---
PROG_DIR   = Path(__file__).resolve().parent
BASE_DIR   = PROG_DIR.parent
CONSEGNE_DIR = BASE_DIR / "CONSEGNE"
DEPOT_NOME = "DEPOSITO VEGGIANO"

# Regex per estrarre il blocco "const data = [...]" dall'HTML
DATA_RE = re.compile(r'const\s+data\s*=\s*(\[.*?\]);\s*const\s+polys', re.DOTALL)
# Regex per estrarre nome e zone dal nomefile  (es. V01_Zone_3110_4110.html)
FILE_RE = re.compile(r'^(V\d+)_Zone_([\w_]+)\.html$', re.IGNORECASE)


def _trova_cartella(data_arg: str | None) -> Path:
    """Restituisce la cartella CONSEGNE_{data} corretta."""
    if data_arg:
        if re.match(r'^\d{2}-\d{2}$', data_arg):
            data_arg = f"{data_arg}-2026"
        p = CONSEGNE_DIR / f"CONSEGNE_{data_arg}"
        if not p.exists():
            raise FileNotFoundError(f"Cartella non trovata: {p}")
        return p
    # Ultima cartella disponibile
    folders = sorted(
        [d for d in CONSEGNE_DIR.iterdir() if d.is_dir() and d.name.startswith("CONSEGNE_")],
        key=lambda d: d.name
    )
    if not folders:
        raise FileNotFoundError("Nessuna cartella CONSEGNE_* trovata.")
    return folders[-1]


def _estrai_data_da_html(html_path: Path) -> list[dict]:
    """
    Estrae l'array 'data' dal file HTML e restituisce la lista
    dei punti di consegna nell'ordine ottimizzato (senza il deposito).
    """
    content = html_path.read_text(encoding="utf-8")
    m = DATA_RE.search(content)
    if not m:
        print(f"  ⚠️  Array 'data' non trovato in {html_path.name}")
        return []
    try:
        raw = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Errore parsing JSON in {html_path.name}: {e}")
        return []

    # Rimuove le entry del deposito (prima e ultima)
    punti = [p for p in raw if p.get("nome", "").upper() != DEPOT_NOME.upper()]
    return punti


def _parse_filename(filename: str) -> tuple[str, list[str]]:
    """
    Estrae nome giro e lista zone dal nome file.
    Es. 'V01_Zone_3110_4110.html' → ('V01', ['3110', '4110'])
    """
    m = FILE_RE.match(filename)
    if not m:
        return filename.replace(".html", ""), []
    nome_giro = m.group(1).upper()          # 'V01'
    zone_str  = m.group(2)                  # '3110_4110' o '0000_3111_4111'
    zone      = [z for z in zone_str.split("_") if z]
    return nome_giro, zone


def main():
    data_arg = sys.argv[1].strip() if len(sys.argv) > 1 else None

    try:
        cartella = _trova_cartella(data_arg)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Estrae la data dalla cartella (es. CONSEGNE_26-03-2026 → 26-03-2026)
    data_ddt = cartella.name.replace("CONSEGNE_", "")
    percorsi_dir = cartella / "PERCORSI_VEGGIANO"

    if not percorsi_dir.exists():
        print(f"❌ Cartella PERCORSI_VEGGIANO non trovata in: {cartella.name}")
        print("   Assicurati di aver eseguito prima lo script 6_genera_percorsi_veggiano.py")
        sys.exit(1)

    # Trova tutti gli HTML dei viaggi in ordine
    html_files = sorted(
        [f for f in percorsi_dir.glob("V*.html") if FILE_RE.match(f.name)]
    )

    if not html_files:
        print(f"❌ Nessun file V*.html trovato in {percorsi_dir}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  7_GENERA_JSON_OTTIMIZZATO — {data_ddt}")
    print(f"{'='*60}")
    print(f"  Trovati {len(html_files)} giri in PERCORSI_VEGGIANO\n")

    viaggi_ottimizzati = []

    for html_path in html_files:
        nome_giro, zone = _parse_filename(html_path.name)
        punti = _estrai_data_da_html(html_path)

        # Aggiunge data_ddt a ogni punto per la ricerca PDF
        for p in punti:
            # Se data_consegna è vuota → usa la data del DDT (non oggi!)
            if not p.get("data_consegna"):
                p["data_consegna"] = data_ddt

        viaggio = {
            "nome_giro": nome_giro,
            "file_sorgente": html_path.name,
            "zone": zone,
            "num_fermate": len(punti),
            "data_ddt": data_ddt,
            "lista_punti": punti
        }
        viaggi_ottimizzati.append(viaggio)

        # Riepilogo fermate per questo giro
        print(f"  ✅ {nome_giro} (zone: {', '.join(zone)}) → {len(punti)} fermate")
        for i, p in enumerate(punti, 1):
            cf = p.get("codice_frutta", "p00000")
            cl = p.get("codice_latte",  "p00000")
            nome = p.get("nome", "?")[:45]
            print(f"       {i:>2}. {nome:<45} F:{cf}  L:{cl}")

    # Salva il JSON ottimizzato
    out_path = cartella / "viaggi_giornalieri_OTTIMIZZATO.json"
    out_path.write_text(
        json.dumps(viaggi_ottimizzati, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Statistiche finali
    tot_fermate = sum(v["num_fermate"] for v in viaggi_ottimizzati)
    print(f"\n{'='*60}")
    print(f"  ✅ JSON Ottimizzato generato!")
    print(f"     File:      {out_path.name}")
    print(f"     Giri:      {len(viaggi_ottimizzati)}")
    print(f"     Fermate:   {tot_fermate} totali")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

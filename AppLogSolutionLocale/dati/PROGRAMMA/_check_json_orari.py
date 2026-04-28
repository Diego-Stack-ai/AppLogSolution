import json
from pathlib import Path

base = Path(r'g:\Il mio Drive\App\AppLogSolutionLocale\dati\CONSEGNE\CONSEGNE_28-04-2026')

for fname in ['viaggi_giornalieri.json', 'viaggi_giornalieri_OTTIMIZZATO.json']:
    json_path = base / fname
    if not json_path.exists():
        continue
    data = json.loads(json_path.read_text(encoding='utf-8'))
    # Struttura: data['viaggi'] oppure lista diretta
    viaggi = data.get('viaggi', []) if isinstance(data, dict) else data
    print(f"\n=== {fname} ===")
    for viaggio in viaggi:
        nome_v = viaggio.get('nome', viaggio.get('id', '?'))
        punti = viaggio.get('punti', [])
        h10 = [p for p in punti if '10:00' in str(p.get('orario_max', ''))]
        print(f"  Viaggio: {nome_v}  |  {len(punti)} fermate  |  H10={len(h10)}")
        for p in punti:
            om = p.get('orario_max', '')
            cf = p.get('codice_frutta', '')
            cl = p.get('codice_latte', '')
            nome = p.get('nome', '')[:40]
            print(f"    {nome:<40} cf={cf:<8} cl={cl:<8} orario_max={om}")

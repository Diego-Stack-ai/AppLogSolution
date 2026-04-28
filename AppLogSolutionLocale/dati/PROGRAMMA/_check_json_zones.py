import json
from pathlib import Path
p = Path(r'g:\Il mio Drive\App\AppLogSolutionLocale\dati\CONSEGNE\CONSEGNE_28-04-2026\viaggi_giornalieri.json')
data = json.loads(p.read_text(encoding='utf-8'))
viaggi = data.get('viaggi', data) if isinstance(data, dict) else data
for i, v in enumerate(viaggi):
    nome = v.get('nome_giro', v.get('nome', f'Viaggio {i}'))
    # ensure string for printing without unicode errors
    nome = str(nome).encode('ascii', 'ignore').decode('ascii')
    zone = v.get('zone', [])
    punti = v.get('lista_punti', [])
    print(f'Giro: {nome} - Zone: {zone} - Punti: {len(punti)}')

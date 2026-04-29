import json

f1 = 'G:/Il mio Drive/App/AppLogSolution/dati/CONSEGNE/CONSEGNE_20-04-2026/punti_consegna_unificati.json'
f2 = 'G:/Il mio Drive/App/AppLogSolution/dati/CONSEGNE/CONSEGNE_20-04-2026_copia/punti_consegna_unificati.json'

with open(f1, encoding='utf-8') as f: j1 = json.load(f)
with open(f2, encoding='utf-8') as f: j2 = json.load(f)

d1 = {p['nome']: p for p in j1.get('punti', [])}
d2 = {p['nome']: p for p in j2.get('punti', [])}

diff = 0
for n, p2 in d2.items():
    if n in d1:
        p1 = d1[n]
        if round(p1.get('lat', 0) or 0, 5) != round(p2.get('lat', 0) or 0, 5) or round(p1.get('lon', 0) or 0, 5) != round(p2.get('lon', 0) or 0, 5):
            print(n, '-> VERO(copia):', p2.get('lat'), p2.get('lon'), 'SBAGLIATO(nuovo):', p1.get('lat'), p1.get('lon'))
            diff += 1

print('Punti con differenze in unificati.json:', diff)

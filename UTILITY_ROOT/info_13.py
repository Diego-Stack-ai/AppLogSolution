import pandas as pd
df = pd.read_excel('G:/Il mio Drive/App/AppLogSolution/dati/PROGRAMMA/mappatura_destinazioni.xlsx', dtype=str)
pairs = [
    ('p2236', 'p00000'), ('p00000', 'p1711'), ('p2314', 'p1754'), 
    ('p2380', 'p1894'), ('p2316', 'p1752'), ('p2161', 'p00000'), 
    ('p2238', 'p1875'), ('p00000', 'p1749'), ('p2228', 'p2660'), 
    ('p2235', 'p00000'), ('p2227', 'p2659'), ('p2162', 'p00000'), 
    ('p2366', 'p00000')
]
for f, l in pairs:
    mask_f = df['Codice Frutta'].fillna('').str.lower().str.strip() == f
    mask_l = df['Codice Latte'].fillna('').str.lower().str.strip() == l
    row = df[mask_f & mask_l]
    if not row.empty:
        r = row.iloc[0]
        nome = r['A chi va consegnato']
        ind = r.get('Indirizzo', '')
        cit = r.get('Città', '') # could be 'Citt' depending on import
        print(f"- **{nome}**: {ind}, {cit} (Lat: {r['Latitudine']}, Lon: {r['Longitudine']})")

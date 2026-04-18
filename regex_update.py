import re

with open('G:/Il mio Drive/App/AppLogSolution/dati/PROGRAMMA/4_mappa_zone_google.py', 'r', encoding='utf-8') as f: content = f.read()

# Fix JS function call in renderMarkers
content = re.sub(r'_salvaSingolo\(p\.nome,\s*p\.indirizzo\s*\|\|\s*\'\',\s*p\.lat,\s*p\.lon\);', r"_salvaSingolo(p.codice_frutta || '', p.codice_latte || '', p.nome || '', p.lat, p.lon);", content)

# Fix JS _salvaSingolo definition
content = re.sub(r'function _salvaSingolo\(nome, indirizzo, lat, lon\) \{[\s\S]*?body:\s*JSON\.stringify\(\{nome,\s*indirizzo,\s*lat,\s*lon\}\)\s*\}\)', r"function _salvaSingolo(cod_f, cod_l, nome, lat, lon) {\n            fetch('/save_coord', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({cod_f, cod_l, nome, lat, lon}) })", content)

# Fix _aggiorna_entrambi_excel definition
old_agg = '''def _aggiorna_entrambi_excel(nome, lat, lon, indirizzo=None):
    """Sincronizzazione Atomica su Excel Master e Excel Giornaliero usando openpyxl per non rompere il file."""
    try:'''
new_agg = '''def _aggiorna_entrambi_excel(cod_f, cod_l, lat, lon, nome=None):
    """Sincronizzazione Atomica su Excel Master e Excel Giornaliero tramite Codice Frutta e Codice Latte."""
    try:'''
content = content.replace(old_agg, new_agg)

# Inside _aggiorna_entrambi_excel logic
content = re.sub(r'# Cerca colonna nome.*?(?=# Cerca o crea)', r'''col_f_idx = -1
                    col_l_idx = -1
                    for i, h in enumerate(headers):
                        if "frutta" in h or "cod. fr" in h: col_f_idx = i
                        elif "latte" in h or "cod. la" in h: col_l_idx = i
                    if col_f_idx == -1 and col_l_idx == -1:
                        col_f_idx, col_l_idx = 0, 1
                    
                    ''', content, flags=re.DOTALL)

content = re.sub(r'nome_target = str\(nome\)\.strip\(\)\.lower\(\).*?trovato = False', r'''c_f = str(cod_f).strip().lower() if cod_f and str(cod_f)!="p00000" else ""
                    c_l = str(cod_l).strip().lower() if cod_l and str(cod_l)!="p00000" else ""
                    if not c_f and not c_l: return True
                    trovato = False''', content, flags=re.DOTALL)

content = re.sub(r'for row_idx, row in enumerate\(ws\.iter_rows\(min_row=2\).*?trovato = True', r'''for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                        rf = str(row[col_f_idx].value or "").strip().lower() if col_f_idx>=0 else ""
                        rl = str(row[col_l_idx].value or "").strip().lower() if col_l_idx>=0 else ""
                        match_f = (c_f and rf == c_f)
                        match_l = (c_l and rl == c_l)
                        
                        if match_f or match_l:
                            ws.cell(row=row_idx, column=col_lat_idx+1, value=lat)
                            ws.cell(row=row_idx, column=col_lon_idx+1, value=lon)
                            trovato = True''', content, flags=re.DOTALL)

with open('G:/Il mio Drive/App/AppLogSolution/dati/PROGRAMMA/4_mappa_zone_google.py', 'w', encoding='utf-8') as f: f.write(content)
print("Regex replacements in python code done.")

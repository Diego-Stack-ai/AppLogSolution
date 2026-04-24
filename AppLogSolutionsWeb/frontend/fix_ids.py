import os
import re

files = [
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_articoli.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_nuovi_clienti.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_orari.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_rientri.html'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix the ID generation with spaces:
    # From: id="f_\" -> id="f_\"
    # From: document.getElementById('f_'+f).value -> document.getElementById('f_'+f.replace(/[^a-zA-Z0-9]/g, '_')).value
    
    content = content.replace('id="f_"', 'id="f_"')
    content = content.replace("document.getElementById('f_'+f).value", "document.getElementById('f_'+f.replace(/[^a-zA-Z0-9]/g, '_-')).value")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print("Fixed IDs in", f)

import os

files = [
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_articoli.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_nuovi_clienti.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_orari.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_rientri.html'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace("replace(/[^a-zA-Z0-9]/g, '_-')", "replace(/[^a-zA-Z0-9]/g, '_')")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

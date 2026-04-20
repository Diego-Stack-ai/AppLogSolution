import os

files = [
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_articoli.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_nuovi_clienti.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_orari.html',
    'G:/Il mio Drive/App/AppLogSolutions/frontend/gestione_rientri.html'
]

css_scrollbar = '''
        .list-container { 
            display: grid; gap: 16px; margin-top:20px; 
            max-height: 70vh; overflow-y: auto; padding-right: 12px;
        }
        .list-container::-webkit-scrollbar { width: 8px; }
        .list-container::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 8px; }
        .list-container::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 8px; }
        .list-container::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
'''

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace old .list-container with the new one
    content = content.replace('.list-container { display: grid; gap: 16px; margin-top:20px; }', css_scrollbar)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

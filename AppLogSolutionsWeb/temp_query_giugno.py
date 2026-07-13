import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

try:
    firebase_admin.initialize_app()
except ValueError:
    pass

db = firestore.client()

# Query presenze per giugno 2026
mese = "2026-06"
presenze_ref = db.collection('presenze')
query = presenze_ref.where('mese', '==', mese).stream()

risultati = []
for doc in query:
    data = doc.to_dict()
    data['id'] = doc.id
    risultati.append(data)

# Print a summary
print(f"Trovati {len(risultati)} documenti per {mese}")

if len(risultati) > 0:
    print("Campi tipici di un documento:")
    print(json.dumps(risultati[0], indent=2))
    
    # Analyze navette/viaggi/TVT
    with_tvt = 0
    with_navetta = 0
    with_viaggio = 0
    with_attivita = 0
    
    for r in risultati:
        if 'tvt' in r and r['tvt']:
            with_tvt += 1
        if 'navetta' in r and r['navetta']:
            with_navetta += 1
        if 'viaggio' in r and r['viaggio']:
            with_viaggio += 1
        if 'attivitaAggiuntive' in r and len(r['attivitaAggiuntive']) > 0:
            with_attivita += 1
            
    print(f"\nDocumenti con TVT: {with_tvt}")
    print(f"Documenti con Navetta: {with_navetta}")
    print(f"Documenti con Viaggio/Zona: {with_viaggio}")
    print(f"Documenti con Attività Aggiuntive: {with_attivita}")
    
    # Print distinct values for "viaggio" or "navetta" if we want to see them
    navette_viste = set()
    for r in risultati:
        if 'navetta' in r and r['navetta']:
            navette_viste.add(r['navetta'])
            
    if navette_viste:
        print(f"Navette trovate: {navette_viste}")

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase (assuming default credentials or we can use the local ones)
try:
    firebase_admin.initialize_app()
except ValueError:
    pass

db = firestore.client()

docs = db.collection('dipendenti').stream()

print("Analisi dipendenti licenziati/inattivi:")
print("-" * 50)
for doc in docs:
    data = doc.to_dict()
    nome = data.get('nome', data.get('Nome', 'Sconosciuto'))
    attivo = data.get('attivo')
    stato = data.get('stato', data.get('Stato', ''))
    ruolo = data.get('ruolo', data.get('Ruolo', ''))
    
    # Se ha a che fare con Flori o licenziati
    is_flori = 'flori' in nome.lower()
    is_licenziato = 'licenziat' in stato.lower()
    is_inattivo = 'inattiv' in stato.lower() or attivo is False
    
    if is_flori or is_licenziato or is_inattivo:
        print(f"Nome: {nome}")
        print(f"  - Attivo (booleano): {attivo}")
        print(f"  - Stato (testo): '{stato}'")
        print(f"  - Ruolo: '{ruolo}'")
        print("-" * 50)

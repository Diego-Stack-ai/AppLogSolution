import firebase_admin
from firebase_admin import credentials, firestore

try:
    firebase_admin.initialize_app()
except ValueError:
    pass

db = firestore.client()

print("Checking CATTEL clients in Firestore...")
clienti_ref = db.collection('clienti').document('CATTEL').collection('raccolta clienti')
docs = list(clienti_ref.stream())

for doc in docs[:10]:
    d = doc.to_dict()
    print(f"ID: {doc.id}, codice_frutta: '{d.get('codice_frutta')}', codice_latte: '{d.get('codice_latte')}', nome: '{d.get('cliente') or d.get('nome_consegna')}'")
    
print(f"Total CATTEL clients: {len(docs)}")

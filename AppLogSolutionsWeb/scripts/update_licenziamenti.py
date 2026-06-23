import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
autisti_ref = db.collection("dipendenti").stream()

batch = db.batch()
count = 0

for doc in autisti_ref:
    data = doc.to_dict()
    nome = data.get("nome", "").lower()
    
    # Check for Sirbu Catalin and Bundo Gerty
    if "sirbu catalin" in nome or "bundo gerti" in nome:
        batch.update(doc.reference, {"data_licenziamento": "2026-05-31"})
        print(f"Aggiornato licenziamento per: {data.get('nome')}")
    else:
        # For all others, set empty if not exists
        if "data_licenziamento" not in data:
            batch.update(doc.reference, {"data_licenziamento": ""})
    count += 1

batch.commit()
print(f"Licenziamenti aggiornati con successo per {count} dipendenti!")


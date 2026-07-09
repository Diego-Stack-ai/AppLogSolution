import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

data_cercata = "08-07-2026"
print(f"Ricerca viaggi ddt DNR per {data_cercata} in PROD...")
viaggi_ref = db.collection('clienti').document('DNR').collection('viaggi ddt')
query = viaggi_ref.where("data_lavoro", "==", data_cercata).stream()
viaggi = list(query)
if len(viaggi) == 0:
    print(f"Nessun viaggio trovato per {data_cercata}")
else:
    print(f"Trovati {len(viaggi)} viaggi:")
    for v in viaggi:
        print(f"- {v.id}: {v.to_dict().get('status')} | Autista: {v.to_dict().get('autista', 'Non assegnato')} | {v.to_dict().get('nome_giro')}")

data_cercata = "06-07-2026"
print(f"\nRicerca viaggi ddt DNR per {data_cercata} in PROD...")
query2 = viaggi_ref.where("data_lavoro", "==", data_cercata).stream()
viaggi2 = list(query2)
if len(viaggi2) == 0:
    print(f"Nessun viaggio trovato per {data_cercata}")
else:
    print(f"Trovati {len(viaggi2)} viaggi:")
    for v in viaggi2:
        print(f"- {v.id}: {v.to_dict().get('status')} | Autista: {v.to_dict().get('autista', 'Non assegnato')} | {v.to_dict().get('nome_giro')}")

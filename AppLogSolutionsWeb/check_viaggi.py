import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

data_cercata = "07-07-2026"
print(f"Ricerca viaggi ddt CATTEL per {data_cercata} in PROD...")

viaggi_ref = db.collection('clienti').document('CATTEL').collection('viaggi ddt')
query = viaggi_ref.where("data_lavoro", "==", data_cercata).stream()

viaggi = list(query)
if len(viaggi) == 0:
    print(f"Nessun viaggio trovato per la data {data_cercata}")
else:
    print(f"Trovati {len(viaggi)} viaggi:")
    for v in viaggi:
        print(f"- {v.id}: {v.to_dict().get('status')} | Autista: {v.to_dict().get('autista', 'Non assegnato')} | {v.to_dict().get('nome_giro')}")

print("\nCerco gli ultimi viaggi in PROD per CATTEL...")
query_recent = viaggi_ref.order_by("data_lavoro", direction=firestore.Query.DESCENDING).limit(10).stream()

for v in query_recent:
    d = v.to_dict()
    print(f"- {v.id}: {d.get('data_lavoro')} | Autista: {d.get('autista', 'N/A')} | status: {d.get('status')}")


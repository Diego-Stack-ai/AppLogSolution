import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

print("Cerco gli ultimi viaggi in PROD per GRAN CHEF...")
viaggi_ref = db.collection('clienti').document('GRAN CHEF').collection('viaggi ddt')
query_recent = viaggi_ref.order_by("data_lavoro", direction=firestore.Query.DESCENDING).limit(10).stream()

for v in query_recent:
    d = v.to_dict()
    print(f"- {v.id}: {d.get('data_lavoro')} | Autista: {d.get('autista', 'N/A')} | status: {d.get('status')}")

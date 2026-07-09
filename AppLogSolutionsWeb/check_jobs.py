import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

print("Cerco gli ultimi 10 Job in PROD (DNR)...")
jobs_ref = db.collection('clienti').document('DNR').collection('processing_jobs')
query_jobs = jobs_ref.order_by("createdAt", direction=firestore.Query.DESCENDING).limit(10).stream()

for j in query_jobs:
    d = j.to_dict()
    print(f"- Job {j.id}: data_lavoro={d.get('data_lavoro')} | data_ddt={d.get('data_ddt')} | status={d.get('status')} | createdAt={d.get('createdAt')}")

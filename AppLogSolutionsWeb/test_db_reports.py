import firebase_admin
from firebase_admin import credentials, firestore
import json

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo")

db = firestore.client(app=app)
reports = db.collection('clienti').document('DNR').collection('reports_logistici').order_by('data_consegna', direction=firestore.Query.DESCENDING).limit(5).stream()

print("ULTIMI 5 REPORTS:")
for r in reports:
    print(r.id, r.to_dict().get("status", "no status"))

jobs = db.collection('clienti').document('DNR').collection('processing_jobs').order_by('created_at', direction=firestore.Query.DESCENDING).limit(5).stream()

print("\nULTIMI 5 JOBS DI ELABORAZIONE:")
for j in jobs:
    data = j.to_dict()
    print(j.id, data.get("status", "NO STATUS"), data.get("error", ""))
    

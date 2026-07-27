import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dev_key.json'
import firebase_admin
from firebase_admin import firestore

app = firebase_admin.initialize_app()
db = firestore.client(app=app)

print("--- INVENTARIO CATTEL DEV (25-07-2026) ---")

# 1. Processing Jobs
print("\n[Jobs]")
jobs = db.collection('processing_jobs').where('tenant', '==', 'CATTEL').where('dataViaggi', '==', '25-07-2026').stream()
for j in jobs:
    d = j.to_dict()
    print(f"- Job ID: {j.id} | Status: {d.get('status')} | Error: {d.get('errorMessage')}")

# 2. Viaggi
print("\n[Viaggi]")
viaggi = db.collection('viaggi_camion').where('tenant', '==', 'CATTEL').where('data', '==', '25-07-2026').stream()
for v in viaggi:
    d = v.to_dict()
    print(f"- Viaggio ID: {v.id} | Targa: {d.get('targa')} | Zone: {d.get('id_zona')}")

# 3. Title Locks
print("\n[Title Locks]")
locks = db.collection('title_locks').where('tenant', '==', 'CATTEL').where('data', '==', '25-07-2026').stream()
for l in locks:
    d = l.to_dict()
    print(f"- Lock ID: {l.id} | Targa: {d.get('targa')} | LockedAt: {d.get('lockedAt')}")

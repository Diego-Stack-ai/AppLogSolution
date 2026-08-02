import sys
import json
sys.path.insert(0, 'functions')
from firebase_admin import credentials, firestore, initialize_app

initialize_app(credentials.Certificate('cantiere_key.json'))
db = firestore.client()
docs = db.collection('clienti').document('DNR').collection('processing_jobs').order_by('created_at', direction=firestore.Query.DESCENDING).limit(5).stream()

print('=== ULTIMI 5 JOB ===')
for d in docs:
    status = d.get('status')
    tipo = d.get('type')
    created = d.get('created_at')
    started = d.get('started_at')
    completed = d.get('completed_at')
    fname = d.get('fileName')
    storage_path = d.get('storage_path')
    print(f'Job {d.id} | Stato: {status} | Tipo: {tipo} | Creato: {created} | Started: {started} | Completed: {completed} | File: {fname} | StoragePath: {storage_path}')

import firebase_admin
from firebase_admin import credentials, firestore
import json

try:
    cred = credentials.Certificate("h:/Il mio Drive/App/AppLogSolutionsWeb/functions/log-solution-60007-firebase-adminsdk-h4a0x-97fb376483.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    clienti_ref = db.collection('clienti_fatturazione')
    docs = clienti_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        print(f"CLIENTE: {data.get('nome')}")
        print(f"MAGAZZINI: {json.dumps(data.get('magazzini', []), indent=2)}")
        print("---")
except Exception as e:
    print(f"Error: {e}")

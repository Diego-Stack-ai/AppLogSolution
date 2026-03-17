import firebase_admin
from firebase_admin import credentials, firestore
import json

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Cerchiamo sia l'UID che lo slug
ids_to_check = ['xyOAp8p9v9UAJuHOaTJcpyhOAf63', 'catalin_sirbu']

for doc_id in ids_to_check:
    doc = db.collection('users').document(doc_id).get()
    if doc.exists:
        print(f"--- Document: {doc_id} ---")
        print(json.dumps(doc.to_dict(), indent=2))
    else:
        print(f"--- Document: {doc_id} NOT FOUND ---")

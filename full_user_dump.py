import firebase_admin
from firebase_admin import credentials, firestore
import json

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')
docs = users_ref.stream()

print("--- Dump Completo Utenti ---")
for doc in docs:
    print(f"ID: {doc.id}")
    print(json.dumps(doc.to_dict(), indent=2))
    print("-" * 20)

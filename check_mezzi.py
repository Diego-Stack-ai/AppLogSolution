import firebase_admin
from firebase_admin import credentials, firestore
import json

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def check_mezzi():
    print("Elenco Mezzi in Firestore:")
    mezzi_ref = db.collection('mezzi')
    docs = list(mezzi_ref.stream())
    
    results = []
    for doc in docs:
        d = doc.to_dict()
        results.append({
            "doc_id": doc.id,
            "data": d
        })
        print(f"ID: {doc.id} | Dati: {d}")
        
    with open('mezzi_analysis.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    check_mezzi()

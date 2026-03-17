import firebase_admin
from firebase_admin import credentials, firestore

# Configurazione
key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fix_missing():
    users_ref = db.collection('users')
    docs = list(users_ref.stream())
    for doc in docs:
        d = doc.to_dict()
        if 'uid' not in d or not d['uid']:
            print(f"Aggiorno {doc.id} per aggiungere il campo uid")
            users_ref.document(doc.id).update({'uid': doc.id})

if __name__ == "__main__":
    fix_missing()

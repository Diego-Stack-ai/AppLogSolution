import firebase_admin
from firebase_admin import credentials, firestore

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def list_users_details():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    print("--- Dettagli Utenti Firestore ---")
    for doc in docs:
        d = doc.to_dict()
        print(f"ID: {doc.id} | Nome: {d.get('nome')} | Username: {d.get('username')} | Password: {d.get('password')} | Ruolo: {d.get('ruolo')} | Email: {d.get('email')}")

if __name__ == "__main__":
    list_users_details()

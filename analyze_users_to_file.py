import firebase_admin
from firebase_admin import credentials, firestore
import json

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def analyze_users():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    
    report = []
    for doc in docs:
        d = doc.to_dict()
        user_info = {
            "id": doc.id,
            "nome": d.get("nome", "N.D."),
            "email": d.get("email", "N.D."),
            "ruolo": d.get("ruolo", "N.D."),
            "tipoTurno": d.get("tipoTurno", "N.D."),
            "canElevate": d.get("canElevate", "N.D."),
            "has_password_field": "password" in d,
            "extra_fields": [k for k in d.keys() if k not in ["nome", "email", "ruolo", "tipoTurno", "canElevate", "password"]]
        }
        report.append(user_info)
    
    with open("g:\\Il mio Drive\\AppLogSolution\\users_analysis.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    analyze_users()
    print("Analisi salvata in users_analysis.json")

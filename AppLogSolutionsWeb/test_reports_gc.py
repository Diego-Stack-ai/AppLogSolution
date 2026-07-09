import firebase_admin
from firebase_admin import credentials, firestore

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo_db2")

db = firestore.client(app=app)
reports_gc = db.collection('clienti').document('GRAN CHEF').collection('reports_logistici').stream()

print("REPORTS GRAN CHEF:")
for r in reports_gc:
    print(r.id, r.to_dict())

reports_dnr = db.collection('clienti').document('DNR').collection('reports_logistici').document("07-07-2026").get()
print("\nREPORT DNR 07-07-2026:", "Esiste" if reports_dnr.exists else "Non esiste")

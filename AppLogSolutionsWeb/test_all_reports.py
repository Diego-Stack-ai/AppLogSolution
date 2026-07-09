import firebase_admin
from firebase_admin import credentials, firestore

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo_db4")

db = firestore.client(app=app)
reports = db.collection('clienti').document('DNR').collection('reports_logistici').stream()

print("TUTTI I REPORTS LOGISTICI IN Sviluppo:")
for r in reports:
    print(r.id)

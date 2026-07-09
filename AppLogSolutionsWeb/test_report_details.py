import firebase_admin
from firebase_admin import credentials, firestore

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo_db3")

db = firestore.client(app=app)
r = db.collection('clienti').document('DNR').collection('reports_logistici').document("07-07-2026").get()
print(r.to_dict())

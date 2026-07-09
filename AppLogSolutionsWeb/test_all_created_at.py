import firebase_admin
from firebase_admin import credentials, firestore

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo_db5")

db = firestore.client(app=app)
reports = db.collection('clienti').document('DNR').collection('reports_logistici').stream()

for r in reports:
    data = r.to_dict()
    print(r.id, data.get('created_at'))

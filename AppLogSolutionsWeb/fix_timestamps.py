import firebase_admin
from firebase_admin import credentials, firestore
from dateutil import parser
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo_db6")

db = firestore.client(app=app)
reports_ref = db.collection('clienti').document('DNR').collection('reports_logistici')
reports = reports_ref.stream()

for r in reports:
    data = r.to_dict()
    ca = data.get('created_at')
    if isinstance(ca, str):
        try:
            dt = parser.parse(ca)
            reports_ref.document(r.id).update({'created_at': dt})
            print(f"Updated {r.id} to {dt}")
        except Exception as e:
            print(f"Failed to parse {ca} for {r.id}: {e}")
            
print("Fix completed.")

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

col = db.collection('customers').document('DNR').collection('clienti')
docs = col.stream()
missing = 0
for d in docs:
    data = d.to_dict()
    if not data.get('lat') or str(data.get('lat')) == '0' or str(data.get('lat')) == '0.0':
        missing += 1

print('Clienti senza coordinate:', missing)

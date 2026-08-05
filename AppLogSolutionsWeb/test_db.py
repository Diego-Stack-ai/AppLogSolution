import firebase_admin
from firebase_admin import credentials, firestore

try:
    firebase_admin.get_app()
    db = firestore.client()
except ValueError:
    cred = credentials.Certificate('H:/Il mio Drive/App/AppLogSolutionsWeb/log-solution-60007-firebase-adminsdk-j33u7-0335eaf770.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

for t in ['DAC', 'CATTEL', 'GRAN CHEF']:
    docs = list(db.collection('clienti').document(t).collection('rientri ddt').stream())
    print(f"{t}: {len(docs)} documenti")
    for d in docs:
        print(f"  - {d.id}: data={d.to_dict().get('data_ddt')}, stato={d.to_dict().get('stato')}")

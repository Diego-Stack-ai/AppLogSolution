import firebase_admin
from firebase_admin import credentials, firestore

c = credentials.Certificate('backend/config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
firebase_admin.initialize_app(c)
db = firestore.client()

batch = db.batch()
count = 0
for n in ['anagrafica_clienti', 'anagrafica_articoli', 'gestione rientri']:
    for d in db.collection('clienti').document('DNR').collection(n).stream():
        batch.delete(d.reference)
        count += 1
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()

batch.commit()
print(f'Cancellati {count} documenti vecchi')

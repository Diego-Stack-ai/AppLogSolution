import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

col = db.collection('customers').document('DNR').collection('clienti')
docs = list(col.stream())
batch = db.batch()
count = 0

for d in docs:
    # If the ID is clearly one of the old pXXXX ones, migrate it.
    if d.id.lower().startswith('p'):
        new_ref = col.document()  # Auto-generates ID like 'AB123XYZ...'
        batch.set(new_ref, d.to_dict())
        batch.delete(d.reference)
        count += 1
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()

batch.commit()
print(f'Migrated {count} documents to auto-generated IDs')

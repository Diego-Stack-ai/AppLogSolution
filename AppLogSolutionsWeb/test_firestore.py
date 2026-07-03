import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate('functions/serviceAccountKey.json')
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    pass
db = firestore.client()
docs = db.collection('configurazione').get()
for doc in docs:
    print(doc.id, doc.to_dict())

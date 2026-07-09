import firebase_admin
from firebase_admin import credentials, storage

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('dev_key.json')
    app = firebase_admin.initialize_app(cred, name="test_sviluppo_storage")

bucket = storage.bucket('log-solutions-sviluppo.firebasestorage.app', app=app)
blobs = bucket.list_blobs(prefix="input_pdf_fornitore/")

print("FILES IN input_pdf_fornitore:")
for b in blobs:
    print(b.name, b.updated)

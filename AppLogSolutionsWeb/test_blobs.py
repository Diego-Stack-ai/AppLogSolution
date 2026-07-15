import json
import firebase_admin
from firebase_admin import credentials, storage, firestore

cred = credentials.Certificate("log-solutions-sviluppo-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
bucket = storage.bucket(name="log-solutions-sviluppo.appspot.com")

blobs = bucket.list_blobs(prefix="split_ddt/2026-07-09/")
for b in blobs:
    print(b.name)

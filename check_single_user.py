import firebase_admin
from firebase_admin import credentials, firestore

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

import json
doc = db.collection('users').document('xyOAp8p9v9UAJuHOaTJcpyhOAf63').get()
if doc.exists:
    print(json.dumps(doc.to_dict(), indent=2))
else:
    print("Not found")

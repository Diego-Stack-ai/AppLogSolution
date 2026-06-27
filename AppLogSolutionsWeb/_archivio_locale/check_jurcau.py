import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection("presenze").where("autista", "==", "Jurcau Florin Rares").where("mese", "==", "2026-06").stream()
for d in docs:
    data = d.to_dict()
    print(f"{d.id}: {data.get(\"data\")[:10]} - imp: {data.get(\"importo\",0)}, km: {data.get(\"kmDelta\",0)}, note: {data.get(\"note\",\"\")}")


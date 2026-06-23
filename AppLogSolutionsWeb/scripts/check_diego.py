import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
presenze = db.collection("presenze").where("autistaId", "==", "jDA7dUlEYEQ3XGDlGPh0gvm3vHb2").limit(10).stream()

for p in presenze:
    data = p.to_dict()
    print(f"{data.get('data')} M: {data.get('oraInizioM')}-{data.get('oraFineM')} P: {data.get('oraInizioP')}-{data.get('oraFineP')}")


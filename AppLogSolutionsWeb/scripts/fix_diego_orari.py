import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

diego_id = "jDA7dUlEYEQ3XGDlGPh0gvm3vHb2"
presenze = db.collection("presenze").where("autistaId", "==", diego_id).stream()
batch = db.batch()
count = 0

def fix_time(val):
    if not val or val == "-": return ""
    val = str(val).strip()
    if val.endswith(".5"):
        parts = val.split(".")
        return f"{int(parts[0]):02d}:30"
    if val.endswith(".0"):
        parts = val.split(".")
        return f"{int(parts[0]):02d}:00"
    if val.isdigit():
        return f"{int(val):02d}:00"
    if ":" in val:
        parts = val.split(":")
        if len(parts) == 2 and parts[0].isdigit():
            return f"{int(parts[0]):02d}:{parts[1]}"
    return val

for p in presenze:
    data = p.to_dict()
    updated = False
    new_data = {}
    
    for f in ["oraInizioM", "oraFineM", "oraInizioP", "oraFineP"]:
        val = str(data.get(f, ""))
        fixed = fix_time(val)
        if fixed != val:
            new_data[f] = fixed
            updated = True
            
    if updated:
        batch.update(p.reference, new_data)
        count += 1
        print(f"Aggiornato {p.id}: {new_data}")

batch.commit()
print(f"Fatto! Aggiornati {count} record.")


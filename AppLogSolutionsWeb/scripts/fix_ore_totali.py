import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

presenze = db.collection("presenze").stream()
batch = db.batch()
count = 0
updated = 0

for p in presenze:
    data = p.to_dict()
    ord = data.get("oreOrdinarie", 0)
    stra = data.get("oreStraordinarie", 0)
    
    # Handle possible string values
    try:
        ord_val = float(ord)
    except:
        ord_val = 0.0
        
    try:
        stra_val = float(stra)
    except:
        stra_val = 0.0
        
    totale_corretto = ord_val + stra_val
    totale_attuale = data.get("oreTotali", 0)
    
    try:
        tot_val = float(totale_attuale)
    except:
        tot_val = 0.0
        
    if abs(totale_corretto - tot_val) > 0.001:
        batch.update(p.reference, {"oreTotali": totale_corretto})
        updated += 1
        
    count += 1
    if updated > 0 and updated % 400 == 0:
        batch.commit()
        batch = db.batch()

if updated > 0:
    batch.commit()
    
print(f"Fatto! Analizzati {count} record, aggiornati {updated} record con il nuovo Totale Ore.")


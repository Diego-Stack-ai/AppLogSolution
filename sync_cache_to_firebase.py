import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

DRIVE_PATH = r"G:\Il mio Drive\Fatturazione"
CACHE_FILE = os.path.join(DRIVE_PATH, "CACHE_CONSEGNE_TOP.json")

def main():
    if not os.path.exists(CACHE_FILE):
        print(f"❌ Errore: {CACHE_FILE} non trovato.")
        return

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

    cred_path = r"G:\Il mio Drive\AppLogSolutions\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json"
    if not os.path.exists(cred_path):
        print("Credenziali Firebase non trovate in", cred_path)
        return
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    coll = db.collection("customers").document("GRAN CHEF").collection("clienti")
    
    docs = coll.stream()
    
    match_count = 0
    miss_count = 0
    batch = db.batch()
    
    for doc in docs:
        data = doc.to_dict()
        ind = data.get("indirizzo", "")
        loc = data.get("localita", "")
        pr = data.get("provincia", "")
        
        full_a = f"{ind}, {loc} {pr}".strip(", ")
        
        # Le chiavi nella cache sono spesso uppercase o hanno formattazioni specifiche.
        # Proviamo a scorrere la cache per fare il match (sensibile e insensibile al case)
        found_coords = cache.get(full_a)
        
        if not found_coords:
            # Fallback
            for k, v in cache.items():
                if k.lower() == full_a.lower():
                    found_coords = v
                    break
        
        if found_coords:
            batch.update(doc.reference, {
                "lat": found_coords.get("lat"),
                "lon": found_coords.get("lng")
            })
            match_count += 1
        else:
            miss_count += 1
            
        if match_count > 0 and match_count % 400 == 0:
            batch.commit()
            batch = db.batch()

    if match_count % 400 != 0:
        batch.commit()
        
    print(f"✅ Coordinate sincronizzate per GRAN CHEF: {match_count} trovate, {miss_count} non trovate.")

if __name__ == "__main__":
    main()

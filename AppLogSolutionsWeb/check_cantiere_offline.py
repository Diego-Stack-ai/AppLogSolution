import os
os.environ["GCLOUD_PROJECT"] = "log-solutions-cantiere"

from firebase_admin import credentials, firestore, storage, initialize_app
import json

print("Inizializzando l'app...")
initialize_app()
db = firestore.client()
bucket = storage.bucket("log-solutions-cantiere.appspot.com")

def check_cantiere():
    print("=== RECUPERO ULTIMI JOB COMPLETATI ===")
    
    jobs_ref = db.collection('clienti').document('DNR').collection('elaborazione_pdf')\
        .where('status', '==', 'completed')\
        .order_by('completed_at', direction=firestore.Query.DESCENDING)\
        .limit(10)\
        .stream()
        
    jobs = list(jobs_ref)
    print(f"Trovati {len(jobs)} job completati di recente.")
    
    if not jobs:
        print("Nessun job trovato.")
        return

    for doc in jobs:
        d = doc.to_dict()
        job_id = doc.id
        etichetta = d.get('type')
        data_elab = d.get('data_rilevata')
        
        print(f"\n--- JOB {job_id} ({etichetta}) ---")
        
        meta_path = f"split_ddt/{data_elab}/{etichetta}/ddt_estratti_{job_id}.json"
        print(f"Cerco JSON in: {meta_path}")
        
        blob = bucket.blob(meta_path)
        if not blob.exists():
            print("  ❌ FILE JSON NON TROVATO IN STORAGE!")
            continue
            
        print("  ✅ File JSON trovato. Analisi delle delivery...")
        content = blob.download_as_string().decode('utf-8')
        data = json.loads(content)
        
        deliveries = data.get('deliveries', [])
        print(f"  Trovate {len(deliveries)} deliveries.")
        
        campioni = [deliveries[0]] if deliveries else []
        if len(deliveries) > 1:
            campioni.append(deliveries[-1])
            
        for i, deliv in enumerate(campioni):
            print(f"  > Campione {i+1}:")
            # Check legacy
            print(f"    - codice_consegna (legacy): {deliv.get('codice_consegna', 'NON PRESENTE')}")
            print(f"    - num_ddt (legacy): {deliv.get('num_ddt', 'NON PRESENTE')}")
            
            # Check canonico
            print(f"    - schema_version: {deliv.get('schema_version', 'NON PRESENTE')}")
            print(f"    - delivery_id: {deliv.get('delivery_id', 'NON PRESENTE')}")
            print(f"    - logistics.colli: {deliv.get('logistics', {}).get('colli', 'NON PRESENTE')}")
            print(f"    - document.storage_path: {deliv.get('document', {}).get('storage_path', 'NON PRESENTE')}")

if __name__ == "__main__":
    check_cantiere()

import sys
sys.path.append('g:\\Il mio Drive\\App\\AppLogSolutionsWeb\\functions')
import main
from firebase_admin import storage

def test():
    bucket = storage.bucket(name=main.BUCKET_NAME)
    db = main.get_db()
    
    last_job = None
    for t in ['DNR', 'GRAN CHEF', 'CATTEL']:
        docs = db.collection('clienti').document(t).collection('processing_jobs').order_by('created_at', direction=main.firestore.Query.DESCENDING).limit(1).stream()
        for d in docs:
            jd = d.to_dict()
            print(f"Ultimo job in {t}: {jd.get('created_at')} -> {jd.get('storage_path')}")
            if last_job is None or jd.get('created_at').timestamp() > last_job.get('created_at').timestamp():
                last_job = jd
                
    if not last_job:
        print("Nessun job trovato")
        return
        
    path = last_job.get("storage_path")
    print(f"Test per storage path: {path}")
    
    blob = bucket.blob(path)
    file_bytes = blob.download_as_bytes()
    
    db_mappati = {}
    print("Simulazione _processa_excel_cattel_core_logic...")
    risultato = main._processa_excel_cattel_core_logic(file_bytes, db_mappati, "27-06-2026", "test_job_id")
    
    delivs = risultato.get("deliveries", [])
    print(f"Trovate {len(delivs)} deliveries.")
    if len(delivs) > 0:
        print(f"Primo elemento: {delivs[0]}")
    else:
        print("Nessuna delivery trovata! Analizziamo perche'...")

if __name__ == "__main__":
    test()

from firebase_admin import credentials, firestore, storage, initialize_app
import json

cred = credentials.Certificate("h:/Il mio Drive/App/AppLogSolutionsWeb/cantiere_key.json")
print("Inizializzando l'app al cantiere con la chiave specifica...")
initialize_app(cred, {
    'storageBucket': 'log-solutions-cantiere.appspot.com'
})
db = firestore.client()
bucket = storage.bucket()

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

    # Manteniamo traccia se abbiamo analizzato almeno un Frutta/Latte, un Cattel, un Dac, un Grand_Chef
    analizzati = set()

    for doc in jobs:
        d = doc.to_dict()
        job_id = doc.id
        etichetta = d.get('type')
        data_elab = d.get('data_rilevata')
        
        # Filtra se abbiamo già analizzato questa etichetta
        if etichetta in analizzati:
            continue
        analizzati.add(etichetta)
            
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
            print(f"    - type (legacy): {deliv.get('tipo', 'NON PRESENTE')}")
            if etichetta == 'CATTEL':
                print(f"    - autista (legacy): {deliv.get('autista', 'NON PRESENTE')}")
            if etichetta == 'GRAND_CHEF':
                print(f"    - gc_colli (legacy): {deliv.get('gc_colli', 'NON PRESENTE')}")
            
            # Check canonico
            print(f"    - schema_version: {deliv.get('schema_version', 'NON PRESENTE')}")
            print(f"    - delivery_id: {deliv.get('delivery_id', 'NON PRESENTE')}")
            print(f"    - source.parser_type: {deliv.get('source', {}).get('parser_type', 'NON PRESENTE')}")
            print(f"    - logistics.colli: {deliv.get('logistics', {}).get('colli', 'NON PRESENTE')}")
            print(f"    - logistics.peso_kg: {deliv.get('logistics', {}).get('peso_kg', 'NON PRESENTE')}")
            print(f"    - document.storage_path: {deliv.get('document', {}).get('storage_path', 'NON PRESENTE')}")
            print(f"    - time_windows: {deliv.get('time_windows', 'NON PRESENTE')}")

if __name__ == "__main__":
    check_cantiere()
